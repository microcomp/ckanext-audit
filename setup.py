from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-audit',
    version=version,
    description="extend revision with actor and sends messages to auditlog",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Dominik Kapisinsky',
    author_email='kapisinsky@microcomp.sk',
    url='http://github.com/microcomp',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.audit'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        audit=ckanext.audit.plugin:AuditPlugin  
        [paste.paster_command]
        audit-cmd = ckanext.audit.audit_cmd:AuditCmd
        [ckan.celery_task]
        tasks = ckanext.audit.celery_import:task_imports
    ''',
)
