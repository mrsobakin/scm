from scm.metrics.decorators import infometric
from scm.metrics import MetricResult

@infometric.course(name="Количество учеников", id="number_of_students_infometric")
class NumberOfCourseStudentsInfometric:
    @staticmethod
    def calc(data, config):
        return data.user_course_progress.groupby("course_id", as_index=False).size().set_axis(["id", "value"], axis=1)


@infometric.module(name = "Количество учеников", id = "number_of_module_students_infometric")
class NumberOfModuleStudentsInfometric:
    @staticmethod
    def calc(data, config):
        return data.user_module_progress[["course_module_id", "time_unlocked"]].dropna().groupby("course_module_id", as_index=False).size().set_axis(["id", "value"], axis=1)



@infometric.module(name = "Получили зачет", id="achieved_in_module_number_infometric")
class AchievedInModuleNumberInfometric:
    @staticmethod
    def calc(data, config):
        return data.user_module_progress[["course_module_id", "time_achieved"]].dropna().groupby("course_module_id", as_index=False).size().set_axis(["id", "value"], axis=1)

