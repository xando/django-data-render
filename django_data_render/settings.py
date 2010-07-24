from django.conf import settings as django_settings



data_render_settings = getattr(django_settings, 'DATA_RENDER_SETTINGS', {})


DEFAULT_FIELD_CONTEXT = data_render_settings.get('DEFAULT_FIELD_CONTEXT', {
        'label_class' : 'field',
        })
PATH_SEPARATOR = data_render_settings.get('PATH_SEPARATOR', '__')
DEFAULT_DATE_FORMAT = data_render_settings.get('DEFAULT_DATE_FORMAT', '%Y-%m-%d')
DEFAULT_DATETIME_FORMAT = data_render_settings.get('DEFAULT_DATETIME_FORMAT', '%Y-%m-%d %H:%M')
