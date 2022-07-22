
import pandas as pd

from scm.metrics.decorators import metric


@metric.element(name="Сдали с первого раза", id="done_in_first_try_rate_metric")
class DoneInFirstTryRateMetric:
    description = """Доля людей, сдавших задачу с первого раза"""
    
    # jackie_chan_confused.jpg
    # Author: Sergey
    @staticmethod
    def calc(data, config):
        merge_user_element_and_course_element = pd.merge(data.user_element_progress, data.course_element[['module_id','element_id','element_type','is_advanced']], how="inner", left_on='course_element_id', right_on='element_id')
        merge_user_element_and_log = pd.merge(merge_user_element_and_course_element, data.solution_log, how="inner", left_on='id', right_on='element_progress_id')     #обьединение логов попыток сдать задачу и самих задач
        df_merge_log_check = merge_user_element_and_log[["id_x", "tries_count_y", "submission_time","verdict","course_module_id","course_element_type","course_element_id","is_advanced","course_id","course_module_id"]].sort_values(['id_x','submission_time'])     # оставил только необходимые столбики и отсортировались
        df_merge_log_check = df_merge_log_check[(df_merge_log_check['course_element_type'] == 'task') & (df_merge_log_check['is_advanced'] == False)]
        
        dict_element_size_ok = dict()     #массив количество человек решивших i задачу с 1 раза 
        dict_element_size = dict()     #массив количество человек решавших i задачу
        size_df_merge_log = len(df_merge_log_check)     #количество скинутых решений
        mass_id_element_size_ok = []     #массив с задачами которые сдавали

        for i_string_log_real in df_merge_log_check.values:
            if i_string_log_real[1] == 1:
                if dict_element_size.get(i_string_log_real[6]) == None:
                    dict_element_size[i_string_log_real[6]] = 0
                dict_element_size[i_string_log_real[6]] += 1     # прибавляет 1 i задаче (подсчитывает количество людей)
                mass_id_element_size_ok.append([i_string_log_real[8],i_string_log_real[4],i_string_log_real[6]])     # добавляет i задачу в массив
            if i_string_log_real[3] == 'ok' and i_string_log_real[1] == 1:
                if dict_element_size_ok.get(i_string_log_real[6]) == None:
                    dict_element_size_ok[i_string_log_real[6]] = 0
                dict_element_size_ok[i_string_log_real[6]] += 1     # прибавление 1 к i задаче если человек с 1 раза здал задачу

        mass_id_element_size_ok.sort()

        dt = []

        for i in range(len(mass_id_element_size_ok)):
            if i == 0 or (mass_id_element_size_ok[i] != mass_id_element_size_ok[i - 1]):
                dt.append([mass_id_element_size_ok[i][0], mass_id_element_size_ok[i][1], mass_id_element_size_ok[i][2], dict_element_size_ok[mass_id_element_size_ok[i][2]] / dict_element_size[mass_id_element_size_ok[i][2]], dict_element_size_ok[mass_id_element_size_ok[i][2]],dict_element_size[mass_id_element_size_ok[i][2]]])

            
        dt = pd.DataFrame(dt, columns = ['course_id', 'course_module_id', 'course_element_id', 'value', 'size_user_first_OK', 'sample'])

        dt_1 = pd.merge( dt, data.course_element.loc[data.course_element['element_type'] == 'task'],how = "inner", left_on = ['course_module_id','course_element_id'], right_on= ['module_id','element_id'])[['id','value', 'sample']]

        return dt_1
        
