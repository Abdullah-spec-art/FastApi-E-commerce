"""add certification table

Revision ID: db90a5b3b321
Revises: 840da1f6257c
Create Date: 2025-01-31 20:51:12.229380

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db90a5b3b321'
down_revision: Union[str, None] = '840da1f6257c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Certifications',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('certification_type', sa.Enum('PRODUCT', 'SUPPLIER', 'MANUFACTURER', name='certificationtypeenum'), nullable=False),
    sa.Column('certification_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_Certifications_id'), 'Certifications', ['id'], unique=True)
    op.create_table('ProductCertifications',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('certification_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['certification_id'], ['Certifications.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['Products.id'], ),
    sa.PrimaryKeyConstraint('id', 'product_id', 'certification_id')
    )
    op.create_index(op.f('ix_ProductCertifications_id'), 'ProductCertifications', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ProductCertifications_id'), table_name='ProductCertifications')
    op.drop_table('ProductCertifications')
    op.drop_index(op.f('ix_Certifications_id'), table_name='Certifications')
    op.drop_table('Certifications')
    # ### end Alembic commands ###
