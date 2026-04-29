# -*- coding: utf-8 -*-
"""Add context snapshots to execution logs."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0003_execution_log_context"
down_revision = "0002_execution_logs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("execution_logs", sa.Column("task_project_id_snapshot", sa.Integer(), nullable=True))
    op.add_column("execution_logs", sa.Column("cognitive_load_snapshot", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("execution_logs", "cognitive_load_snapshot")
    op.drop_column("execution_logs", "task_project_id_snapshot")
