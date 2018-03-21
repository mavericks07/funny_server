from collections import OrderedDict
from flask import request
from playhouse.flask_utils import PaginatedQuery, get_current_url, get_next_url
from marshmallow import Schema
from flask_mongoengine import QuerySet, Pagination


class NormalPagination(object):

    def __init__(self, page_queryset: PaginatedQuery, schema: Schema):
        self.page = page_queryset.get_page()
        self.count = page_queryset.query.count()
        self.page_nums = page_queryset.get_page_count()
        self.data = schema.dump(obj=page_queryset.get_object_list(), many=True).data
        self.result = OrderedDict([
            ('count', self.count),
            ('page_nums', self.page_nums),
            ('next', self.get_next_url()),
            ('previous', self.get_previous_url()),
            ('results', self.data)
        ])

    def has_next(self):
        return self.page < self.page_nums

    def has_previous(self):
        return self.page > 1

    def get_next_url(self):
        if self.has_next():
            return f'{request.base_url}?page={self.page+1}'
        return None

    def get_previous_url(self):
        if self.has_previous():
            return f'{request.base_url}?page={self.page-1}'
        return None


class MongoPagination(object):

    def __init__(self, page_queryset: QuerySet, schema: Schema):
        self.page = page_queryset()
        self.count = page_queryset.query.count()
        self.page_nums = page_queryset.pages()
        self.data = schema.dump(obj=page_queryset.get_object_list(), many=True).data
        self.result = OrderedDict([
            ('count', self.count),
            ('page_nums', self.page_nums),
            ('next', self.get_next_url()),
            ('previous', self.get_previous_url()),
            ('results', self.data)
        ])

    def has_next(self):
        return self.page < self.page_nums

    def has_previous(self):
        return self.page > 1

    def get_next_url(self):
        if self.has_next():
            return f'{request.base_url}?page={self.page+1}'
        return None

    def get_previous_url(self):
        if self.has_previous():
            return f'{request.base_url}?page={self.page-1}'
        return None