from typing import Optional

from .types import BaseComponent, ComponentDecorator, CustomizeFunction


class CustomizedComponent(BaseComponent):
    def __init__(
        self,
        component: BaseComponent,
        customize_fn: Optional[CustomizeFunction] = None,
    ):
        self.component = component
        self.customize_fn = customize_fn

    def __call__(self, *args, **kwargs):
        task = self.component(*args, **kwargs)
        if self.customize_fn:
            return self.customize_fn(task)
        return task

    def execute(self, *args, **kwargs):
        return self.component.execute(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.component, name)


def cpu_request(cpu_request: str) -> ComponentDecorator:
    def _decorator(fn: BaseComponent) -> BaseComponent:
        return CustomizedComponent(fn, lambda task: task.set_cpu_request(cpu_request))

    return _decorator


def memory_request(memory_request: str) -> ComponentDecorator:
    def _decorator(fn: BaseComponent) -> BaseComponent:
        return CustomizedComponent(
            fn, lambda task: task.set_memory_request(memory_request)
        )

    return _decorator
