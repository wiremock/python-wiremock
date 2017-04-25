with WireMockServer() as wm:
    Config.base_url = 'http://localhost:{}/__admin'.format(wm.port)
    Mappings.create_mapping(...)  # Set up stubs
    requests.get(...)             # Make API calls
