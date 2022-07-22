
import itertools
from dataclasses import dataclass, field

import pandas as pd
from pandas import DataFrame

import scm.utils


def _empty_metric_df():
    return DataFrame({"id": pd.Series(dtype="int")})


@dataclass
class MetricResult():
    value: float = float("nan")
    sample: int = None
    
    @classmethod
    def from_df(cls, df):
        return cls(
            value = df["value"],
            sample = df["sample"] if "sample" in df else None
        )
    
    @classmethod
    def collapse_df(cls, df):
        return scm.utils.collapse_columns(
            df = df,
            keep = ["id"],
            name = "metric",
            f = cls.from_df
        )


@dataclass
class Metrics:
    df: DataFrame = field( default_factory = _empty_metric_df )
    metrics: dict = field( default_factory = dict )
    info_metrics: dict = field( default_factory = dict )

    def split(self):
        def f(df):
            return type(self)(
                df = DataFrame(df).T,
                metrics = self.metrics,
                info_metrics = self.info_metrics
            )
        return scm.utils.collapse_columns(self.df, ["id"], "metrics", f)

    @classmethod
    def concat(cls, lst):
        metrics, info_metrics = {}, {}

        lst=list(lst)

        for metric in lst:
            metrics.update( metric.metrics )
            info_metrics.update( metric.info_metrics )

        try:
            df = pd.concat( (metric.df for metric in lst), ignore_index=True )
        except ValueError:
            df = _empty_metric_df()

        df = df.reindex(columns = ["id"]+list(metrics.keys() | info_metrics.keys()))
        
        df = df.fillna(MetricResult)

        return cls(
            df = df, 
            metrics = metrics,
            info_metrics = info_metrics
        )

    @classmethod
    def empty(cls, idlist):
        return cls(
            df = DataFrame({"id": idlist})
        )


@dataclass
class MultiMetrics:
    element: Metrics = field( default_factory = Metrics )
    module: Metrics = field( default_factory = Metrics )
    course: Metrics = field( default_factory = Metrics )

    def merge_with_metric(self, metric):
        metrics_obj = getattr(self, metric.type)

        metrics_obj.df = metrics_obj.df.merge( 
            metric.result.rename(columns={ "metric": metric.id }), 
            on="id", 
            how="outer" 
        )
        
        metrics_obj.df.fillna( MetricResult, inplace = True )
        
        id_dct = metrics_obj.info_metrics if metric.is_info else metrics_obj.metrics
        id_dct[metric.id] = type(metric)

    @classmethod
    def concat(cls, lst):
        lst = list(lst)
        return cls(
            element = Metrics.concat(mm.element for mm in lst),
            module = Metrics.concat(mm.module for mm in lst),
            course = Metrics.concat(mm.course for mm in lst)
        )

    def to_df(self):
        return self.element.split(), self.module.split(), self.course.split()


from scm.metrics.metrics.infometrics import *
from scm.metrics.metrics.avg_try_count import *
from scm.metrics.metrics.mmv_conversion import *
from scm.metrics.metrics.done_rate_by_media import *
from scm.metrics.metrics.done_rate_by_pupils import *
from scm.metrics.metrics.done_rate_by_prev_element import *
from scm.metrics.metrics.done_in_first_try_rate import *
from scm.metrics.metrics.avg_solve_impr_time import *
from scm.metrics.metrics.time_spent import *
from scm.metrics.metrics.course_cert import *
from scm.metrics.metrics.time_between_tries import *
from scm.metrics.metrics.module_done_rate import *
from scm.metrics.metrics.module_drop_rate import *


class SiriusCoursesMetricCalculator:
    def __init__(self, external_metrics=None):
        metrics = [ 
            NumberOfCourseStudentsInfometric, 
            NumberOfModuleStudentsInfometric, 
            AchievedInModuleNumberInfometric,
            AverageTryCountMetric, 
            ConversionMetric, 
            MeanModuleScoreMetric,
            DoneRateByMediaMetric,
            DoneRateByPrevElementMetric,
            # DoneRateByPupilsMetric,
            DoneInFirstTryRateMetric,
            AvgSolveImpovementTimeMetric,
            CertRateExceptingTransfered,
            # TimeBetweenTriesDel,
            TimeBetweenTriesClip,
            # ModuleDoneRate,
            ModuleDropOnRate,
            TimeSpentMetric

            #CheckboxBruteforceMetric
        ]
        # ^ TODO: move somewhere else.

        if external_metrics:
            metrics.extend(external_metrics)

        self.metrics = { metric.id: metric for metric in metrics }

    def calc_metrics(self, data, metrics_ids, config={}):
        """
            Computes all metrics in `metrics_ids`.
        """
        
        if metrics_ids == "*":
            metrics_ids = self.metrics.keys()
        
        multimetrics = MultiMetrics()

        for metric_id in metrics_ids:
            cfg = config.get(metric_id, {})
            
            metric = self.metrics[metric_id](data, cfg)

            multimetrics.merge_with_metric(metric)

        return multimetrics

