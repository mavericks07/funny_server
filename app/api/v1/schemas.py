from marshmallow import fields, validates, ValidationError
from app.core.schemas import BaseSchema, MongoBaseSchema
from app.models import User, Joke


class UserSchema(BaseSchema):

    model = User

    username = fields.String(required=True, error_messages={'required': '用户名是必填项'})

    @validates('username')
    def validate_username(self, value):
        users = self.model.filter(username=value)
        if users.exists():
            raise ValidationError('该用户名已存在')

    class Meta:
        fields = User.common_fields


class JokeSchema(MongoBaseSchema):
    model = Joke
    content = fields.String(required=True, error_messages={'required': '内容是必填'})

    class Meta:
        fields = Joke.common_fields
