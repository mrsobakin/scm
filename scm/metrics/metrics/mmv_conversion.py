
from scm.metrics.decorators import metric

@metric.module(name="Средний балл", id="mean_module_score_metric")
class MeanModuleScoreMetric:
    description = """Средний балл (в процентах) учеников дошедших до модуля, начавших учиться и решивших хотя бы одну задачу"""
    # Author: Maksim
    @staticmethod
    def calc(data, config):
        """
        Средний балл (в процентах) учеников дошедших до модуля, начавших учиться и решивших хотя бы одну задачу
        """
        user_module_progress = data.user_module_progress
        course_module = data.course_module
        course = data.course
        course_element = data.course_element

        user_module_progress = user_module_progress.loc[~user_module_progress["time_unlocked"].isna()]
        # ^ игнорируем учеников, которые перенесли результаты
        user_module_progress = user_module_progress.loc[user_module_progress["progress_current"] > 0]
        # ^ решили хотя бы одну задачу
        values = course_module.merge(user_module_progress, how="inner", left_on="id",
                                     right_on="course_module_id")\
                                     .groupby("course_module_id")["progress_current"].agg(["mean", "std", "count"])

        # ищем максимум по модулю
        values = values.merge(course_module[["id", "progress_max"]], left_on="course_module_id", right_on="id", how="left")

        # нормируем
        values["mean"] /= values["progress_max"]
        values["std"] /= values["progress_max"]

        return values[["id", "mean", "count"]].rename({"mean": "value", "count": "sample"}, axis=1)

@metric.module(name="Конверсия", id="module_conversion_metric")
class ConversionMetric:
    description = """Конверсия учеников дошедших до модуля, начавших учиться"""
    #                                   ^ Че это значит???
    
    # Author: Maksim    
    @staticmethod
    def calc(data, config):
        """
        Конверсия учеников дошедших до модуля, начавших учиться
        """
        user_element_progress = data.user_element_progress
        user_module_progress = data.user_module_progress
        course_module = data.course_module

        target_counts = MeanModuleScoreMetric.calc(data, config)

        user_start_learn = user_element_progress.loc[user_element_progress["is_achieved"] == True,
                                                     ["course_module_id", "user_id"]].drop_duplicates()
        user_start_learn["is_start>"] = True
        # ^ начали учиться и продолжили

        user_module_progress = user_module_progress.loc[~user_module_progress["time_unlocked"].isna()]
        # ^ игнорируем учеников, которые перенесли результаты
        merged = user_module_progress.merge(user_start_learn, how="left", on=["user_id", "course_module_id"])
        merged = merged[merged['is_start>'] == True]
        # ^ выбираем только тех, кто начал учиться и продолжил

        values = course_module.merge(merged, how="inner", left_on="id",
                                     right_on="course_module_id")\
                                     .groupby("course_module_id")["progress_current"].agg(["count"])
        # ^ общее количество учеников: учатся и продолжают

        values = values.merge(course_module[["id"]], left_on="course_module_id", right_on="id", how="left")
        # ^ уже не помню

        values = values.merge(target_counts, on="id", how="left")
        values["value"] = values["sample"] /  values["count"]

        return values[["id", "value", "sample"]]
