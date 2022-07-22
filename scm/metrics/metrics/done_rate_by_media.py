import pandas as pd

def get_blocks_by_module(course_element):
    """
    Рзабивает модули на блоки
    {
        module_id: [(media_id, tasks)]
    }
    """
    types = set(["video", "text"])
    split_by_module = {}
    for i, df in course_element.sort_values(by=["module_id", "position"]).groupby("module_id"):
        splitted = []
        temp = []
        for index, element_type, element_id in df[["element_type", "element_id"]].itertuples():
            if element_type in types:
                if temp:
                    splitted.append(temp)
                    temp = [(element_id, element_type)]
                else:
                    temp.append((element_id, element_type))
            else:
                temp.append(element_id)
            
        if temp: splitted.append(temp)

        split_by_module[i] = [(j[0], j[1:]) for j in splitted]
    return split_by_module


def get_achieved_users_by_element(user_element_progress):
    """
    Находит для каждого элемента юзеров, решивших задачу
    """
    selected = user_element_progress.loc[(user_element_progress["achieve_reason"] != "transferred")\
                                         & (user_element_progress["is_achieved"] == True),
                                         ['course_element_id', "course_element_type", 'user_id']]
    df = selected.groupby(['course_element_id', "course_element_type"]).agg(set)
    return dict(df.itertuples())


from scm.metrics.decorators import metric

@metric.element(name="Процент решивших от смотревших теорию", id="done_rate_by_media")
class DoneRateByMediaMetric:
    description = """Процент решивших задачу, из посмотревших предыдущий теоретический материал (решившие / посмотревшие т.м.)"""
    
    # Author: Maksim
    @staticmethod
    def calc(data, config):
        """
        Считает для каждого элемента долю тех кто
        (смотрел и решил) / (смотрел) - столбец fraction
        меньше - хуже
        """
        course_module = data.course_module
        user_element_progress = data.user_element_progress
        course_element = data.course_element

        # фильтруем модули, чтобы теор. информация была всегда до задач
        ordinary_modules = set(course_module.loc[course_module["type"] == "ordinary", "id"])
        user_element_progress = user_element_progress[user_element_progress["course_module_id"].isin(ordinary_modules)]
        course_element = course_element[course_element["module_id"].isin(ordinary_modules)]

        split_by_module = get_blocks_by_module(course_element) # получаем блоки модулей
        elements_achieved = get_achieved_users_by_element(user_element_progress)
        # ^ получаем словарь {(el_id, el_type): set(users)}

        results = []
        for module_id, blocks in split_by_module.items():
            for media, tasks in blocks:
                if media in elements_achieved:
                    user_seen = elements_achieved[media]
                    user_seen_length = len(user_seen)
                    for task_id in tasks:
                        user_solved = elements_achieved[(task_id, "task")]
                        results.append((module_id, "task", task_id, len(user_seen & user_solved) / user_seen_length, user_seen_length))
        df = pd.DataFrame(results, columns=["module_id", "element_type", "element_id", "value", "sample"])

        df = df.merge(data.course_element\
                      .query("element_type == 'task'")[["element_id", "module_id", "id"]],
                      how="left", left_on=["element_id", "module_id"],
                      right_on=["element_id", "module_id"])
        return df[["id", "value", "sample"]]
