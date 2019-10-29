from sanic.testing import SanicTestClient

from service_api.app import app


class TestIndex:
    _test_client = SanicTestClient(app, port=None)

    def test_get_without_username_should_return_403(self):
        request, response = self._test_client.get('/')
        assert response.status == 403

    def test_get_with_username_should_return_200(self):
        request, response = self._test_client.get(
            '/',
            headers={"username": "tests"}
        )
        assert response.status == 200

    def test_post_without_username_should_return_403(self):
        request, response = self._test_client.post('/')
        assert response.status == 403

    def test_post_with_username_and_without_data_should_return_404(self):
        request, response = self._test_client.post(
            '/',
            headers={"username": "tests"}
        )
        assert response.status == 404

    def test_post_with_username_and_with_data_should_return_200(self):
        request, response = self._test_client.post(
            '/',
            headers={"username": "tests"},
            json={"sample": "data"}
        )
        assert response.status == 200

    def test_delete_without_username_should_return_403(self):
        request, response = self._test_client.delete('/')
        assert response.status == 403

    def test_delete_with_username_and_without_data_should_return_404(self):
        request, response = self._test_client.delete(
            '/',
            headers={"username": "tests"}
        )
        assert response.status == 404

    def test_delete_with_username_and_with_data_should_return_200(self):
        request, response = self._test_client.delete(
            '/',
            headers={"username": "tests"},
            json={"sample": "data"}
        )
        assert response.status == 200
