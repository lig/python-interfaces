from __future__ import annotations

import typing

import interfaces.exceptions
import interfaces.spec
import interfaces.util


__all__ = ['Interface']


class _InterfaceMeta(type):
    def __interface_spec__(self) -> interfaces.spec.InterfaceSpec:
        return interfaces.spec.InterfaceSpec(iface=self)

    def __subclasscheck__(self, subclass: typing.Type) -> bool:
        return interfaces.util.isimplementation(subclass, self)


class Interface(metaclass=_InterfaceMeta):
    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        raise interfaces.exceptions.InterfaceNoInstanceAllowedError(iface=cls)

    def __init_subclass__(cls) -> None:
        cls_method_names = interfaces.spec._PartialInterfaceSpec(cls).keys()

        for cls_base in cls.__bases__:

            if not isinstance(cls_base, _InterfaceMeta):
                raise TypeError(
                    "Cannot create a consistent method resolution order (MRO) for bases"
                    f" {', '.join(k.__name__ for k in cls.__bases__)}"
                )

            base_spec = interfaces.spec.interface_spec(cls_base)
            if cls_method_names.isdisjoint(base_spec.keys()):
                continue

            raise interfaces.exceptions.InterfaceOverloadingError(
                method_names=set(base_spec).intersection(cls_method_names),
                ancestor_iface=cls_base,
                descendant_iface=cls,
            )

        super().__init_subclass__()
