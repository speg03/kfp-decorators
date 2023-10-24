import os
import pathlib

import kfp.dsl as kfp_dsl
import yaml
from kfp import compiler
from kfp_decorators import dsl
from kfp_decorators.pipeline_task import BaseComponent


class TestComponent:
    def wrapper_component(self) -> BaseComponent:
        @dsl.component()
        def hello(message: str) -> str:
            return message

        return hello

    def origin_component(self) -> BaseComponent:
        @kfp_dsl.component()
        def hello(message: str) -> str:
            return message

        return hello  # type: ignore

    def test_compile_components(self, tmp_path: pathlib.Path):
        wrapper_component = self.wrapper_component()
        package_path = os.fspath(tmp_path / "wrapper_component.yaml")
        compiler.Compiler().compile(wrapper_component, package_path)
        with open(package_path, "r") as f:
            compiled_wrapper_component = yaml.safe_load(f)

        origin_component = self.origin_component()
        package_path = os.fspath(tmp_path / "origin_component.yaml")
        compiler.Compiler().compile(origin_component, package_path)
        with open(package_path, "r") as f:
            compiled_origin_component = yaml.safe_load(f)

        assert compiled_wrapper_component == compiled_origin_component


class TestPipeline:
    def wrapper_pipeline(self) -> BaseComponent:
        @dsl.component()
        def hello(message: str) -> str:
            return message

        @dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        return hello_pipeline

    def origin_pipeline(self) -> BaseComponent:
        @kfp_dsl.component()
        def hello(message: str) -> str:
            return message

        @kfp_dsl.pipeline(name="hello")
        def hello_pipeline(message: str = "hello") -> None:
            hello(message=message)

        return hello_pipeline  # type: ignore

    def test_compile_pipelines(self, tmp_path: pathlib.Path):
        wrapper_pipeline = self.wrapper_pipeline()
        package_path = os.fspath(tmp_path / "wrapper_pipeline.yaml")
        compiler.Compiler().compile(wrapper_pipeline, package_path)
        with open(package_path, "r") as f:
            compiled_wrapper_pipeline = yaml.safe_load(f)

        origin_pipeline = self.origin_pipeline()
        package_path = os.fspath(tmp_path / "origin_pipeline.yaml")
        compiler.Compiler().compile(origin_pipeline, package_path)
        with open(package_path, "r") as f:
            compiled_origin_pipeline = yaml.safe_load(f)

        assert compiled_wrapper_pipeline == compiled_origin_pipeline
