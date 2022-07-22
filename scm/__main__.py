
import sys
from pathlib import Path

import pandas as pd

from scm.metrics import SiriusCoursesMetricCalculator
from scm.types import *
import scm.report
import scm.utils

def generate_csv(metrics):
    types = ["element", "module", "course"]
    
    for type in types:
        df = getattr(metrics, type).df
        
        for column in df.columns[1:]:
            df[column] = df[column].apply( lambda cell: cell.value )
        
        yield df.to_csv(index=False)


def main():
    subcmd, *args = sys.argv[1:]

    folder = args[0]
    data = SiriusCoursesData.from_path(folder)

    scmc = SiriusCoursesMetricCalculator()

    # TODO: change * to whitelist/blacklist
    metrics = scmc.calc_metrics(data, "*", config = {
        "avg_try_count": {
            "upper_clip": 50        
        }    
    })

    if subcmd == "csv":
        for metric, t in zip(generate_csv(metrics), "emc"):
            with open(f"{args[1]}/metrics_{t}.csv", "w") as f:
                f.write(str(metric))

    elif subcmd ==  "report":
        course = Course.from_data(data, metrics)[0]

        html = scm.report.from_course(course)

        with open(args[1], "w") as f:
            f.write(str(html))


if __name__ == "__main__":
    main()
