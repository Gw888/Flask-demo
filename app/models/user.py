from app import db
from datetime import datetime

class User(db.Model):
    """
    用户表模型（Model）
    继承自 db.Model，代表数据库中的一张表
    """
    __tablename__ = 'users'  # 表名
    
    id = db.Column(db.Integer, primary_key=True)  # 主键，自增
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一
    email = db.Column(db.String(120), unique=True, nullable=False)    # 邮箱，唯一
    password = db.Column(db.String(255), nullable=False)              # 密码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)      # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def __repr__(self):
        return f'<User {self.username}>' 