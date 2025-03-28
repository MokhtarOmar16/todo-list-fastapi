"""initial

Revision ID: 56e4cbcd071d
Revises: b2af3fb4b3ff
Create Date: 2025-03-28 07:11:16.473303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56e4cbcd071d'
down_revision: Union[str, None] = 'b2af3fb4b3ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mission', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_todo_description'), ['description'], unique=False)
        batch_op.create_index(batch_op.f('ix_todo_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_todo_mission'), ['mission'], unique=False)
        batch_op.create_index(batch_op.f('ix_todo_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_todo_user_id'))
        batch_op.drop_index(batch_op.f('ix_todo_mission'))
        batch_op.drop_index(batch_op.f('ix_todo_id'))
        batch_op.drop_index(batch_op.f('ix_todo_description'))

    op.drop_table('todo')
    # ### end Alembic commands ###
