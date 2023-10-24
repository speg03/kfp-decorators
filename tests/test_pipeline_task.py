import os
import pathlib

import pytest
import yaml
from kfp import compiler
from kfp_decorators import chain, cpu_request, dsl, memory_request
from kfp_decorators.pipeline_task import CustomizedComponent
from kfp_decorators.types import BaseComponent, ComponentDecorator


class TestCustomizedComponent:
    @pytest.fixture
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

    @pytest.fixture
    def origin_component(self) -> BaseComponent:
        @dsl.component()
        def hello(message: str) -> str:
            return message

        return hello

    @pytest.fixture
    def customized_pipeline(self) -> BaseComponent:
        def customize_decorator() -> ComponentDecorator:
            def _decorator(fn: BaseComponent) -> BaseComponent:
                return CustomizedComponent(fn)

            return _decorator

        @customize_decorator()
        @dsl.component()
        def hello(message: str) -> str:
            return message

        @dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        return hello_pipeline

    @pytest.fixture
    def origin_pipeline(self) -> BaseComponent:
        @dsl.component()
        def hello(message: str) -> str:
            return message

        @dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        return hello_pipeline

    def test_compile_components(
        self,
        tmp_path: pathlib.Path,
        customized_component: BaseComponent,
        origin_component: BaseComponent,
    ):
        package_path = os.fspath(tmp_path / "customized_component.yaml")
        compiler.Compiler().compile(customized_component, package_path)
        with open(package_path, "r") as f:
            compiled_customized_component = yaml.safe_load(f)

        package_path = os.fspath(tmp_path / "origin_component.yaml")
        compiler.Compiler().compile(origin_component, package_path)
        with open(package_path, "r") as f:
            compiled_origin_component = yaml.safe_load(f)

        assert compiled_customized_component == compiled_origin_component

    def test_compile_pipelines(
        self,
        tmp_path: pathlib.Path,
        customized_pipeline: BaseComponent,
        origin_pipeline: BaseComponent,
    ):
        package_path = os.fspath(tmp_path / "customized_pipeline.yaml")
        compiler.Compiler().compile(customized_pipeline, package_path)
        with open(package_path, "r") as f:
            compiled_customized_pipeline = yaml.safe_load(f)

        package_path = os.fspath(tmp_path / "origin_pipeline.yaml")
        compiler.Compiler().compile(origin_pipeline, package_path)
        with open(package_path, "r") as f:
            compiled_origin_pipeline = yaml.safe_load(f)

        assert compiled_customized_pipeline == compiled_origin_pipeline

    def test_local_execute(self, customized_component: BaseComponent):
        assert customized_component.execute(message="hello") == "hello"


class TestChain:
    def test_compile_pipelines(self, tmp_path: pathlib.Path):
        default_resource = chain(cpu_request("100m"), memory_request("100Mi"))

        @default_resource
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

        executor = pipeline["deploymentSpec"]["executors"]["exec-hello"]
        assert executor["container"]["resources"]["cpuRequest"] == 0.1
        assert executor["container"]["resources"]["memoryRequest"] == 0.1048576


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

        executor = pipeline["deploymentSpec"]["executors"]["exec-hello"]
        assert executor["container"]["resources"]["cpuRequest"] == 0.1


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

        executor = pipeline["deploymentSpec"]["executors"]["exec-hello"]
        assert executor["container"]["resources"]["memoryRequest"] == 0.1048576
