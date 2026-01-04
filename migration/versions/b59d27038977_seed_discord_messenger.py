"""seed discord messenger

Revision ID: b59d27038977
Revises: 87e1bd665ac8
Create Date: 2026-01-04 17:06:36.786834

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b59d27038977'
down_revision: Union[str, Sequence[str], None] = '87e1bd665ac8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 固定 ULID（再実行可能にするため、26文字）
# ULID は 0123456789ABCDEFGHJKMNPQRSTVWXYZ のみ使用可能
DISCORD_MESSENGER_ULID = "01JGQK0000D1SC0RD00000000"


def upgrade() -> None:
    """Upgrade schema."""
    messenger_table = sa.table(
        "messenger",
        sa.column("record_id", sa.String),
        sa.column("name", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )

    now = datetime.now(timezone.utc)

    op.bulk_insert(
        messenger_table,
        [
            {
                "record_id": DISCORD_MESSENGER_ULID,
                "name": "discord",
                "created_at": now,
                "updated_at": now,
            }
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    messenger_table = sa.table(
        "messenger",
        sa.column("record_id", sa.String),
    )

    op.execute(
        messenger_table.delete().where(
            messenger_table.c.record_id == DISCORD_MESSENGER_ULID
        )
    )
