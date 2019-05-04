import pytest

import interfaces


@pytest.fixture(scope='session', params=[interfaces.isimplementation, issubclass])
def isimplementation(request):
    return request.param


def test_010_isimplementation_single_true_explicit_interface(
    typeT1, typeT2, isimplementation
):
    class TestInterface(interfaces.interface):
        def method(arg: typeT1) -> typeT2:
            pass

    class TestClass(interfaces.object, implements=[TestInterface]):
        def method(arg: typeT1) -> typeT2:
            pass

    assert isimplementation(TestClass, TestInterface)


def test_020_isimplementation_single_true_explicit_object(
    typeT1, typeT2, isimplementation
):
    class TestInterface(interfaces.interface):
        def method(arg: typeT1) -> typeT2:
            pass

    class TestClass(interfaces.object):
        def method(arg: typeT1) -> typeT2:
            pass

    assert isimplementation(TestClass, TestInterface)


def test_030_isimplementation_single_true(typeT1, typeT2, isimplementation):
    class TestInterface(interfaces.interface):
        def method(arg: typeT1) -> typeT2:
            pass

    class TestClass:
        def method(arg: typeT1) -> typeT2:
            pass

    assert isimplementation(TestClass, TestInterface)


def test_040_isimplementation_single_false(typeT1, typeT2, isimplementation):
    class TestInterface(interfaces.interface):
        def method(arg: typeT1) -> typeT2:
            pass

    class TestClass:
        pass

    assert not isimplementation(TestClass, TestInterface)


def test_050_isimplementation_multi_true_one_explicit(typeT1, typeT2, isimplementation):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass(interfaces.object, implements=[TestInterfaceA, TestInterfaceB]):
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass

    assert isimplementation(TestClass, TestInterfaceA)


def test_060_isimplementation_multi_true_one(typeT1, typeT2, isimplementation):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass:
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass

    assert isimplementation(TestClass, TestInterfaceA)


def test_070_isimplementation_multi_true_all_explicit(typeT1, typeT2, isimplementation):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass(interfaces.object, implements=[TestInterfaceA, TestInterfaceB]):
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass

    assert isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))


def test_080_isimplementation_multi_true_all(typeT1, typeT2, isimplementation):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass:
        def method_a(arg: typeT1) -> typeT1:
            pass

        def method_b(arg: typeT2) -> typeT2:
            pass

    # NOTE: In this case `isimplementation` behaves different than `issubclass`
    assert isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))


def test_090_isimplementation_multi_false_one(typeT1, typeT2):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass:
        def method_a(arg: typeT1) -> typeT1:
            pass

    assert not interfaces.isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))


def test_100_isimplementation_multi_false_all(typeT1, typeT2, isimplementation):
    class TestInterfaceA(interfaces.interface):
        def method_a(arg: typeT1) -> typeT1:
            pass

    class TestInterfaceB(interfaces.interface):
        def method_b(arg: typeT2) -> typeT2:
            pass

    class TestClass:
        pass

    assert not isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))
