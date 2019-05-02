__all__ = ['InterfaceNoInstanceAllowedError', 'InterfaceNotImplementedError']


class InterfaceError(Exception):
    pass


class InterfaceNoInstanceAllowedError(InterfaceError):
    def __init__(self, *, iface):
        self._iface = iface

    def __str__(self):
        return (
            f"Attempted to create an instance of interface `{self._iface!r}` which is"
            " not allowed"
        )


class InterfaceNotImplementedError(InterfaceError):
    def __init__(self, *, klass, method_name, iface):
        self._klass = klass
        self._method_name = method_name
        self._iface = iface

    def __str__(self):
        return (
            f"`{self._klass!r}` must fully implement `{self._method_name!s}` method of"
            f" `{self._iface}`"
        )
