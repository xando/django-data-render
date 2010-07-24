# -*- coding: utf-8 -*-
"""
Path dispatcher v0.1

Path chain dispatcher. A 'protocol' for chain-call dispatching.
It's created to make the data access easy and flexible from the given string path.
Makes no difference if there is a attribute, dict or method.


# example:

# suppose we've got following model...
# models.py
class Cost(models.Model):
    currency = models.CharField(max_length=3)
    value = models.FloatField()

    def to_dict(self):
        return {
           'currency' : self.currency,
           'value' : self.value,
        }


# ...and somewere in the code
data = {
   'username' : 'jacob',
   'cost' : Cost(currency='EUR', value=123.32)
   'variables' : {
      'a' : 123,
      'b' : [1,2,3,4]
   }
}


# Now we can do the magic:
path_dispatcher = PathDispatcher(data, separator='__') # default separator
assert path_dispatcher['username'] == 'jacob'
assert path_dispatcher['cost__currency'] == 'EUR'
assert path_dispatcher['cost__value'] == 123.32
assert path_dispatcher['cost__to_dict__currency'] == 'EUR'
assert path_dispatcher['cost__to_dict__value'] == 123.32
assert path_dispatcher['variables__a'] == 123
assert path_dispatcher['variables__b__2'] == 3


# optionaly you can pass 'object_proccesor' (object with
# method which takes `data` object as param and transforms it somehow.
# There is one restrictions to object_proccesor's:
# it work's only if the *first* bit of path that matches method name.


# example
class DataProccesor:
   def get_very_complicated_staff(self, data):
       # do the things
       return 'it_works!'

path_dispatcher = PathDispatcher(data, object_proccesor=DataProccesor())
assert path_dispatcher['get_very_complicated_staff'] == 'it_works!'


# but this will raise an ValueError
value = path_dispatcher['username__get_very_complicated_staff']
"""
import re
from django.utils.datastructures import SortedDict

from django_data_render.settings import PATH_SEPARATOR


# utility functions
is_int = re.compile(r'\d+').match
call_if_callable = lambda obj: obj if not callable(obj) else obj()



def attribute(current=None, bit=None):
    if hasattr(current, bit):
        return True, call_if_callable(getattr(current, bit))
    return False, current



def getitem_string(current=None, bit=None):
    if hasattr(current, '__getitem__') and bit in current:
        return True, call_if_callable(current[bit])
    return False, current



def getitem_int(current=None, bit=None):
    if hasattr(current, '__getitem__') and is_int(bit):
        return True, call_if_callable(current[int(bit)])
    return False, current



dispatchers = SortedDict([
        (attribute.__name__, attribute),
        (getitem_string.__name__, getitem_string),
        (getitem_int.__name__, getitem_int),
        ])



class PathDispatcher(object):
    def __init__(self, data, object_proccesor=None, separator=None, dispatchers=dispatchers):
        self.data = data
        self.object_proccesor = object_proccesor
        self.separator = separator
        self.dispatchers = dispatchers
        self.separator = separator if separator else PATH_SEPARATOR


    def __getitem__(self, path):
        current = self.data        
        splited_path = path.split(self.separator)

        # first check for method in object_proccesor ...
        object_proccesor_method_name_candidate = splited_path[0]
        if hasattr(self.object_proccesor, object_proccesor_method_name_candidate):
            return getattr(self.object_proccesor, object_proccesor_method_name_candidate)(current)

        # ... if it fails try other dispatcher functions
        success = False
        for bit in splited_path:
            for dispatcher in self.dispatchers.values():
                success, current = dispatcher(current, bit)
                if success:
                    break

            if not success:
                raise ValueError(
                    "PathDispatcher ERROR. Could not resolve '%s' from '%s'. " % (bit, path) + 
                    "Used separator: '%s'." % self.separator)

            # important that we break in None case, or a relationship
            # spanning across a null-key will raise an exception in the
            # next iteration, instead of defaulting.
            if current is None:
                break

        return current
