from bson import ObjectId
from marshmallow import Schema, validates, ValidationError, fields, post_load
from app.core.models import BaseModel, MongoBaseModel


class BaseSchema(Schema):
    model = BaseModel

    id = fields.UUID(dump_only=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    modify_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)

    class Meta:
        fields = BaseModel.common_fields

    """
    改变load之后的返回值为model类型
    """
    @post_load
    def base_load(self, data):
        return self.model(**data)


Schema.TYPE_MAPPING[ObjectId] = fields.String


class MongoBaseSchema(Schema):
    model = MongoBaseModel

    _id = fields.String(dump_only=True)

    class Meta:
        fields = ('_id',)

    @post_load
    def base_load(self, data):
        return self.model(**data)
