from typing import Callable, cast

import kfp.dsl as _kfp_dsl
from kfp.dsl import *  # noqa: F403  # type: ignore
from kfp.dsl.graph_component import GraphComponent
from kfp.dsl.python_component import PythonComponent


def component(*arg, **kwargs) -> Callable[[Callable], PythonComponent]:
    def _decorator(fn: Callable) -> PythonComponent:
        return cast(PythonComponent, _kfp_dsl.component(fn, *arg, **kwargs))

    return _decorator


def pipeline(*arg, **kwargs) -> Callable[[Callable], GraphComponent]:
    def _decorator(fn: Callable) -> GraphComponent:
        return cast(GraphComponent, _kfp_dsl.pipeline(fn, *arg, **kwargs))

    return _decorator
