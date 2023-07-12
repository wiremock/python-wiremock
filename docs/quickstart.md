Quick Start
===========

An example app:

```python
from wiremock.constants import Config
from wiremock.client import *

Config.base_url = 'https://mockserver.example.com/__admin/'
# Optionally set a custom cert path:
# Config.requests_cert = ... (See requests documentation)
# Optionally disable cert verification
# Config.requests_verify = False

mapping = Mapping(
    priority=100,
    request=MappingRequest(
        method=HttpMethods.GET,
        url='/hello'
    ),
    response=MappingResponse(
        status=200,
        body='hi'
    ),
    persistent=False,
)

mapping = Mappings.create_mapping(mapping=mapping)

all_mappings = Mappings.retrieve_all_mappings()
```

### Starting WireMock server with a context manager

```python
from wiremock.constants import Config
from wiremock.client import *
from wiremock.server.server import WireMockServer

with WireMockServer() as wm:
    Config.base_url = 'http://localhost:{}/__admin'.format(wm.port)
    Mappings.create_mapping(...)  # Set up stubs
    requests.get(...)             # Make API calls
```

### Starting WireMock server in a unittest.TestCase

```python

class MyTestClassBase(TestCase):
    @classmethod
    def setUpClass(cls):
        wm = self.wiremock_server = WireMockServer()
        wm.start()
        Config.base_url = 'http://localhost:{}/__admin'.format(wm.port)

    @classmethod
    def tearDownClass(cls):
        self.wiremock_server.stop()
```

### Customizing the path to java

```python
WireMockServer(java_path='/path/to/my/java')
```

### Customizing the WireMock server JAR file:

```python
WireMockServer(jar_path='/my/secret/location/wiremock-standalone-2.35.0.jar')
```
