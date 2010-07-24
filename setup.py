# -*- coding: utf-8 -*-
import os

from distutils.core import setup
import django_data_render



setup(
    name='django-data-render',
    version=django_data_render.__version__,
    description='Render dict-like data, objects or Django models in simple unified way.',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='http://github.com/jqb/django-data-render',
    packages=['django_data_render'],
    package_dir={'django_data_render': 'django_data_render'},
    package_data={'django_data_render': ['templates/data_render/*.html']},
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    )
