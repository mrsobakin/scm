
from collections import namedtuple
from scm.metrics import MetricResult

def __metric(name, id, type, is_info, have_sample=False, desc_file=None):
    def wrap(cls):
        cls.name = name
        cls.id = id
        cls.type = type
        cls.is_info = is_info
        cls.have_sample = have_sample
        
        if desc_file:
            with open(desc_file, "r") as f:
                cls.description = f.read()
        else:
            if not hasattr(cls, "description"):
                if cls.calc.__doc__:
                    cls.description = cls.calc.__doc__
                else:
                    cls.description = name
        
        def __init__(self, data, config):
            self.result = MetricResult.collapse_df(
                self.calc(data, config)
            )

        cls.__init__ = __init__

        return cls
    return wrap


metric = namedtuple("metric", ["element", "module", "course"])(
    element = lambda *args, **kwargs: __metric(*args, **kwargs, type="element", is_info=False),
    module = lambda *args, **kwargs: __metric(*args, **kwargs, type="module", is_info=False),
    course = lambda *args, **kwargs: __metric(*args, **kwargs, type="course", is_info=False)
)


infometric = namedtuple("infometric", ["element", "module", "course"])(
    element = lambda *args, **kwargs: __metric(*args, **kwargs, type="element", is_info=True),
    module = lambda *args, **kwargs: __metric(*args, **kwargs, type="module", is_info=True),
    course = lambda *args, **kwargs: __metric(*args, **kwargs, type="course", is_info=True)
)

