from typing import Callable

from .components import BaseComponent, CustomizedComponent


def cpu_request(cpu_request: str) -> Callable[[BaseComponent], BaseComponent]:
    def _decorator(fn: BaseComponent) -> BaseComponent:
        return CustomizedComponent(fn, lambda task: task.set_cpu_request(cpu_request))

    return _decorator
