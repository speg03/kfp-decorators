import functools
from typing import Callable, cast

from kfp import dsl
from kfp.dsl.base_component import BaseComponent


def cpu_request(cpu_request: str) -> Callable[[BaseComponent], BaseComponent]:
    def _decorator(fn: BaseComponent) -> BaseComponent:
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs) -> dsl.PipelineTask:
            task = fn(*args, **kwargs)
            task.set_cpu_request(cpu_request)
            return task

        return cast(BaseComponent, _wrapper)

    return _decorator
