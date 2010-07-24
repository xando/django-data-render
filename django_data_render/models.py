# -*- coding: utf-8 -*-
from django.utils.datastructures import SortedDict
from fields import FieldRenderer, register



def fields_for_model(model, fields=None, exclude=None):
    result = SortedDict()
    opts = model._meta
    for f in opts.fields + opts.many_to_many:
        if (fields and not f.name in fields) or (exclude and f.name in exclude):
            continue
        result[f.name] = register.get(f)(name=f.name, verbose_name=f.verbose_name, path=f.name)
    return result



class RendererOptions(object):
    def __init__(self, options=None):
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.model = getattr(options, 'model', None)



class DeclarativeFieldsMetaclass(type):
    """
    Metaclass that converts Field attributes to a `base_columns` dictionary,
    taking into account parent class `base_columns` as well.
    """

    def __new__(cls, name, bases, attrs):
        # extract user defined fields
        fields = [(name, attrs.pop(name)) 
                  for name, obj in attrs.items() 
                  if isinstance(obj, FieldRenderer)]
        fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))


        # add fields from bases in proper order
        for base in bases[::-1]:
            if hasattr(base, 'base_fields'):
                fields = getattr(base, 'base_fields').items() + fields


        # setting the fields instances names, and converting fields do dict
        for name, field in fields:
            field.name = name
            if not field.path:
                field.path = name
        fields = SortedDict(fields)

        
        # getting meta attrinbutes
        opts = RendererOptions(attrs.get('Meta', None))


        # getting models defined attibutes and overiding them by those created by user
        if opts.model:
            declared_fields = fields_for_model(opts.model, opts.fields, opts.exclude)
            declared_fields.update(fields)
            fields = declared_fields


        attrs['base_fields'] = fields
        attrs['_meta'] = opts
        return type.__new__(cls, name, bases, attrs)
