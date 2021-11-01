from wiremock.constants import Config
from wiremock.client import *
from wiremock.server.server import WireMockServer
import requests


with WireMockServer() as wm:
    Config.instance().base_url = "http://localhost:{}/__admin".format(wm.port)
    Mappings.create_mapping(...)  # Set up stubs
    requests.get(...)  # Make API calls
