from setuptools import setup, find_packages

setup(
    name = 'scm',
    version = '0.1.0',    
    description = 'Sirius Courses Metrics',
    packages = [
        "scm", 
        "scm.metrics", 
        "scm.metrics.metrics", 
        "scm.report"
    ],
    install_requires = [
        "dominate>=2.6.0", 
        "matplotlib>=3.5.2", 
        "numpy>=1.22.4", 
        "pandas>=1.4.3", 
        "pygraphviz>=1.9", 
        "seaborn>=0.11.2"
    ]
)
