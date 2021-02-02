# pylint: disable-msg=C0116

from os import remove

import pickledb
from jsonschema import validate, exceptions
from chest import create_app


class TestRouts:
    def setup_class(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client()

    def setup(self):
        self.client.post('/dictionary', json={"key": "test", "value": "data"})

    def teardown(self):
        pickledb.load(self.app.config['DATABASE'], True).deldb()

    def teardown_class(self):
        remove(self.app.config['DATABASE'])

    # helper
    def helper_validate_response_json(self, json):
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "type": "object",
            "properties": {
                "result": {
                    "type": "string",
                },
                "time": {
                    "type": "string",
                    "pattern": "(\\d{4})-(\\d{2})-(\\d{2}) (\\d{2}):(\\d{2}):(\\d{2})"},
            },
            "required": [
                "result",
                "time"],
            "additionalProperties": False}
        try:
            validate(instance=json, schema=schema)
        except exceptions.ValidationError:
            return False
        return True


class TestIndex(TestRouts):
    # / Get
    def test_get_index(self):
        response = self.client.get('/')
        assert response.status_code == 200


class TestDictionary(TestRouts):
    # /dictionary GET
    def test_get_dictionary_check_status_code_equals_200(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = self.client.get('/dictionary/test')
        assert response.status_code == 200

    def test_get_dictionary_check_json_result_equals_data(self):
        response = self.client.get('/dictionary/test')
        assert response.json['result'] == 'data'

    def test_get_dictionary_check_response_format(self):
        response = self.client.get('/dictionary/test')
        assert self.helper_validate_response_json(response.json)

    def test_get_dictionary_check_status_code_equals_404(self):
        response = self.client.get('/dictionary/nonkey')
        assert response.status_code == 404

    # /dictionary DELETE

    def test_delete_dictionary_check_status_code_equals_200_exist(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = self.client.delete('/dictionary/test')
        assert response.status_code == 200

    def test_delete_dictionary_check_status_code_equals_200_not_exist(self):
        response = self.client.delete('/dictionary/empty')
        assert response.status_code == 200

    def test_delete_dictionary_check_json_result_equals_data(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = self.client.delete('/dictionary/test')
        assert response.json['result'] == 'data'

    def test_delete_dictionary_check_response_format(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = self.client.delete('/dictionary/test')
        assert self.helper_validate_response_json(response.json)

    # /dictionary POST

    def post_dictionary(self, json):
        return self.client.post('/dictionary', json=json)

    def test_post_dictionary_check_status_code_equals_200(self):
        response = self.post_dictionary({"key": "key", "value": "value"})
        assert response.status_code == 200

    def test_post_dictionary_check_status_code_equals_200_1(self):
        response = self.post_dictionary({"key": "key", "value": "value"})
        assert response.status_code == 200

    def test_post_dictionary_check_json_result_equals_data(self):
        response = self.post_dictionary({"key": "key", "value": "value"})
        assert response.json['result'] == 'value'

    def test_post_dictionary_check_response_format(self):
        response = self.post_dictionary({"key": "key", "value": "value"})
        assert self.helper_validate_response_json(response.json)

    def test_post_dictionary_check_status_code_equals_400_extra(self):
        response = self.post_dictionary(
            {"key": "key", "value": "value", "extra": "data"})
        assert response.status_code == 400

    def test_post_dictionary_check_status_code_equals_400_shortage(self):
        response = self.post_dictionary({"key": "key"})
        assert response.status_code == 400

    def test_post_dictionary_check_status_code_equals_400_blank_key(self):
        response = self.post_dictionary({"key": "", "value": "value"})
        assert response.status_code == 400

    def test_post_dictionary_check_status_code_equals_400_space_key(self):
        response = self.post_dictionary({"key": " ", "value": "value"})
        assert response.status_code == 400

    def test_post_dictionary_409(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = response = self.post_dictionary(
            {"key": "test", "value": "data"})
        assert response.status_code == 409

   # /dictionary PUT

    def put_dictionary(self, json):
        return self.client.put('/dictionary', json=json)

    def test_put_dictionary_check_status_code_equals_200(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = self.put_dictionary({"key": "test", "value": "date2"})
        assert response.status_code == 200

    def test_put_dictionary_check_status_code_equals_400_extra(self):
        response = self.put_dictionary(
            {"key": "key", "value": "value", "extra": "data"})
        assert response.status_code == 400

    def test_put_dictionary_check_status_code_equals_400_shortage(self):
        response = self.put_dictionary({"key": "key"})
        assert response.status_code == 400

    def test_put_dictionary_check_status_code_equals_400_blank_key(self):
        response = self.put_dictionary({"key": "", "value": "value"})
        assert response.status_code == 400

    def test_put_dictionary_check_status_code_equals_400_space_key(self):
        response = self.put_dictionary({"key": " ", "value": "value"})
        assert response.status_code == 400

    def test_put_dictionary_404(self):
        # {"key": "test", "value": "data"} created in self.setup method before start this test
        response = response = self.put_dictionary(
            {"key": "not_exist", "value": "data"})
        assert response.status_code == 404
