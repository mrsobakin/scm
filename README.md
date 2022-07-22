# Sirius Courses Metrics

A tool for calculating difficulty metrics and generating analytic reports for Sirius Courses

## Installation
```bash
git clone ...
cd scm
pip install .
```


## Using

### Standalone
SCM can be used as a standalone tool.
For exporting metrics `csv` subcommand is used.
`python -m scm csv "path/to/data" "path/to/metrics/folder"`

Report is generated with `report` subcommand.
`python -m scm csv "path/to/data" "path/to/report/file"`


### As a module
SCM can also be used as a python module. Below is a simple example for generating report.
```python
from scm.metrics import SiriusCoursesMetricCalculator
from scm.types import *
import scm.report

# Loading csv files
data = SiriusCoursesData.from_path("path/to/some/data")

scmc = SiriusCoursesMetricCalculator()

# Calculating metrics
metrics = scmc.calc_metrics(data, "*", config = {
    "avg_try_count": {
        "upper_clip": 50        
    }    
})

# Creating course structure
course = Course.from_data(data, metrics)[0]

# Generating report
html = scm.report.from_course(course)

with open(args[1], "w") as f:
	f.write(str(html))
```