import pytest

from src.ui.discord.config import DiscordConfigIF


def test_discord_config_if_is_abstract() -> None:
    with pytest.raises(TypeError):
        DiscordConfigIF()  # type: ignore[abstract]
