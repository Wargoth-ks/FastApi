"""confirmed_email

Revision ID: b4e562675005
Revises: e0ed7dbf5d4c
Create Date: 2023-11-02 16:30:39.379963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4e562675005"
down_revision: Union[str, None] = "e0ed7dbf5d4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("confirmed", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "confirmed")
    # ### end Alembic commands ###
