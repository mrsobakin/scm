
import pandas as pd

from scm.metrics.decorators import metric

@metric.module(name="Доля сдавших модуль", id="module_done_rate_metric")
class ModuleDoneRate:
    description = """Доля учеников, получивших зачет по модулю"""
    
    # Author: Ilya
    @staticmethod
    def calc(data, config):  # Вычисляет долю тех, у кого получен зачет по модулю
        course, course_graph, course_module, course_element, user_course_progress, user_module_progress, user_element_progress, solution_log = data.course, data.course_graph, data.course_module, data.course_element, data.user_course_progress, data.user_module_progress, data.user_element_progress, data.solution_log

        elem_progress = user_element_progress[(user_element_progress['course_element_type'] == 'task') & (user_element_progress['tries_count'] > 0) & (user_element_progress['achieve_reason'] != 'transferred')][['user_id', 'course_module_id', 'course_element_id', 'module_progress_id']]
        mod_progress = user_module_progress[['id', 'user_id', 'is_achieved', 'course_id', 'course_module_id']]

        d = {}
        ans = []
        for (module_id), group in elem_progress.groupby('course_module_id'):
            d[module_id] = set(group['user_id'])
        for (course_id, module_id), group in mod_progress.groupby(['course_id', 'course_module_id']):
            group = group[group['user_id'].isin(d[module_id])]
            ans.append([course_id, module_id, len(group[group['is_achieved'] == True]) / len(group), len(group)])

        ans = pd.DataFrame(ans, columns=['course_id', 'id', 'value', 'sample'])

        return ans.drop(columns=["course_id"])
