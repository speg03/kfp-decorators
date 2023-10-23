import os
import pathlib
from typing import Callable

import yaml
from kfp import compiler
from kfp_decorators import dsl
from kfp_decorators.components import BaseComponent, CustomizedComponent


class TestCustomizedComponent:
    def customized_component(self) -> BaseComponent:
        def customize_decorator() -> Callable[[BaseComponent], BaseComponent]:
            def _decorator(fn: BaseComponent) -> BaseComponent:
                return CustomizedComponent(fn)

            return _decorator

        @customize_decorator()
        @dsl.component()
        def hello(message: str) -> str:
            return message

        return hello

    def origin_component(self) -> BaseComponent:
        @dsl.component()
        def hello(message: str) -> str:
            return message

        return hello

    def test_compile_components(self, tmp_path: pathlib.Path):
        customized_component = self.customized_component()
        package_path = os.fspath(tmp_path / "customized_component.yaml")
        compiler.Compiler().compile(customized_component, package_path)
        with open(package_path, "r") as f:
            compiled_customized_component = yaml.safe_load(f)

        origin_component = self.origin_component()
        package_path = os.fspath(tmp_path / "origin_component.yaml")
        compiler.Compiler().compile(origin_component, package_path)
        with open(package_path, "r") as f:
            compiled_origin_component = yaml.safe_load(f)

        assert compiled_customized_component == compiled_origin_component
