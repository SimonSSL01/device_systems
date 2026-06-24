"""add hashed_password and role to users

Revision ID: 734e77817669  # Cambia por el ID real que se generó
Revises: abc123def456      # Cambia por el ID de la migración anterior
Create Date: 2026-06-24 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '734e77817669'          # Cambia por el ID real
down_revision: Union[str, None] = 'abc123def456'  # ID de la migración anterior
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Agregar columna hashed_password
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
    # Agregar columna role con valor por defecto 'user'
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))

def downgrade() -> None:
    op.drop_column('users', 'role')
    op.drop_column('users', 'hashed_password')