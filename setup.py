import sys
from setuptools import setup, find_packages

#next time:
#python setup.py register
#python setup.py sdist upload

version = open('wiremock/VERSION', 'r').readline().strip()
develop_requires = [
    'Sphinx~=2.4.3',
    'black~=19.10b0',
    'coverage~=5.0.3',
    'detox~=0.19',
    'mock~=4.0.1',
    'nose~=1.3.7',
    'python-coveralls~=2.9.3',
    'responses~=0.10.9',
    'requests~=2.23.0',
    'sphinx-rtd-theme~=0.4.3',
    'tox~=3.14.0',
    'watchdog~=0.10.2',
    'wheel>=0.34.2']

long_desc = """
wiremock is an API Client to the Admin API for WireMock Standalone installation: https://wiremock.org/docs

`Documentation <https://wiremock.readthedocs.org/en/latest/>`_

`Report a Bug <https://github.com/platinummonkey/python-wiremock/issues>`_
"""

setup(
    name='wiremock',
    version=version,
    description='Wiremock Admin API Client',
    dependency_links=['https://github.com/platinummonkey/python-wiremock/archive/{0}.tar.gz#egg=wiremock-{0}'.format(version)],
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='wiremock',
    install_requires=[
        'setuptools>=45.2.0',
        'requests>=2.20.0'
    ],
    extras_require={
        'develop': develop_requires,
        'docs': ['Sphinx>=2.4.3', 'sphinx-rtd-theme>=0.4.3', 'watchdog>=0.10.2'],
    },
    test_suite='nose.collector',
    tests_require=develop_requires,
    author='Cody Lee',
    author_email='cody.lee@datadoghq.com',
    maintainer='Cody Lee',
    maintainer_email='cody.lee@datadoghq.com',
    url='https://github.com/platinummonkey/python-wiremock',
    license='Apache Software License 2.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
)
