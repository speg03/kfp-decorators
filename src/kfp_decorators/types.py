from typing import Callable, TypeAlias

from kfp import dsl
from kfp.dsl.base_component import BaseComponent

ComponentDecorator: TypeAlias = Callable[[BaseComponent], BaseComponent]
CustomizeFunction: TypeAlias = Callable[[dsl.PipelineTask], dsl.PipelineTask]
