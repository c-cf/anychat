"""Add is_verified to users

Revision ID: abc123456789
Revises: d31f15caf397
Create Date: 2025-03-23 12:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123456789'
down_revision = 'd31f15caf397'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default="0"))

def downgrade():
    op.drop_column('users', 'is_verified')