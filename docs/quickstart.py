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
