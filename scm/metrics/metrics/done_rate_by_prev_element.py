import pandas as pd

def get_achieved_users_by_task(user_element_progress):
    """
    Находит для каждого элемента (task) юзеров, решивших задачу
    """
    selected = user_element_progress.loc[(user_element_progress["achieve_reason"] != "transferred")\
                                         & (user_element_progress["course_element_type"] == "task")\
                                         & (user_element_progress["is_achieved"] == True),
                                         ['course_element_id', 'user_id']]
    df = selected.groupby(['course_element_id']).agg(lambda x: (set(x), len(x)))
    return dict(df.itertuples())


from scm.metrics.decorators import metric

@metric.element(name="Процент решивших от предыдущего элемента", id="done_rate_by_prev_element_metric")
class DoneRateByPrevElementMetric:
    description = """Процент решивших задачу, относительно предыдущего элемента (решившие данную / решившие предыдущую)"""
    
    @staticmethod
    def calc(data, config):
        """
        Для каждого таска в модуле, начиная со второго, считается
        (решили задачу и решили предыдущую задачу) / (решили предыдущую задачу)
        """
        course_element = data.course_element.sort_values(by=["module_id", "position"])
        course_element = course_element[course_element["element_type"] == "task"]
        # ^ просто фильтруем и выстраиваем порядок

        elements_achieved = get_achieved_users_by_task(data.user_element_progress)
        # ^ для каждого таска собираем юзеров, решивших задачу

        idxs = course_element[["module_id", "element_id"]].values

        values = []

        previous_module_id = None
        for module_id, index in idxs:
            if previous_module_id != module_id:
                previous_module_id = module_id
                previous_index = index
                previous_achived, previous_count = elements_achieved[index]
                continue
                
            current_achived, current_count = elements_achieved[index]
            values.append((module_id, previous_index, index, len(previous_achived & current_achived) / previous_count, previous_count))
            #                                      ^ (решили нынешнею и предыдущую задачи) / (решили предыдущую задачу)
            previous_achived, previous_count = current_achived, current_count
            previous_index = index

        values = pd.DataFrame(values, columns=["module_id", "previous_index", "current_index", "value", "sample"])
        values["course_id"] = data.course.loc[0, "id"]
        
        values = values.merge(data.course_element.query("element_type == 'task'")[["element_id", "module_id", "id"]],
                              how="left", left_on=["current_index", "module_id"],
                              right_on=["element_id", "module_id"])

        return values[['id', 'value', 'sample']]
