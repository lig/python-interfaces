from __future__ import annotations

import collections.abc
import functools
import types
import typing

import interfaces.base
import interfaces.typing


class InterfaceSpec(collections.abc.Mapping):
    slots = ('_iface', '_iface_spec')

    def __init__(self, iface: interfaces.typing.InterfaceType) -> None:
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
        iface: interfaces.typing.InterfaceType
    ) -> collections.abc.Iterable[str]:
        return dir(iface)


class _PartialInterfaceSpec(InterfaceSpec):
    @staticmethod
    def _get_iface_attrs(
        iface: interfaces.typing.InterfaceType
    ) -> collections.abc.Iterable[str]:
        return vars(iface).keys()


@functools.lru_cache(maxsize=None)
def interface_spec(iface: interfaces.typing.InterfaceType) -> InterfaceSpec:
    return iface.__interface_spec__()
