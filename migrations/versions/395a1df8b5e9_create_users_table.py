"""create users table

Revision ID: 395a1df8b5e9
Revises: 
Create Date: 2025-05-01 10:15:36.121539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers
revision = '395a1df8b5e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )




def downgrade():
    op.create_table('tb_user',
    sa.Column('id', mysql.INTEGER(display_width=10), autoincrement=True, nullable=False, comment='主键'),
    sa.Column('open_id', mysql.VARCHAR(length=200), nullable=True, comment='长期授权字符串'),
    sa.Column('nickname', mysql.VARCHAR(length=200), nullable=True, comment='昵称'),
    sa.Column('photo', mysql.VARCHAR(length=200), nullable=True, comment='头像网址'),
    sa.Column('name', mysql.VARCHAR(length=20), nullable=True, comment='姓名'),
    sa.Column('sex', mysql.ENUM('男', '女'), nullable=True, comment='性别'),
    sa.Column('tel', mysql.CHAR(length=11), nullable=True, comment='手机号码'),
    sa.Column('email', mysql.VARCHAR(length=200), nullable=True, comment='邮箱'),
    sa.Column('hiredate', sa.DATE(), nullable=True, comment='入职日期'),
    sa.Column('role', mysql.JSON(), nullable=True, comment='角色'),
    sa.Column('root', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True, comment='是否是超级管理员'),
    sa.Column('dept_id', mysql.INTEGER(display_width=10), autoincrement=False, nullable=True, comment='部门编号'),
    sa.Column('status', mysql.TINYINT(display_width=4), autoincrement=False, nullable=True, comment='状态'),
    sa.Column('create_time', mysql.DATETIME(), nullable=True, comment='创建时间'),
    sa.Column('loginid', mysql.VARCHAR(length=50), nullable=True, comment='账号'),
    sa.Column('password', mysql.VARCHAR(length=255), nullable=True, comment='密码'),
    sa.PrimaryKeyConstraint('id'),
    comment='tb用户表',
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_comment='tb用户表',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('users')
   
