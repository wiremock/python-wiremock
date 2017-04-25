import sys
from setuptools import setup, find_packages

#next time:
#python setup.py register
#python setup.py sdist upload

version = open('wiremock/VERSION', 'r').readline().strip()
develop_requires = [
    'Sphinx==1.5.3',
    'coverage==4.3.4',
    'detox==0.10.0',
    'mock==2.0.0',
    'nose==1.3.7',
    'python-coveralls==2.9.0',
    'responses==0.5.1',
    'requests==2.13.0',
    'six>=1.10.0',
    'sphinx-rtd-theme==0.2.4',
    'tox==2.6.0',
    'watchdog==0.8.3',
    'wheel>=0.24.0']

long_desc = """
wiremock is an API Client to the Admin API for WireMock Standalone installation: https://wiremock.org/docs

`Documentation <https://wiremock.readthedocs.org/en/latest/>`_

`Report a Bug <https://bitbucket.org/wellaware/python_wiremock/issues>`_
"""

setup(
    name='wiremock',
    version=version,
    description='Wiremock Admin API Client',
    dependency_links=['https://bitbucket.org/wellaware/python_wiremock/archive/{0}.tar.gz#egg=wiremock-{0}'.format(version)],
    long_description=long_desc,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Other Environment",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='wiremock',
    install_requires=[
        'setuptools>=35.0.1',
        'six>=1.10.0',
        'requests==2.13.0'
    ],
    extras_require={
        'develop': develop_requires,
        'docs': ['Sphinx>=1.5.3', 'sphinx-rtd-theme>=0.2.4', 'watchdog>=0.8.3'],
    },
    test_suite='nose.collector',
    tests_require=develop_requires,
    author='Cody Lee',
    author_email='codylee@wellaware.us',
    maintainer='Cody Lee',
    maintainer_email='codylee@wellaware.us',
    url='https://bitbucket.org/wellaware/python_wiremock',
    license='Apache Software License 2.0',
    packages=find_packages(),
    include_package_data=True,
)
