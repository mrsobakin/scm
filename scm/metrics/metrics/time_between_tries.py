
import datetime as dt

import pandas as pd
import numpy as np

from scm.metrics.decorators import metric


@metric.element(name="Время между попытками (del)", id="time_between_tries_del_metric")
class TimeBetweenTriesDel():
    description = """Среднее время между попытками. Время больше 40 минут не учитывается."""
    
    # Author: Ilya
    @staticmethod
    def calc(data, config):  # Время между попытками, которое > 40 минут, не учитывается
        course, course_graph, course_module, course_element, user_course_progress, user_module_progress, user_element_progress, solution_log = data.course, data.course_graph, data.course_module, data.course_element, data.user_course_progress, data.user_module_progress, data.user_element_progress, data.solution_log

        merge_user_element_and_log = pd.merge(user_element_progress, solution_log, how="inner", left_on='id', right_on='element_progress_id')     #обьединение логов попыток сдать задачу и самих задач
        df_merge_log_check = merge_user_element_and_log[["id_x", "tries_count_y", "submission_time","verdict","course_module_id","course_element_type","course_element_id","course_id"]].sort_values(['id_x','submission_time'])     # оставил только необходимые столбики и отсортировались
        df_merge_log_check = df_merge_log_check.loc[df_merge_log_check['course_element_type'] == 'task']
        df_merge_log_check.submission_time = pd.to_datetime(df_merge_log_check.submission_time)

        time_zero = pd.Timedelta('0 days 00:00:00') # перменная зделаная для того чтобы не тратить доп время для подсчёта переменной со временим 0
        time_40 = pd.Timedelta('0 days 00:40:00') # перменная зделаная для того чтобы не тратить доп время для подсчёта переменной со временим 40

        dict_time_element = dict()     #смотрите документацию
        dict_size_user_in_element = dict()     #массив количеста людей сдававших i задачу (тоже объясняется в документации)
        mass_id_element = []     #массив с задачами которые здавали


        mass_log = df_merge_log_check.values     # массив log которые мы проверяем
        last_pack = mass_log[0]
        mass_log = mass_log[1::]

        fl = 0     # флаг, отмечает сдал ли человек задачу
        for real_pack in mass_log:
            if last_pack[0] == real_pack[0] and fl == 0:     # проверка на то что real_pack и last_pack это попытки которые здавал один и тот же user, проверка того что на данный момент не сдал задачу
                if real_pack[2] - last_pack[2] < time_40:
                    time_for_user = real_pack[2] - last_pack[2]
                    dict_time_element[real_pack[6]] = dict_time_element.get(real_pack[6], time_zero) + time_for_user  # прибавление времени к i задаче затраченое на следующую попытку
                    mass_id_element.append([real_pack[7],real_pack[4],real_pack[6]])     # добавляет i задачу в массив
                    dict_size_user_in_element[real_pack[6]] = dict_size_user_in_element.get(real_pack[6], 0) + 1 # прибавляет 1 i задаче (подсчитывает количество людей)
                    if real_pack[3] == 'ok':
                        fl = 1 # человек сдал задачу
            elif last_pack[0] != real_pack[0]:
                fl = 0
            last_pack = real_pack
        mass_id_element.sort()
        mass_dt =[]
        for i in range(len(mass_id_element)):
            if i == 0 or (mass_id_element[i] != mass_id_element[i - 1]):
                mass_dt.append([mass_id_element[i][0], mass_id_element[i][1], mass_id_element[i][2], dict_time_element[mass_id_element[i][2]] / dict_size_user_in_element[mass_id_element[i][2]], dict_size_user_in_element[mass_id_element[i][2]]])

        dt = pd.DataFrame(mass_dt, columns = ['course_id', 'course_module_id', 'course_element_id', 'value', 'sample'])
        dt = pd.merge( dt, course_element.loc[course_element['element_type'] == 'task'],how = "inner", left_on = ['course_module_id','course_element_id'], right_on= ['module_id','element_id'])[['id', 'value', 'sample']]
        
        dt["value"] = dt["value"].apply(lambda x: x.total_seconds() / 60)
        
        return dt

@metric.element(name="Время между попытками (clip)", id="time_between_tries_clip_metric")
class TimeBetweenTriesClip():
    description = """Среднее время между попытками. Время > 40 минут приравневается к 40 минутам"""
    
    # Author: Ilya
    @staticmethod
    def calc(data, config):  # Время между попытками, которое > 40 минут, приравнивается к 40 минутам
        course, course_graph, course_module, course_element, user_course_progress, user_module_progress, user_element_progress, solution_log = data.course, data.course_graph, data.course_module, data.course_element, data.user_course_progress, data.user_module_progress, data.user_element_progress, data.solution_log

        merge_user_element_and_log = pd.merge(user_element_progress, solution_log, how="inner", left_on='id', right_on='element_progress_id')     #обьединение логов попыток сдать задачу и самих задач 
        df_merge_log_check = merge_user_element_and_log[["id_x", "tries_count_y", "submission_time","verdict","course_module_id","course_element_type","course_element_id","course_id"]].sort_values(['id_x','submission_time'])     # оставил только необходимые столбики и отсортировались 
        df_merge_log_check = df_merge_log_check.loc[df_merge_log_check['course_element_type'] == 'task']
        df_merge_log_check.submission_time = pd.to_datetime(df_merge_log_check.submission_time)

        time_zero = pd.Timedelta('0 days 00:00:00') # перменная зделаная для того чтобы не тратить доп время для подсчёта переменной со временим 0 
        time_40 = pd.Timedelta('0 days 00:40:00') # перменная зделаная для того чтобы не тратить доп время для подсчёта переменной со временим 40 

        dict_time_element = dict()     #смотрите документацию 
        dict_size_user_in_element = dict()     #массив количеста людей сдававших i задачу (тоже объясняется в документации) 
        mass_id_element = []     #массив с задачами которые здавали 


        mass_log = df_merge_log_check.values     # массив log которые мы проверяем 
        last_pack = mass_log[0]
        mass_log = mass_log[1::]

        fl = 0     # флаг, отмечает сдал ли человек задачу 
        for real_pack in mass_log:
            if last_pack[0] == real_pack[0] and fl == 0:     # проверка на то что real_pack и last_pack это попытки которые здавал один и тот же user, проверка того что на данный момент не сдал задачу  
                time_for_user = min(real_pack[2] - last_pack[2], time_40)
                dict_time_element[real_pack[6]] = dict_time_element.get(real_pack[6], time_zero) + time_for_user  # прибавление времени к i задаче затраченое на следующую попытку   
                mass_id_element.append([real_pack[7],real_pack[4],real_pack[6]])     # добавляет i задачу в массив 
                dict_size_user_in_element[real_pack[6]] = dict_size_user_in_element.get(real_pack[6], 0) + 1 # прибавляет 1 i задаче (подсчитывает количество людей)     
                if real_pack[3] == 'ok':
                    fl = 1 # человек сдал задачу 
            elif last_pack[0] != real_pack[0]:
                fl = 0
            last_pack = real_pack
        mass_id_element.sort()
        mass_dt =[]
        for i in range(len(mass_id_element)):
            if i == 0 or (mass_id_element[i] != mass_id_element[i - 1]):
                mass_dt.append([mass_id_element[i][0], mass_id_element[i][1], mass_id_element[i][2], dict_time_element[mass_id_element[i][2]] / dict_size_user_in_element[mass_id_element[i][2]], dict_size_user_in_element[mass_id_element[i][2]]])

        dt = pd.DataFrame(mass_dt, columns = ['course_id', 'course_module_id', 'course_element_id', 'value', 'sample'])
        dt = pd.merge( dt, course_element.loc[course_element['element_type'] == 'task'],how = "inner", left_on = ['course_module_id','course_element_id'], right_on= ['module_id','element_id'])[['id', 'value', 'sample']]
        
        dt["value"] = dt["value"].apply(lambda x: x.total_seconds() / 60)
        
        return dt
