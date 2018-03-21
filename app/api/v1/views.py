from . import v1
from app.api.v1.schemas import UserSchema, JokeSchema
from app.core.resources import Resource, MongoResource
from ...core.utils.buleprint import register_api


class UserAPI(Resource):

    schema = UserSchema()


class JokeAPI(MongoResource):
    schema = JokeSchema()

    def get(self, pk):
        return super(JokeAPI, self).get(pk)

register_api(v1, UserAPI, 'user_api', '/users/', pk='pk')
register_api(v1, JokeAPI, 'joke_api', '/jokes/', pk='pk')
