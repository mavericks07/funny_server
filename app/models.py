import peewee
from mongoengine import fields
from app.core.models import BaseModel
from app.core.utils.mongodb import mongo


class User(BaseModel):
    username = peewee.CharField(max_length=32)

    common_fields = BaseModel.common_fields + ('username',)


class Joke(mongo.Document):

    _id = fields.ObjectIdField()
    content = fields.StringField()
    from_url = fields.StringField()

    common_fields = ('_id', 'content')
