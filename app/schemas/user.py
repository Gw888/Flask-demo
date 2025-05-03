from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    """
    用户序列化类（Schema）
    用于把数据库对象转成JSON，或反过来
    """
    class Meta:
        model = User
    
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True) 