"""add id column to anomaly_events

Revision ID: add_id_column
Revises: e14f5ddde47d
Create Date: 2026-01-09 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_id_column'
down_revision: Union[str, Sequence[str], None] = 'e14f5ddde47d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add id column to anomaly_events table if it doesn't exist."""
    # Check if id column already exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    try:
        columns = [col['name']
                   for col in inspector.get_columns('anomaly_events')]
    except Exception:
        # Table doesn't exist yet, skip this migration
        return

    if 'id' not in columns:
        # Add id column (nullable first to allow existing rows)
        op.add_column('anomaly_events',
                      sa.Column('id', sa.Text(), nullable=True))

        # Generate ULIDs for existing rows using PostgreSQL's gen_random_uuid
        # Note: We'll use UUID format as fallback since ULID generation in SQL is complex
        op.execute("""
            UPDATE anomaly_events 
            SET id = gen_random_uuid()::text 
            WHERE id IS NULL
        """)

        # Make id NOT NULL and set as primary key
        op.alter_column('anomaly_events', 'id', nullable=False)

        # Create index on id
        op.create_index(op.f('ix_anomaly_events_id'),
                        'anomaly_events', ['id'], unique=False)

        # Set as primary key (drop existing primary key if any)
        try:
            op.execute(
                "ALTER TABLE anomaly_events DROP CONSTRAINT IF EXISTS anomaly_events_pkey")
        except Exception:
            pass
        op.execute("ALTER TABLE anomaly_events ADD PRIMARY KEY (id)")


def downgrade() -> None:
    """Remove id column from anomaly_events table."""
    # Drop index first
    op.drop_index(op.f('ix_anomaly_events_id'), table_name='anomaly_events')
    # Drop primary key constraint
    op.execute(
        "ALTER TABLE anomaly_events DROP CONSTRAINT IF EXISTS anomaly_events_pkey")
    # Drop column
    op.drop_column('anomaly_events', 'id')
