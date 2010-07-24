# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django_data_render import render


class UserRender(render.Renderer):
    class Meta:
        model = User
        exclude = ('id', 'first_name')

    def get_actions(self, obj):
        return [1,2,3,4,5]

    username = render.FieldRenderer()
    actions = render.FieldRenderer(path='get_actions__4')



class UserRenderTwo(UserRender):
    def get_something(self, obj):
        return ['asd', 'asd', 'dfgg']

    something = render.FieldRenderer(path='get_something')
