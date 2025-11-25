import pytest

from src.system.ui.discord.config import DiscordConfigIf


def test_discord_config_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        DiscordConfigIf()  # type: ignore[abstract]
