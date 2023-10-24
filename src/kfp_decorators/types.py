from typing import Callable

from kfp import dsl
from kfp.dsl.base_component import BaseComponent

ComponentDecorator = Callable[[BaseComponent], BaseComponent]
CustomizeFunction = Callable[[dsl.PipelineTask], dsl.PipelineTask]
