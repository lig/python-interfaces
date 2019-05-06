import subprocess

import interfaces


def test_typing_self_test() -> None:
    subprocess.run(f'mypy {__file__}', check=True, shell=True)


class SampleInterface(interfaces.interface):  # type: ignore
    def method(self) -> None:
        pass


class SampleImplementation(
    interfaces.object, implements=[SampleInterface]  # type: ignore
):
    def method(self) -> None:
        pass


def typed_code_wrapper() -> SampleInterface:
    typed_var: SampleInterface
    typed_var = SampleImplementation()
    return typed_var
