.. _quickstart:

Quick Start
===========

An example app:

.. literalinclude:: quickstart.py
    :language: python
    :linenos:

An example of starting WireMock server with a context manager:

.. literalinclude:: server_cm.py
    :language: python
    :linenos:


An example of starting WireMock server in a unittest.TestCase:

.. literalinclude:: server_ut.py
    :language: python
    :linenos:

Customizing the path to java:

    WireMockServer(java_path='/path/to/my/java')

Customizing the WireMock server JAR file:

    WireMockServer(jar_path='/my/secret/location/wiremock-standalone-2.0.0.jar')


