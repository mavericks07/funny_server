from random import randint
from . import v1
from app.api.v1.schemas import UserSchema, JokeSchema
from app.core.resources import Resource, MongoResource
from ...core.utils.buleprint import register_api


class UserAPI(Resource):

    schema = UserSchema()


class JokeAPI(MongoResource):
    schema = JokeSchema()

    def get_queryset(self, **kwargs):
        random_num = randint(0, 42000)
        queryset = self.schema.model.objects[random_num: random_num+5]
        return queryset

register_api(v1, UserAPI, 'user_api', '/users/', pk='pk')
register_api(v1, JokeAPI, 'joke_api', '/jokes/', pk='pk')
