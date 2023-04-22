import pytest
from requests import Response

from wiremock.exceptions import UnexpectedResponseException


# Helpers
def create_dummy_response(status_code=200):
    resp = Response()
    resp.status_code = status_code
    return resp


def test_handle_response(client):
    for status_code in [200, 201, 204]:
        resp = create_dummy_response(status_code)
        returned = client.handle_response(resp)
        assert returned == resp

    resp = create_dummy_response(203)
    with pytest.raises(UnexpectedResponseException):
        client.handle_response(resp)
