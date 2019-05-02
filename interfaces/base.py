import collections.abc
import inspect
import typing

import interfaces.exceptions


__all__ = ['Interface', 'isimplementation']


class Interface:
    def __new__(cls, *args, **kwargs):
        raise interfaces.exceptions.InterfaceNoInstanceAllowedError(iface=cls)


def isimplementation(
    cls: type,
    interface_or_iterable: typing.Union[typing.Iterable[Interface], Interface],
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
    cls: type, iface: Interface, *, raise_errors: bool = False
) -> bool:

    for attr_name in dir(iface):

        if attr_name[:2] == attr_name[-2:] == '__':
            continue

        if not hasattr(cls, attr_name):
            return _isimplementation_fail(cls, attr_name, iface, raise_errors)

        cls_attr = inspect.getattr_static(cls, attr_name)
        iface_attr = inspect.getattr_static(iface, attr_name)

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
    cls: type, attr_name: str, iface: Interface, raise_errors: bool
) -> bool:
    if raise_errors:
        raise interfaces.exceptions.InterfaceNotImplementedError(
            klass=cls, method_name=attr_name, iface=iface
        )
    else:
        return False
