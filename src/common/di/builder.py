import dataclasses
from abc import ABC
from typing import TYPE_CHECKING, ClassVar

from injector import Module

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable

    from injector import Binder, Scope, ScopeDecorator


@dataclasses.dataclass
class BindEntry[InterfaceT: ABC]:
    interface: type[InterfaceT]
    to: type[InterfaceT] | InterfaceT
    scope: "None | type['Scope'] | 'ScopeDecorator'" = None


class ModuleBase(Module):
    _BINDINGS: ClassVar["Iterable[BindEntry[ABC]]"]

    def configure(self, binder: "Binder") -> None:
        for entry in self._BINDINGS:
            binder.bind(
                interface=entry.interface,
                to=entry.to,
                scope=entry.scope,
            )
