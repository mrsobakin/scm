
import datetime as dt

import pandas as pd

from scm.metrics.decorators import metric

@metric.module(name="Доля бросивших на модуле", id="module_drop_on_rate_metric")
class ModuleDropOnRate:
    description = """Доля учеников, бросивших курс на данном модуле, среди всех бросивших курс"""
    
    # Author: Ilya
    @staticmethod
    def calc(data, config):  # доля бросивших модуль среди всех бросивших курс
        course, course_graph, course_module, course_element, user_course_progress, user_module_progress, user_element_progress, solution_log = data.course, data.course_graph, data.course_module, data.course_element, data.user_course_progress, data.user_module_progress, data.user_element_progress, data.solution_log

        modules = set(course_module['id'][(course_module.type == 'ordinary') & (course_module.level == 1)])
        first_modules = list(modules - set(course_graph.to_module_id))

        df = user_element_progress.merge(solution_log, left_on='id', right_on='element_progress_id', how='left')
        df = df[['module_progress_id', 'time_achieved', 'submission_time', 'course_element_type']]
        df = df.merge(user_module_progress, left_on='module_progress_id', right_on='id')
        df = df[df['is_achieved'] == False][['course_id', 'course_module_id', 'course_element_type', 'user_id', 'time_achieved_x', 'submission_time']]
        df = df[(df['time_achieved_x'].notna()) | (df['submission_time'].notna())]
        time_achieved, submission_time = df['time_achieved_x'], df['submission_time']
        df['time_action'] = [submission_time.iloc[i] if pd.notnull(submission_time.iloc[i]) else time_achieved.iloc[i] for i in range(len(submission_time))]
        df = df[['course_id', 'course_module_id', 'user_id', 'time_action']]
        df.time_action = pd.to_datetime(df.time_action)
        df = df.sort_values('time_action', ascending=False)

        d = {}
        sm = 0
        close = pd.to_datetime(course.iloc[0]['close_date'])
        for user_id, group in df.groupby('user_id'):
            row = group.iloc[0]
            if close - row['time_action'] >= dt.timedelta(days=7) and (row['course_id'], row['course_module_id']) not in first_modules:
                d[row['course_module_id']] = d.get(row['course_module_id'], 0) + 1
                sm += 1

        df = []
        course_id = course.iloc[0]['id']
        for module_id in course_module['id']:
            df.append([course_id, module_id, d.get(module_id, 0) / sm, sm])

        df = pd.DataFrame(df, columns=['course_id', 'id', 'value', 'sample'])
        return df.drop(columns=['course_id'])
