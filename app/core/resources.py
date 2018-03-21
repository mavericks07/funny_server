import datetime
from flask import request, jsonify, abort
from flask.views import MethodView
from playhouse.flask_utils import PaginatedQuery
from app.core.schemas import BaseSchema, MongoBaseSchema
from app.core.utils.pagination import NormalPagination


class BaseResource(MethodView):

    schema = None
    filter_fields = ()
    search_fields = ()
    page_size = 10

    def get_filter_get_method_parm(self):
        """
        过滤get方法的查询字段
        """
        url_parm = request.args.to_dict()
        cleaned_parm = {k: v for k, v in url_parm.items() if k in self.filter_fields}
        return cleaned_parm


class Resource(BaseResource):

    schema = BaseSchema()
    filter_fields = ('username',)
    search_fields = ()
    page_size = 10

    def post(self):
        request_data = request.get_json()
        obj, errors = self.schema.load(request_data)
        if errors:
            return errors
        obj.save(force_insert=True)
        serializer = self.schema.dump(obj)
        return serializer.data, 201

    def get(self, pk):
        if pk:
            obj = self.get_object(pk)
            serializer = self.schema.dump(obj)
            return serializer.data
        parm = self.get_filter_get_method_parm()
        queryset = self.get_queryset(**parm)
        page_queryset = PaginatedQuery(queryset, self.page_size)
        serializers = NormalPagination(page_queryset, self.schema).result
        return serializers

    def put(self, pk):
        pass

    def patch(self, pk):
        pass

    def delete(self, pk):
        pass

    def get_queryset(self, **kwargs):
        queryset = self.schema.model.select()
        if kwargs:
            queryset = queryset.filter(**kwargs)
        return queryset

    def get_object(self, pk):
        try:
            obj = self.schema.model.get(self.schema.model.id == pk)
            return obj
        except self.schema.model.DoesNotExist:
            abort(404)


class MongoResource(BaseResource):

    schema = MongoBaseSchema()
    filter_fields = ()
    search_fields = ()
    page_size = 10

    def post(self):
        request_data = request.get_json()
        obj, errors = self.schema.load(request_data)
        if errors:
            return errors
        obj.save(force_insert=True)
        serializer = self.schema.dump(obj)
        return serializer.data, 201

    def get(self, pk):
        if pk:
            obj = self.get_object(pk)
            serializer = self.schema.dump(obj)
            return serializer.data
        parm = self.get_filter_get_method_parm()
        queryset = self.get_queryset(**parm)
        # page_queryset = PaginatedQuery(queryset, self.page_size)
        serializers = self.schema.dump(queryset, many=True).data
        print(queryset)
        return serializers

    def put(self, pk):
        pass

    def patch(self, pk):
        pass

    def delete(self, pk):
        pass

    def get_queryset(self, **kwargs):
        queryset = self.schema.model.objects
        if kwargs:
            queryset = queryset.objects(**kwargs)
        return queryset

    def get_object(self, pk):
        try:
            obj = self.schema.model.get(self.schema.model.id == pk)
            return obj
        except self.schema.model.DoesNotExist:
            abort(404)