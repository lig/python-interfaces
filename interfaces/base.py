from __future__ import annotations

import collections.abc
import functools
import inspect
import types
import typing

import interfaces.exceptions


__all__ = ['Interface', 'isimplementation']


class Interface:
    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> None:
        raise interfaces.exceptions.InterfaceNoInstanceAllowedError(iface=cls)

    def __init_subclass__(cls) -> None:
        cls_method_names = _PartialInterfaceSpec(cls).keys()
        for cls_base in cls.__bases__:
            base_spec = interface_spec(cls_base)
            if cls_method_names.isdisjoint(base_spec.keys()):
                continue
            raise interfaces.exceptions.InterfaceOverloadingError(
                method_names=set(base_spec).intersection(cls_method_names),
                ancestor_iface=cls_base,
                descendant_iface=cls,
            )
        super().__init_subclass__()

    @classmethod
    def __interface_spec__(cls) -> InterfaceSpec:
        return InterfaceSpec(iface=cls)


class InterfaceSpec(collections.abc.Mapping):
    slots = ('_iface', '_iface_spec')

    def __init__(self, iface: typing.Type[Interface]) -> None:
        self._iface = iface
        self._iface_spec = {
            attr_name: getattr(iface, attr_name)
            for attr_name in self._get_iface_attrs(iface)
            if not (attr_name[:2] == attr_name[-2:] == '__')
        }

    def __getitem__(self, key: str) -> types.MethodType:
        return self._iface_spec[key]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self._iface_spec)

    def __len__(self) -> int:
        return len(self._iface_spec)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__!s}({self._iface!r})"

    @staticmethod
    def _get_iface_attrs(
        iface: typing.Type[Interface]
    ) -> collections.abc.Iterable[str]:
        return dir(iface)


class _PartialInterfaceSpec(InterfaceSpec):
    @staticmethod
    def _get_iface_attrs(
        iface: typing.Type[Interface]
    ) -> collections.abc.Iterable[str]:
        return vars(iface).keys()


def isimplementation(
    cls: type,
    interface_or_iterable: typing.Union[
        typing.Iterable[typing.Type[Interface]], typing.Type[Interface]
    ],
) -> bool:

    return all(
        _isimplementation(cls, iface)
        for iface in (
            interface_or_iterable  # type: ignore
            if isinstance(interface_or_iterable, collections.abc.Iterable)
            else (interface_or_iterable,)
        )
    )


@functools.lru_cache(maxsize=None)
def interface_spec(iface: typing.Type[Interface]) -> InterfaceSpec:
    return iface.__interface_spec__()


def _isimplementation(
    cls: type, iface: typing.Type[Interface], *, raise_errors: bool = False
) -> bool:

    for attr_name, iface_attr in interface_spec(iface).items():

        if attr_name[:2] == attr_name[-2:] == '__':
            continue

        if not hasattr(cls, attr_name):
            return _isimplementation_fail(cls, attr_name, iface, raise_errors)

        cls_attr = inspect.getattr_static(cls, attr_name)

        if (
            inspect.isdatadescriptor(iface_attr)
            and inspect.isdatadescriptor(cls_attr)
            and (
                inspect.signature(cls_attr.__get__)
                == inspect.signature(iface_attr.__get__)
            )
            and (
                inspect.signature(cls_attr.__set__)
                == inspect.signature(iface_attr.__set__)
            )
            and (
                inspect.signature(cls_attr.__delete__)
                == inspect.signature(iface_attr.__delete__)
            )
        ):
            continue

        if (
            inspect.isfunction(iface_attr)
            and inspect.isfunction(cls_attr)
            and inspect.signature(cls_attr) == inspect.signature(iface_attr)
        ):
            continue

        return _isimplementation_fail(cls, attr_name, iface, raise_errors)

    return True


def _isimplementation_fail(
    cls: type, attr_name: str, iface: typing.Type[Interface], raise_errors: bool
) -> bool:
    if raise_errors:
        raise interfaces.exceptions.InterfaceNotImplementedError(
            klass=cls, method_name=attr_name, iface=iface
        )
    else:
        return False
