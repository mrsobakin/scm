
import pandas as pd
import numpy as np

from scm.metrics.decorators import metric


@metric.module(name="Затраченное время", id="time_spent_metric")
class TimeSpentMetric:
    # Author: Maksim
    @staticmethod
    def calc(data, config):
        """
        Рассчитывается затраченное время по всем модулям к конкретным
        модулям учитывая стандартное отклонение и среднее
        """
        user_module_progress = data.user_module_progress.copy()

        user_module_progress["time_achieved"] = pd.to_datetime(user_module_progress["time_achieved"])
        user_module_progress["time_unlocked"] = pd.to_datetime(user_module_progress["time_unlocked"])

        user_module_progress = user_module_progress[~user_module_progress["time_achieved"].isna() & ~user_module_progress["time_unlocked"].isna()]
        # ^ там где время точно известно и это не перенос
        user_module_progress = user_module_progress[user_module_progress["time_unlocked"] < user_module_progress["time_achieved"]]
        # удаляем жуликов -> ---жулик, не воруй!---
        user_module_progress["time_module_diff"] = user_module_progress["time_achieved"] - user_module_progress["time_unlocked"]
        # ^ сколько решал задачу

        delta = pd.Timedelta("5 min")

        temp = user_module_progress[["course_module_id", "time_module_diff"]].groupby("course_module_id").agg(lambda x: np.median([i for i in x if delta <= i]))
        
        # ^ высчитали медиану по всем группам модулей

        threshold = temp["time_module_diff"].mean()
        std_time = temp["time_module_diff"].std()

        temp_norm = (temp["time_module_diff"] - threshold) / std_time
        temp_norm[temp_norm < 0] = 0
        # ^ так надо, иначе нули, иначе смысл теряется

        df = pd.DataFrame(temp_norm.sort_values(ascending=False).apply(lambda x: min(x, 1)))

        return df.reset_index().rename(columns={"course_module_id": "id", "time_module_diff": "value"})
