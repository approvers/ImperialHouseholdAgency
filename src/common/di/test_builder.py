from abc import ABC, abstractmethod
from unittest.mock import MagicMock

from injector import Binder, singleton

from src.common.di.builder import BindEntry, ModuleBase


class MockInterface(ABC):
    @abstractmethod
    def method(self) -> str:
        pass  # pragma: no cover


class MockImplementation(MockInterface):
    def method(self) -> str:
        return "mock"


class TestBindEntry:
    def test_bind_entry_creation_without_scope(self) -> None:
        entry = BindEntry(
            interface=MockInterface,  # type: ignore[type-abstract]
            to=MockImplementation,
        )

        assert entry.interface is MockInterface
        assert entry.to is MockImplementation
        assert entry.scope is None

    def test_bind_entry_creation_with_scope(self) -> None:
        entry = BindEntry(
            interface=MockInterface,  # type: ignore[type-abstract]
            to=MockImplementation,
            scope=singleton,
        )

        assert entry.interface is MockInterface
        assert entry.to is MockImplementation
        assert entry.scope is singleton


class TestModuleBase:
    def test_configure_binds_all_entries(self) -> None:
        class TestModule(ModuleBase):
            _BINDINGS = [
                BindEntry(
                    interface=MockInterface,
                    to=MockImplementation,
                    scope=singleton,
                ),
            ]

        module = TestModule()
        binder = MagicMock(spec=Binder)

        module.configure(binder)

        binder.bind.assert_called_once()
        call_kwargs = binder.bind.call_args.kwargs
        assert call_kwargs["interface"] is MockInterface
        assert call_kwargs["to"] is MockImplementation
        assert call_kwargs["scope"] is singleton

    def test_configure_binds_multiple_entries(self) -> None:
        class AnotherInterface(ABC):
            @abstractmethod
            def another_method(self) -> int:
                pass  # pragma: no cover

        class AnotherImplementation(AnotherInterface):
            def another_method(self) -> int:
                return 42

        class TestModule(ModuleBase):
            _BINDINGS = [
                BindEntry(
                    interface=MockInterface,
                    to=MockImplementation,
                ),
                BindEntry(
                    interface=AnotherInterface,
                    to=AnotherImplementation,
                    scope=singleton,
                ),
            ]

        module = TestModule()
        binder = MagicMock(spec=Binder)

        module.configure(binder)

        assert binder.bind.call_count == 2
