
class MyTestClassBase(TestCase):
    @classmethod
    def setUpClass(cls):
        wm = self.wiremock_server = WireMockServer()
        wm.start()
        Config.base_url = 'http://localhost:{}/__admin'.format(wm.port)

    @classmethod
    def tearDownClass(cls):
        self.wiremock_server.stop()


