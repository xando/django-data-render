django-data-render
==================

Render dict-like data, objects or Django models in simple unified way.
NOTE it's just development version, it's not tested enough.


Installation
------------
Download whole package and install it:
python setup.py install

Add django_data_render to your INSTALLED_APPS.



Basic usage
-----------
The basic idea was to make it look much like a django form::

  # render.py
  from django_data_render import render

  class MyDataRenderer(render.Renderer):
      name = render.FieldRenderer(verbose_name='My data name')
      group = render.FieldRenderer(path='group__name')

      # currently you can also use render.DateRenderer or render.DateTimeRenderer
      # for dates which takes additional 'format' argument with date format.
      # see also docs below and docs in fields.py and settings.py


  # in views.py:
  def my_view(request):
      ...
      return render_to_response('my_fancy_template.html', {
              'renderer' : MyDataRenderer({
                      'name': 'jacob',
                      'group': {'name' : 'users'}
                      })
              })

  # If we have model, like:
  # class MyModel(models.Model):
  #    name = models.CharField()
  #    group = models.ForeignKey('SomeGroupModel')
  # it will also work in the same way:

  def my_view(request):
      obj = MyModel.objects.get(id=1)
      return render_to_response('my_fancy_template.html', {
              'renderer' : MyDataRenderer(obj)
              })


  
  # and in templates:
  {% for field in renderer %}
  {{ field }}     <-- the template 'data_render/field.html' is used.
  {% endfor %}


  {% for field in renderer.fields %}
  {{ field }}     <-- the template 'data_render/field.html' is used.
  {% endfor %}


  {{ renderer.fields.name.label }}  <-- no template is used
  {{ renderer.fields.name.value }}
  {{ renderer.fields.name }}        <-- the template 'data_render/field.html' is used.
  {{ renderer.fields.group }}


  {{ renderer }} <-- the template 'data_render/object.html' is used.

  
Ofcourse you can overide existing templates.



Meta attribute
--------------
  as it is in django forms, there is ability to generate fields from the model
  (look to ``django_data_render.fields`` file docs)::

  # models.py
  class MyModel(models.Model):
     name = models.CharField()
     group = models.ForeignKey('SomeGroupModel')



  # render.py
  from django_data_render import render

  class MyRenderer(render.Renderer):
      class Meta:
          model = MyModel
	  # exclude and fields are also supported

Fields are generated automagically, even ``verbose_name`` is taken from the model's ``verbose_name``.



Methods on renderer
-------------------
  there is ability to write methods on renderer objects
  (note that to invoke the method it HAVE TO BE defined *first* on the path)::

  # render.py
  class MyRenderer(render.Renderer):
      class Meta:
          model = MyModel

    def get_some_really_heavy_stuff(self, mymodel_obj):
        # do the things here
        return whatever_you_want

    heavy_data = render.FieldRenderer(path='get_some_really_heavy_stuff')



Application settings
--------------------
  There are number of default's which you can change directly, or via main settings.py eg::


  # somewere in your code:
  from django_data_render import settings

  settings.DEFAULT_FIELD_CONTEXT = {
    'label_class' : 'my-default-field-css',
  }



  # or in main setting.py:
  DATA_RENDER_SETTINGS = {
     'PATH_SEPARATOR' : '__',
     # ... and others options, see django_data_render.settings file
  }



TODO
----

1) Add tests!
2) Docs for django_data_render.render file is mising.
3) Add templatetags (context proccesor will be needed)::

  {% load data_render_tags %}
  {% render object using data_render.RendererClass %}
