import unittest
from wiremock.constants import Config
from wiremock.server import WireMockServer


class MyTestClassBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wm = cls.wiremock_server = WireMockServer()
        wm.start()
        Config.base_url = "http://localhost:{}/__admin".format(wm.port)

    @classmethod
    def tearDownClass(cls):
        cls.wiremock_server.stop()
