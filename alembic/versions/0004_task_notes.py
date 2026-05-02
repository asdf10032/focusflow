# -*- coding: utf-8 -*-
"""Add notes to tasks."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0004_task_notes"
down_revision = "0003_execution_log_context"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "notes")
