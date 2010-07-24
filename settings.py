import os 
PROJECT_ROOT = os.path.dirname(__file__)
BASE_URL = '/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_URL = '/'.join((BASE_URL, 'static')) + '/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('kuba.janoszek', 'kuba.janoszek@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
    }

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+x&(yo6og$2yn)byx274l(ej31ae5%kt@oi**du6f$0r7wqq9y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'django-model-render.urls'
TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'django_data_render',
    'examples',
    )
