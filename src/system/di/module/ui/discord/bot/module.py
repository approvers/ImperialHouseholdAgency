from injector import Binder, Module, singleton

from src.system.ui.discord.bot import DiscordBot


class DiscordBotModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=DiscordBot,
            to=DiscordBot,
            scope=singleton,
        )
