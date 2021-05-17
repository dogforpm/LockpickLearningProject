"""empty message

Revision ID: 80ed85ca5aca
Revises: 20246068648c
Create Date: 2021-05-17 16:37:59.984105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80ed85ca5aca'
down_revision = '20246068648c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.add_column('question', sa.Column('QuestionNumber', sa.Integer(), nullable=True))
    op.add_column('question', sa.Column('lesson_id', sa.Integer(), nullable=True))
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.create_foreign_key(None, 'question', 'lesson', ['lesson_id'], ['id'])
    op.drop_column('question', 'test_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('test_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.create_foreign_key(None, 'question', 'test', ['test_id'], ['id'])
    op.drop_column('question', 'lesson_id')
    op.drop_column('question', 'QuestionNumber')
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('LessonNum', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Completed', sa.BOOLEAN(), nullable=True),
    sa.Column('lesson_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
