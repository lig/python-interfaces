import pytest

import interfaces


def test_010_empty_definition():
    class TestInterface(interfaces.interface):
        pass

    class TestClass(interfaces.InterfaceImplementationBase, implements=[TestInterface]):
        pass


def test_020_non_iterable_as_implements_value():
    class TestInterface(interfaces.interface):
        pass

    class TestClass(interfaces.InterfaceImplementationBase, implements=TestInterface):
        pass


def test_030_error_non_interface_as_implements_value():
    class TestInterface(interfaces.interface):
        pass

    with pytest.raises(TypeError):

        class TestClass(interfaces.InterfaceImplementationBase, implements=[int]):
            pass


def test_040_method_is_implemented_no_annotations():
    class TestInterface(interfaces.interface):
        def method(self, attr):
            return attr

    class TestClass(interfaces.InterfaceImplementationBase, implements=[TestInterface]):
        def method(self, attr):
            return attr


def test_050_method_is_implemented_with_annotations():
    class TestInterface(interfaces.interface):
        def method(self, attr: str) -> int:
            return len(attr)

    class TestClass(interfaces.InterfaceImplementationBase, implements=[TestInterface]):
        def method(self, attr: str) -> int:
            return len(attr)


def test_060_error_method_is_not_implemented():
    class TestInterface(interfaces.interface):
        def method(self, attr):
            return attr

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(
            interfaces.InterfaceImplementationBase, implements=[TestInterface]
        ):
            pass


def test_070_error_method_params_signature_is_not_implemented():
    class TestInterface(interfaces.interface):
        def method(self, attr: str) -> int:
            return len(attr)

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(
            interfaces.InterfaceImplementationBase, implements=[TestInterface]
        ):
            def method(self, attr: int) -> int:
                return attr


def test_080_error_method_return_signature_is_not_implemented():
    class TestInterface(interfaces.interface):
        def method(self, attr: str) -> int:
            return len(attr)

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(
            interfaces.InterfaceImplementationBase, implements=[TestInterface]
        ):
            def method(self, attr: str) -> str:
                return attr


def test_090_property_is_implemented_no_annotations():
    class TestInterface(interfaces.interface):
        @property
        def value(self):
            return 42

    class TestClass(interfaces.InterfaceImplementationBase, implements=[TestInterface]):
        @property
        def value(self):
            return 'sample string'


def test_100_error_property_is_implemented_as_method_no_annotations():
    class TestInterface(interfaces.interface):
        @property
        def value(self):
            return 42

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(
            interfaces.InterfaceImplementationBase, implements=[TestInterface]
        ):
            def value(self):
                return 'sample string'
