import responses

from wiremock.tests.base import BaseClientTestCase, attr
from wiremock.client import Mapping, MappingMeta, MappingRequest, MappingResponse, Mappings, AllMappings


class MappingsResourceTests(BaseClientTestCase):
    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_create_mapping(self):
        e = MappingResponse(body="test", status=200)
        resp = e.get_json_data()
        responses.add(responses.POST, "http://localhost/__admin/mappings", json=resp, status=200)

        m = Mapping(priority=1, request=MappingRequest(url="test", method="GET"), response=MappingResponse(status=200, body="test"))

        r = Mappings.create_mapping(m)
        self.assertIsInstance(r, MappingResponse)
        self.assertEquals(200, r.status)
        self.assertEquals("test", r.body)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_retrieve_all_mappings(self):
        e = AllMappings(mappings=[Mapping(id="1234-5678", priority=1), ], meta=MappingMeta(total=1))
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/mappings", json=resp, status=200)

        r = Mappings.retrieve_all_mappings()
        self.assertIsInstance(r, AllMappings)
        self.assertIsInstance(r.meta, MappingMeta)
        self.assertEquals(1, r.meta.total)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_retrieve_mapping(self):
        e = Mapping(id="1234-5678", priority=1)
        resp = e.get_json_data()
        responses.add(responses.GET, "http://localhost/__admin/mappings/1234-5678", json=resp, status=200)

        r = Mappings.retrieve_mapping(e)
        self.assertIsInstance(r, Mapping)
        self.assertEquals("1234-5678", r.id)
        self.assertEquals(1, r.priority)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_update_mapping(self):
        e = Mapping(id="1234-5678", priority=1)
        resp = e.get_json_data()
        responses.add(responses.PUT, "http://localhost/__admin/mappings/1234-5678", json=resp, status=200)

        r = Mappings.update_mapping(e)
        self.assertIsInstance(r, Mapping)
        self.assertEquals("1234-5678", r.id)
        self.assertEquals(1, r.priority)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_persist_mappings(self):
        responses.add(responses.POST, "http://localhost/__admin/mappings/save", body="", status=200)

        r = Mappings.persist_mappings()
        self.assertEquals(200, r.status_code)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_reset_mappings(self):
        responses.add(responses.POST, "http://localhost/__admin/mappings/reset", body="", status=200)

        r = Mappings.reset_mappings()
        self.assertEquals(200, r.status_code)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_delete_all_mappings(self):
        responses.add(responses.DELETE, "http://localhost/__admin/mappings", body="", status=200)

        r = Mappings.delete_all_mappings()
        self.assertEquals(200, r.status_code)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_delete_mapping(self):
        e = Mapping(id="1234-5678", priority=1)
        responses.add(responses.DELETE, "http://localhost/__admin/mappings/1234-5678", body="", status=200)

        r = Mappings.delete_mapping(e)
        self.assertEquals(200, r.status_code)

    @attr("unit", "mappings", "resource")
    @responses.activate
    def test_delete_mapping_by_metadata(self):
        responses.add(responses.POST, "http://localhost/__admin/mappings/remove-by-metadata", body='{}', status=200)

        r = Mappings.delete_mapping_by_metadata({
            "matchesJsonPath": {
                "expression": "$.some.key",
                "equalTo": "SomeValue"
            }
        })

        self.assertEquals(200, r.status_code)
