import datetime
import uuid
import peewee
from playhouse.flask_utils import FlaskDB
from playhouse.db_url import connect
from mongoengine import fields
from .utils.mongodb import mongo

db = connect('mysql+pool://root:qw010203@127.0.0.1/flask_test?max_connections=100&stale_timeout=300')
db_wrapper = FlaskDB()


class BaseModel(db_wrapper.Model):
    id = peewee.UUIDField(primary_key=True, default=uuid.uuid4)
    create_time = peewee.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    modify_time = peewee.DateTimeField(default=datetime.datetime.now, verbose_name="修改时间")
    is_del = peewee.BooleanField(default=False, verbose_name='是否删除', null=True)

    common_fields = ("id", "create_time", "modify_time")

    # def save(self, *args, **kwargs):
    #     self.modify_time = datetime.datetime.now()
    #     return super(BaseModel, self).save(*args, **kwargs)

    # class Meta:
    #     database = db


class MongoBaseModel(mongo.Document):
    _id = fields.ObjectIdField()

    common_fields = ("_id",)


if __name__ == '__main__':
    db.connect()
    db.create_table(BaseModel)
