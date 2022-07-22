from scm.metrics.decorators import metric

@metric.element(name="Решения перебором (чекбоксы)", id="checkbox_bruteforce_metric")
class CheckboxBruteforceMetric:
    # Author: Maksim
    @staticmethod
    def calc(data, config):
        """
        Метрика показывает насколько в среднем люди пытаются перебирать задачи
        задачи - мульти (выбор нескольких элементов)
        """
        full_elements = get_full_elements(data.course_elements_inputs)
        user_element_progress = data.user_element_progress
        course_element = data.course_element

        selected = full_elements.query("(input_types == 'multi') & (count == 1)").reset_index(drop=True)
        selected.loc[:, "answers_comb"] = 2 ** selected["answers_cnt"]

        element_progress = user_element_progress.loc[(user_element_progress["achieve_reason"] != "transferred")\
                                                     & (user_element_progress["course_element_type"] == "task")\
                                                     & (user_element_progress["tries_count"] > 0)\
                                                     & (user_element_progress["is_achieved"] == True),
                                                     ["user_id", "tries_count", "course_element_id", "course_module_id"]]
        
        element_progress = element_progress.merge(course_element.query("element_type == 'task'")\
                                                  [["element_id", "module_id", "id"]],
                                                  how="left", left_on=["course_element_id", "course_module_id"],
                                                  right_on=["element_id", "module_id"])
        # ^ мне просто нужны глобальные индексы
        
        element_progress = element_progress.loc[:, ["user_id", "tries_count", "id", "element_id", "module_id"]]

        element_progress = element_progress.merge(selected, how="left", left_on=["id"],
                                                  right_on=["course_element_id"]).dropna(subset=["input_types"])
        
        element_progress["fraction"] = element_progress["tries_count"] / element_progress["answers_comb"]

        element_progress = element_progress[["id", "fraction"]].groupby(["id"]).agg(["mean", "count"])["fraction"]

        return element_progress.reset_index().rename({"mean": "value", "count": "sample"}, axis=1)
