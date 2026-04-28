# -*- coding: utf-8 -*-
"""Add execution history logs."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0002_execution_logs"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "execution_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("task_title_snapshot", sa.String(length=300), nullable=False),
        sa.Column("estimated_minutes_snapshot", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("actual_minutes", sa.Integer(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint(
            "status IN ('done','skipped','incomplete','canceled')",
            name="ck_execution_logs_status",
        ),
    )
    op.create_index("ix_execution_logs_date", "execution_logs", ["date"])
    op.create_index("ix_execution_logs_task_id", "execution_logs", ["task_id"])


def downgrade() -> None:
    op.drop_index("ix_execution_logs_task_id", table_name="execution_logs")
    op.drop_index("ix_execution_logs_date", table_name="execution_logs")
    op.drop_table("execution_logs")

