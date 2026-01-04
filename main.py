from src.system.di.container import DIContainer
from src.system.infrastructure.ext.logfire.init import init_logfire
from src.system.ui.discord.bot import DiscordBot


def main() -> None:
    init_logfire()

    bot = DIContainer.get(DiscordBot)
    bot.run_bot()


if __name__ == "__main__":
    main()
