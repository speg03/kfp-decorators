import os
import pathlib

import yaml
from kfp import compiler
from kfp_decorators import cpu_request, dsl


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
