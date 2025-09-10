import dataclasses
from typing import TYPE_CHECKING, Generic, TypeVar

from injector import Module

if TYPE_CHECKING:
    from typing import Union, Iterable
    from abc import ABC

    from injector import Scope, ScopeDecorator, Binder


InterfaceT = TypeVar("InterfaceT", bound="ABC")


@dataclasses.dataclass
class BindEntry(Generic[InterfaceT]):
    interface: type[InterfaceT]
    to: type[InterfaceT]
    scope: "Union[None, type['Scope'], 'ScopeDecorator']" = None


class ModuleBase(Module):
    _BINDINGS: "Iterable[BindEntry[ABC]]"

    def configure(self, binder: "Binder") -> None:
        for entry in self._BINDINGS:
            binder.bind(
                interface=entry.interface,
                to=entry.to,
                scope=entry.scope,
            )
