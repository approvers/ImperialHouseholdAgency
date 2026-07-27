import dataclasses
from typing import TYPE_CHECKING, Generic, TypeVar

from injector import Module

if TYPE_CHECKING:  # pragma: no cover
    from abc import ABC
    from collections.abc import Iterable

    from injector import Binder, Scope, ScopeDecorator


InterfaceT = TypeVar("InterfaceT", bound="ABC")


@dataclasses.dataclass
class BindEntry(Generic[InterfaceT]):
    interface: type[InterfaceT]
    to: type[InterfaceT] | InterfaceT
    scope: "None | type['Scope'] | 'ScopeDecorator'" = None


class ModuleBase(Module):
    _BINDINGS: "Iterable[BindEntry[ABC]]"

    def configure(self, binder: "Binder") -> None:
        for entry in self._BINDINGS:
            binder.bind(
                interface=entry.interface,
                to=entry.to,
                scope=entry.scope,
            )
