import typing

import pytest

import interfaces


@pytest.fixture(scope='session')
def typeT1():
    return typing.TypeVar('T1')


@pytest.fixture(scope='session')
def typeT2():
    return typing.TypeVar('T2')


def test_010_empty_definition():
    class TestInterface(interfaces.interface):
        pass

    class TestClass(interfaces.object, implements=[TestInterface]):
        pass


def test_020_non_iterable_as_implements_value():
    class TestInterface(interfaces.interface):
        pass

    class TestClass(interfaces.object, implements=TestInterface):
        pass


def test_030_error_non_interface_as_implements_value():
    class TestInterface(interfaces.interface):
        pass

    with pytest.raises(TypeError):

        class TestClass(interfaces.object, implements=[object]):
            pass


def test_040_method_is_implemented_no_annotations():
    class TestInterface(interfaces.interface):
        def method(self, arg):
            pass

    class TestClass(interfaces.object, implements=[TestInterface]):
        def method(self, arg):
            pass


def test_050_method_is_implemented_with_annotations(typeT1, typeT2):
    class TestInterface(interfaces.interface):
        def method(self, arg: typeT1) -> typeT2:
            pass

    class TestClass(interfaces.object, implements=[TestInterface]):
        def method(self, arg: typeT1) -> typeT2:
            pass


def test_060_error_method_is_not_implemented():
    class TestInterface(interfaces.interface):
        def method(self, arg):
            pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(interfaces.object, implements=[TestInterface]):
            pass


def test_070_error_method_params_signature_is_not_implemented(typeT1, typeT2):
    class TestInterface(interfaces.interface):
        def method(self, arg: typeT1) -> typeT2:
            pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(interfaces.object, implements=[TestInterface]):
            def method(self, arg: typeT2) -> typeT2:
                pass


def test_080_error_method_return_signature_is_not_implemented(typeT1, typeT2):
    class TestInterface(interfaces.interface):
        def method(self, arg: typeT1) -> typeT2:
            pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(interfaces.object, implements=[TestInterface]):
            def method(self, arg: typeT1) -> typeT1:
                pass


def test_090_property_is_implemented_no_annotations():
    class TestInterface(interfaces.interface):
        @property
        def value(self):
            pass

    class TestClass(interfaces.object, implements=[TestInterface]):
        @property
        def value(self):
            pass


def test_100_error_property_is_implemented_as_method_no_annotations():
    class TestInterface(interfaces.interface):
        @property
        def value(self):
            pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(interfaces.object, implements=[TestInterface]):
            def value(self):
                pass


def test_110_error_interface_instance():
    class TestInterface(interfaces.interface):
        pass

    with pytest.raises(interfaces.InterfaceNoInstanceAllowedError):
        _ = TestInterface()


def test_120_interface_inheritance(typeT1, typeT2):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(TestInterfaceA):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass(interfaces.object, implements=[TestInterfaceB]):
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass


def test_130_error_not_implemented_with_inheritance(typeT1, typeT2):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(TestInterfaceA):
        def method_b(arg: typeT2) -> typeT2:
            pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClass(interfaces.object, implements=[TestInterfaceB]):
            def method_b(arg: typeT2) -> typeT2:
                pass


def test_140_interface_multiple_inheritance(typeT1, typeT2):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestInterfaceC(TestInterfaceA, TestInterfaceB):
        pass

    class TestClass(interfaces.object, implements=[TestInterfaceB]):
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass


def test_150_error_not_implemented_with_multiple_inheritance(typeT1, typeT2):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestInterfaceC(TestInterfaceA, TestInterfaceB):
        pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClassA(interfaces.object, implements=[TestInterfaceC]):
            def method_a(arg: typeT1) -> typeT1:
                pass

    with pytest.raises(interfaces.InterfaceNotImplementedError):

        class TestClassB(interfaces.object, implements=[TestInterfaceC]):
            def method_b(arg: typeT2) -> typeT2:
                pass
