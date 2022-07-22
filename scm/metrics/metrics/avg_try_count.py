import pandas as pd

import scm.utils
from scm.metrics.decorators import metric

# Author: Nikita+Maksim
def _get_latest_ok_submissions(data):
    """
    Returns average try count, grouped by `course_element_id`
    - `tries_count` is the number of first `ok` solution
    - solutions that never were solved are rejected
    - `transfered` results are rejected
    """

    df = data.solution_log[ 
        ["element_progress_id", "tries_count", "verdict"] 
    ]

    df = df.merge(
        data.user_element_progress[ ["id", "course_module_id", "course_element_type", "course_element_id", "achieve_reason"] ], 
        left_on="element_progress_id", 
        right_on="id"
    )

    df = df[ (df["achieve_reason"] != "transferred") & (df["verdict"] == "ok") ]

    df = df.merge(
        data.course_element,
        left_on = ["course_module_id", "course_element_type", "course_element_id"],
        right_on = ["module_id", "element_type", "element_id"]
    )

    df = df[ df["is_advanced"] != True ]

    df = df[ ["id_y", "element_progress_id", "tries_count"] ]

    #df = df.sort_values("submission_time")

    df = df.groupby(["id_y", "element_progress_id"]).agg(scm.utils.first_or_none)

    return df


@metric.element(name="Среднее число попыток", id="avg_try_count", have_sample=True)
class AverageTryCountMetric:
    description = """Среднее число попыток для решения задачи. Рассчитывается по первой успешной попытке"""
        
    # Author: Nikita+Maksim  
    @staticmethod
    def calc(data, config):
        """
            Returns average try count, grouped by `course_element_id`
            - `tries_count` is the number of first `ok` solution
            - solutions that never were solved are rejected
            - `transfered` results are rejected
        """
        df = _get_latest_ok_submissions(data)

        df["tries_count"] = df["tries_count"].clip( upper = config["upper_clip"] )

        mean = df.groupby(level=0).agg(["mean", "size"]).reset_index()

        res = mean.set_axis(["id", "value", "sample"], axis=1)
        return res
