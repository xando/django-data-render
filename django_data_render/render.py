# -*- coding: utf-8 -*-
from django.utils.encoding import StrAndUnicode
from django.template.loader import render_to_string

from django_data_render.models import DeclarativeFieldsMetaclass
from django_data_render.fields import FieldRenderer
from django_data_render.path_dispatcher import PathDispatcher
from django_data_render import utils



class BoundField(StrAndUnicode):
    def __init__(self, dispatcher, field):
        self._field = field
        self._dispather = dispatcher

    name = property(lambda s: s._field.name)
    label = property(lambda s: s._field.get_verbose_name())
    value = property(lambda s: s._field.procces_value(s._dispather[s._field.path]))
    context = property(lambda s: s._field.get_context())

    def __unicode__(self):
        return render_to_string(self._field.template_name, {
                'field' : self,
                })



class BoundFieldsSet(object):
    def __init__(self, renderer):
        self._renderer = renderer
        self._dispather = PathDispatcher(renderer._data, object_proccesor=renderer)
        for name in self._renderer.base_fields:
            setattr(self, name, BoundField(self._dispather, self._renderer.base_fields[name]))

    def __iter__(self):
        for name in self._renderer.base_fields:
            yield BoundField(self._dispather, self._renderer.base_fields[name])



class Renderer(StrAndUnicode):
    """
    Abstraction object over single object or dict.
    """
    __metaclass__ = DeclarativeFieldsMetaclass

    
    def __init__(self, data_object, template_name='data_render/object.html', extra_context=None):
        self._data = data_object
        self._fields = None
        self._template_name = template_name
        self._extra_context = extra_context


    def _get_fields(self):
        if not self._fields:
            self._fields = BoundFieldsSet(self)
        return self._fields
    fields = property(_get_fields)


    context = property(lambda s: utils.eval_dict(s._extra_context))


    def clear(self):
        self._fields = None


    def __iter__(self):
        return iter(self.fields)


    def __len__(self):
        return len(self.base_fields)


    def __unicode__(self):
        return render_to_string(self._template_name, {
                'renderer' : self,
                })
