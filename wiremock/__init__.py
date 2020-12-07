import os

__wiremock_version_path__ = os.path.realpath(__file__ + '/../VERSION')
with open(__wiremock_version_path__, 'r') as f:
    __version__ = f.readline().strip()
