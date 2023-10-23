from typing import Callable, Optional

from kfp import dsl
from kfp.dsl.base_component import BaseComponent


class CustomizedComponent(BaseComponent):
    def __init__(
        self,
        component: BaseComponent,
        customize_fn: Optional[Callable[[dsl.PipelineTask], dsl.PipelineTask]] = None,
    ):
        self.component = component
        self.customize_fn = customize_fn

    def __call__(self, *args, **kwargs):
        task = self.component(*args, **kwargs)
        if self.customize_fn:
            self.customize_fn(task)
        return task

    def execute(self, *args, **kwargs):
        return self.component.execute(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.component, name)
