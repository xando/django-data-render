# -*- coding: utf-8 -*-
"""
Field renderers subsystem.

Field renderer is responsible for:
* keeping meta information of the field (all are optional)
  - `verbose_name` 
     it is used later as field label
  - `default`
     default value (None by default)
  - `path` 
     path to the object we are interested to eg. user__username setted up to `name` by default
     (look to the 'path_dispatcher' docs for more information about it, for example how the separator can be changed)
  - `name`
     don't use it and don't change it. It is used internally and actually you're setting it up by
     giving the field name in your Rederer definition
  - `template_name`
     the template which is used to render the field, 'data_renderer/field.html' by default
  - `extra_context`
     this is if you want to add some extra context information to the field template.
     Before you use it in the template it is evaluated (if some valued are callable they
     are called before you get it in the template)

* simple proccesing value before it is available in template
  things are done in `procces_value` method. By default it just returs the value
  or `default` if `value` is None.

* have some other methods which are used internally



There are three field renderers currenty:
* DateRenderer, DateTimeRenderer - for date and datetime fields,
  it uses one additional param:
  - `format`
     format is used in `procces_value` method for proper date(time) formating

* FieldRenderer - used for everythig else


The last important thing is `register`.
* it basically just maps 'django.db.models' fields to appropriate FieldRenderer subclass.
* by default it returs FieldRenderer class for everything except DateField and DateTimeField.
* you can replace (or create) existing mapping with you're own solutions eg:
  ==============================================
  from django_data_render.fields import register
  from django.db import models

  register.set(models.DateTimeField, MyOwnDateTimeRenderer)
  register.set(models.BooleanField, MyOwnBooleanRenderer)
  ==============================================

  MyOwnDateTimeRenderer and MyOwnBooleanRenderer should subclass FieldRenderer.
"""
from django.db import models
from django_data_render import settings
from django_data_render import utils



class FieldRenderer(object):
    creation_counter = 0

    def __init__(self, verbose_name=None, default=None, path=None, name=None,
                 template_name='data_render/field.html',
                 extra_context=None):
        self.verbose_name = verbose_name
        self.name = name
        self.default = default
        self.path = path if path else name
        self.template_name = template_name
        self.extra_context = extra_context

        self.creation_counter = self.__class__.creation_counter
        self.__class__.creation_counter += 1


    def procces_value(self, value):
        if not value and self.default:
            return self.default
        return value

        
    def get_verbose_name(self):
        if self.verbose_name and callable(self.verbose_name):
            return self.verbose_name()
        result = self.name if not self.verbose_name else self.verbose_name
        return result.capitalize()


    def get_context(self):
        return utils.eval_dict(self.extra_context)



class BaseDateRenderer(FieldRenderer):
    def procces_value(self, value):
        if value:
            return value.strftime(self.format)
        return self.default
    


class DateRenderer(BaseDateRenderer):
    def __init__(self, *a, **kw):
        self.format = kw.pop('format', settings.DEFAULT_DATE_FORMAT)
        BaseDateRenderer.__init__(self, *a, **kw)



class DateTimeRenderer(BaseDateRenderer):
    def __init__(self, *a, **kw):
        self.format = kw.pop('format', settings.DEFAULT_DATETIME_FORMAT)
        BaseDateRenderer.__init__(self, *a, **kw)



class FieldRegister(object):
    def __init__(self):
        self._data = {}
        
    def set(self, db_field, renderer_field):
        self._data[db_field.__name__] = renderer_field

    def get(self, db_field):
        return self._data.get(db_field.__class__.__name__, FieldRenderer)



register = FieldRegister()
register.set(models.DateField, DateRenderer)
register.set(models.DateTimeField, DateTimeRenderer)
