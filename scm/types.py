from pathlib import Path
from dataclasses import dataclass
import json

import pandas as pd
from pandas import DataFrame

import scm.utils
from scm.metrics import Metrics, MultiMetrics


@dataclass
class SiriusCoursesData:
    course: DataFrame
    course_module: DataFrame
    course_element: DataFrame
    user_element_progress: DataFrame
    user_module_progress: DataFrame
    solution_log: DataFrame
    user_course_progress: DataFrame
    course_graph: DataFrame
    course_graph_layout: DataFrame

    @classmethod
    def from_path(cls, path):
        path = Path(path)

        course = pd.read_csv(Path(path, "course.csv"))
        course_module = pd.read_csv(Path(path, "course_module.csv"))
        course_element = pd.read_csv(Path(path, "course_element.csv"))
        user_element_progress = pd.read_csv(Path(path, "user_element_progress.csv"))
        user_module_progress = pd.read_csv(Path(path, "user_module_progress.csv"))
        solution_log = pd.read_csv(Path(path, "solution_log.csv"))
        user_course_progress = pd.read_csv(Path(path, "user_course_progress.csv"))
        course_graph = pd.read_csv(Path(path, "course_graph.csv"))
        course_graph_layout = pd.read_csv(Path(path, "course_graph_layout.csv"))

        return cls(course, course_module, course_element, user_element_progress, user_module_progress, solution_log, user_course_progress, course_graph, course_graph_layout)


@dataclass
class CourseGraphEdge:
    course_id: int
    from_module_id: int
    to_module_id: int
    type: str

    @classmethod
    def from_df(cls, df):
        return cls(
            course_id = df["course_id"],
            from_module_id = df["from_module_id"],
            to_module_id = df["to_module_id"],
            type = df["type"]  
        )


@dataclass
class Element:
    metrics: Metrics

    id: int
    module_id: int
    element_type: str
    element_id: int
    is_advanced: bool
    max_tries: int
    score: int
    position: int

    @classmethod
    def from_df(cls, df):
        return cls(
            id = df["id"],
            module_id = df["module_id"],
            element_type = df["element_type"],
            element_id = df["element_id"],
            is_advanced = df["is_advanced"],
            max_tries = df["max_tries"],
            score = df["score"],
            position = df["position"],

            metrics = df["metrics"] if pd.notna(df["metrics"]) else Metrics.empty([df["id"]])
        )

    def get_multimetrics(self):
        return MultiMetrics(element=metrics)


@dataclass
class Module:
    elements: dict
    elements_order: list
    metrics: Metrics

    id: int
    course_id: int
    percent_to_pass: int
    is_advanced: bool
    progress_max: int
    steps_max: int
    tasks_max: int
    type: str
    level: int
    title: str

    @classmethod
    def from_df(cls, df):
        order = [ element.id for element in sorted(df["element"].values(), key=lambda x: x.position) ]

        return cls(
            id = df["id"],
            course_id = df["course_id"],
            percent_to_pass = df["percent_to_pass"],
            is_advanced = df["is_advanced"],
            progress_max = df["progress_max"],
            steps_max = df["steps_max"],
            tasks_max = df["tasks_max"],
            type = df["type"],
            level = df["level"],
            title = df["title"],

            elements = df["element"],
            elements_order = order,
            metrics = df["metrics"] if pd.notna(df["metrics"]) else Metrics.empty([df["id"]])
        )

    def get_multimetrics(self):
        return MultiMetrics(
            element = Metrics.concat(
                scm.utils.filter_nan(
                    element.metrics for element in self.elements.values()
                )
            ),
            module = self.metrics
        )


@dataclass
class Course:
    modules: dict
    graph: list
    graph_layout: dict
    metrics: Metrics
    
    id: int
    date_start: int
    close_date: int
    knowledge_area_id: int
    course_name: str

    @classmethod
    def from_df(cls, df):
        return cls(            
            id = df["id"],
            date_start = df["date_start"],
            close_date = df["close_date"],
            knowledge_area_id = df["knowledge_area_id"],
            course_name = df["name"],

            modules = df["module"],        
            graph = df["graph"],
            graph_layout = scm.utils.dict_keys_map( 
                json.loads( df["graph_layout"] )["module_positions"], 
                int ),
            metrics = df["metrics"] if pd.notna(df["metrics"]) else Metrics.empty([df["id"]])
        )

    def get_multimetrics(self):
        return MultiMetrics.concat(
            scm.utils.filter_nan(
                scm.utils.chain_element(
                    ( module.get_multimetrics() for module in self.modules.values() ),
                    MultiMetrics(course=self.metrics)      
                )
            )            
        )

    @staticmethod
    def from_data(data, metrics = None):

        dict_by_id = lambda x: scm.utils.dict_from_list(x, "id")

        metrics_element_df, metrics_module_df, metrics_course_df = metrics.to_df()

        course_element = data.course_element.merge(metrics_element_df, on="id", how="outer")
        me_df = scm.utils.collapse_and_group(course_element, "module_id", "element", Element.from_df, agg_func=dict_by_id)

        course_module = data.course_module.merge(metrics_module_df, on="id", how="outer")
        cm_df = course_module.merge( me_df, left_on="id", right_on="module_id" )
        cm_df = scm.utils.collapse_and_group(cm_df, "course_id", "module", Module.from_df, agg_func=dict_by_id)


        graphs = scm.utils.collapse_and_group(data.course_graph, "course_id", "graph", CourseGraphEdge.from_df)

        lc_raw = data.course.merge( cm_df, left_on="id", right_on="course_id" )
        lc_raw = lc_raw.merge( graphs, left_on="id", right_on="course_id" )
        lc_raw = lc_raw.merge( data.course_graph_layout.rename(columns={"content": "graph_layout"}), left_on="id", right_on="course_id" )

        lc_raw = lc_raw.merge( metrics_course_df, on="id", how="outer" )

        courselist = lc_raw.apply(Course.from_df, axis=1).agg(list)

        return courselist
