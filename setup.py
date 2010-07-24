# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import django_data_render


setup(
    name='django-data-render',
    version=django_data_render.__version__,
    description='Render dict-like data, objects or Django models in simple unified way.',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='http://github.com/jqb/django-data-render',
    packages=find_packages('django_data_render'),
    package_dir={ '': 'django_data_render'},
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
