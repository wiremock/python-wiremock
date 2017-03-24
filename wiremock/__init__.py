import os

__wiremock_version_path__ = os.path.realpath(__file__ + '/../VERSION')
__version__ = open(__wiremock_version_path__, 'r').readline().strip()
