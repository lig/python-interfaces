import collections.abc
import inspect
import typing

import interfaces.exceptions


__all__ = ['interface', 'isimplementation']


class interface:
    def __new__(cls, *args, **kwargs):
        raise interfaces.exceptions.InterfaceNoInstanceAllowedError(iface=cls)


def isimplementation(
    cls: type,
    interface_or_iterable: typing.Union[typing.Iterable[interface], interface],
) -> bool:

    return all(
        _isimplementation(cls, iface)
        for iface in (
            interface_or_iterable
            if isinstance(interface_or_iterable, collections.abc.Iterable)
            else (interface_or_iterable,)
        )
    )


def _isimplementation(
    cls: type, iface: interface, *, raise_errors: bool = False
) -> bool:

    for attr_name, attr in vars(iface).items():

        if attr_name[:2] == attr_name[-2:] == '__':
            continue

        if not hasattr(cls, attr_name):
            return _isimplementation_fail(cls, attr_name, iface, raise_errors)

        cls_attr = inspect.getattr_static(cls, attr_name)

        if (
            inspect.isdatadescriptor(attr)
            and inspect.isdatadescriptor(cls_attr)
            and inspect.signature(cls_attr.__get__) == inspect.signature(attr.__get__)
            and inspect.signature(cls_attr.__set__) == inspect.signature(attr.__set__)
            and (
                inspect.signature(cls_attr.__delete__)
                == inspect.signature(attr.__delete__)
            )
        ):
            continue

        if (
            inspect.isfunction(attr)
            and inspect.isfunction(cls_attr)
            and inspect.signature(cls_attr) == inspect.signature(attr)
        ):
            continue

        return _isimplementation_fail(cls, attr_name, iface, raise_errors)

    return True


def _isimplementation_fail(
    cls: type, attr_name: str, iface: interface, raise_errors: bool
) -> bool:
    if raise_errors:
        raise interfaces.exceptions.InterfaceNotImplementedError(
            klass=cls, method_name=attr_name, iface=iface
        )
    else:
        return False
