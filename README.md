# Python Strict Interfaces


## Installation

```shell
pip install strict-interfaces
```


## Design Goals

* Be as strict as possible
* Fail on import time
* Do not mess with `object` and/or `type` inheritance
* Possibility to integrate in CPython Core
* Ability to use "out of the box" regardless support in an interpreter


## Features

* Special keyword `implements` on the class definition
* Multiple interface implementation
* Implicit interface implementation
* Interface inheritance with overloading being restricted
* Special `isimplementation` function similar to `issubclass`
* Partial `issubclass` support (see above)
* It's restricted to create an interface instance
* It's restricted to inherit from `object` and `interface` at the same time


## Usage

### Explicit implemetation

```python
class TestInterface(interfaces.interface):
    def method(self, arg: typeT1) -> typeT2:
        pass

class TestClass(interfaces.object, implements=[TestInterface]):
    def method(self, arg: typeT1) -> typeT2:
        pass
```

### Raises when is not implemented 

```python
class TestInterface(interfaces.interface):
    def method(self, arg):
        pass

class TestClass(interfaces.object, implements=[TestInterface]):
    pass
```

### Implicit implementation and run-time check

```python
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

assert interfaces.isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))
```

### `isimplementation` checks whether all interfaces are implemented 

```python
class TestInterfaceA(interfaces.interface):
    def method_a(arg: typeT1) -> typeT1:
        pass

class TestInterfaceB(interfaces.interface):
    def method_b(arg: typeT2) -> typeT2:
        pass

class TestClass:
    def method_a(arg: typeT1) -> typeT1:
        pass

# NOTE: In this case `isimplementation` behaves different than `issubclass`
assert not interfaces.isimplementation(TestClass, (TestInterfaceA, TestInterfaceB))
assert issubclass(TestClass, (TestInterfaceA, TestInterfaceB))
```


## Contributing

Pull requests, feature requests, and bug reports are always welcome!

[github.com/lig/python-interfaces](https://github.com/lig/python-interfaces)
