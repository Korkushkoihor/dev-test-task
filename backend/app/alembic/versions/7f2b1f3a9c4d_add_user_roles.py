"""Add role-based access control to users.

Revision ID: 7f2b1f3a9c4d
Revises: fe56fa70289e
"""
from alembic import op
import sqlalchemy as sa

revision = "7f2b1f3a9c4d"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("role", sa.String(length=20), nullable=True))
    op.execute("UPDATE \"user\" SET role = CASE WHEN is_superuser THEN 'admin' ELSE 'member' END")
    op.alter_column("user", "role", nullable=False, server_default="member")


def downgrade() -> None:
    op.drop_column("user", "role")
