import typing


if typing.TYPE_CHECKING:
    import interfaces.base

    InterfaceType = typing.Type[interfaces.base.Interface]
