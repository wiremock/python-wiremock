import pytest
import responses

from wiremock.client import (
    AllMappings,
    Mapping,
    MappingMeta,
    MappingRequest,
    MappingResponse,
    Mappings,
)


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_create_mapping():
    e = MappingResponse(body="test", status=200)
    resp = e.get_json_data()
    responses.add(
        responses.POST, "http://localhost/__admin/mappings", json=resp, status=200
    )

    m = Mapping(
        priority=1,
        request=MappingRequest(url="test", method="GET"),
        response=MappingResponse(status=200, body="test"),
    )

    r = Mappings.create_mapping(m)
    assert isinstance(r, MappingResponse)
    assert r.status == 200
    assert r.body == "test"


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_retrieve_all_mappings():
    e = AllMappings(
        mappings=[
            Mapping(id="1234-5678", priority=1),
        ],
        meta=MappingMeta(total=1),
    )
    resp = e.get_json_data()
    responses.add(
        responses.GET,
        "http://localhost/__admin/mappings",
        json=resp,
        status=200,
    )

    r = Mappings.retrieve_all_mappings()
    assert isinstance(r, AllMappings)
    assert isinstance(r.meta, MappingMeta)
    assert 1 == r.meta.total


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_retrieve_mapping():
    e = Mapping(id="1234-5678", priority=1)
    resp = e.get_json_data()
    responses.add(
        responses.GET,
        "http://localhost/__admin/mappings/1234-5678",
        json=resp,
        status=200,
    )

    r = Mappings.retrieve_mapping(e)
    assert isinstance(r, Mapping)
    assert "1234-5678" == r.id
    assert 1 == r.priority


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_update_mapping():
    e = Mapping(id="1234-5678", priority=1)
    resp = e.get_json_data()
    responses.add(
        responses.PUT,
        "http://localhost/__admin/mappings/1234-5678",
        json=resp,
        status=200,
    )

    r = Mappings.update_mapping(e)
    assert isinstance(r, Mapping)
    assert "1234-5678" == r.id
    assert 1 == r.priority


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_persist_mappings():
    responses.add(
        responses.POST,
        "http://localhost/__admin/mappings/save",
        body="",
        status=200,
    )

    r = Mappings.persist_mappings()
    assert r.status_code == 200


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_reset_mappings():
    responses.add(
        responses.POST,
        "http://localhost/__admin/mappings/reset",
        body="",
        status=200,
    )

    r = Mappings.reset_mappings()
    assert r.status_code == 200


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_delete_all_mappings():
    responses.add(
        responses.DELETE,
        "http://localhost/__admin/mappings",
        body="",
        status=200,
    )

    r = Mappings.delete_all_mappings()
    assert r.status_code == 200


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_delete_mapping():
    e = Mapping(id="1234-5678", priority=1)
    responses.add(
        responses.DELETE,
        "http://localhost/__admin/mappings/1234-5678",
        body="",
        status=200,
    )

    r = Mappings.delete_mapping(e)
    assert r.status_code == 200


@pytest.mark.unit
@pytest.mark.mappings
@pytest.mark.resource
@responses.activate
def test_delete_mapping_by_metadata():
    responses.add(
        responses.POST,
        "http://localhost/__admin/mappings/remove-by-metadata",
        body="{}",
        status=200,
    )

    r = Mappings.delete_mapping_by_metadata(
        {
            "matchesJsonPath": {
                "expression": "$.some.key",
                "equalTo": "SomeValue",
            },
        }
    )

    assert r.status_code == 200
