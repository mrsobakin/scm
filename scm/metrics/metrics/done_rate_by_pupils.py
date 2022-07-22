
from scm.metrics.decorators import metric

@metric.element(name="Процент решивших от учеников", id="done_rate_by_pupils")
class DoneRateByPupilsMetric:
    description = """Процент успешных решений элемента (решившие / попробовавшие)"""
    
    # Author: Maksim    
    @staticmethod
    def calc(data, config):
        """
        Процент успешных решений по элементу
        Количество пользователей решивших делить на попробовших
        """
        user_element_progress = data.user_element_progress
        selected_users = user_element_progress.loc[(user_element_progress["achieve_reason"] != "transferred")\
                                               & (user_element_progress["course_element_type"] == "task")\
                                               & (user_element_progress["tries_count"] > 0),
                                               ['course_module_id', 'course_element_id', 'is_achieved']]
        selected_users = selected_users.fillna(0)
        selected_users = selected_users.groupby(["course_module_id", "course_element_id"]).agg(["count", "sum"])["is_achieved"]
        selected_users["value"] = selected_users["sum"] / selected_users["count"]
        # ^ sum считате единички(успешные решения) и делит на общее кол-во нулей и единиц
        
        selected_users = selected_users.merge(data.course_element\
                                              .query("element_type == 'task'")[["element_id", "module_id", "id"]],
                                              how="left", left_on=["course_element_id", "course_module_id"],
                                              right_on=["element_id", "module_id"])
        return selected_users[["id", "value", "count"]].rename({"count": "sample"}, axis=1)
