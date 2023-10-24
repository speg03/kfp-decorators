import os
import pathlib

import yaml
from kfp import compiler
from kfp_decorators import cpu_request, dsl, memory_request
from kfp_decorators.pipeline_task import CustomizedComponent
from kfp_decorators.types import BaseComponent, ComponentDecorator


class TestCustomizedComponent:
    def customized_component(self) -> BaseComponent:
        def customize_decorator() -> ComponentDecorator:
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


class TestCpuRequest:
    def test_compile_pipelines(self, tmp_path: pathlib.Path):
        @cpu_request("100m")
        @dsl.component()
        def hello(message: str) -> str:
            return message

        @dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        package_path = os.fspath(tmp_path / "hello_pipeline.yaml")
        compiler.Compiler().compile(hello_pipeline, package_path)

        with open(package_path, "r") as f:
            pipeline = yaml.safe_load(f)

        assert (
            pipeline["deploymentSpec"]["executors"]["exec-hello"]["container"][
                "resources"
            ]["cpuRequest"]
            == 0.1
        )


class TestMemoryRequest:
    def test_compile_pipelines(self, tmp_path: pathlib.Path):
        @memory_request("100Mi")
        @dsl.component()
        def hello(message: str) -> str:
            return message

        @dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        package_path = os.fspath(tmp_path / "hello_pipeline.yaml")
        compiler.Compiler().compile(hello_pipeline, package_path)

        with open(package_path, "r") as f:
            pipeline = yaml.safe_load(f)

        assert (
            pipeline["deploymentSpec"]["executors"]["exec-hello"]["container"][
                "resources"
            ]["memoryRequest"]
            == 0.1048576
        )
