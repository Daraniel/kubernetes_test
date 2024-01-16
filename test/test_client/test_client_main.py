import unittest
from unittest.mock import Mock, patch

import httpx
from client_main import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.client = Client(self.base_url)

    def tearDown(self):
        self.client.close()

    @patch.object(httpx.Client, "post")
    def test_login_for_access_token(self, mock_post):
        mock_post.return_value = Mock(
            status_code=200, json=lambda: {"access_token": "test_token"}
        )

        response = self.client.login_for_access_token(
            username="johndoe", password="secret"
        )

        mock_post.assert_called_with(
            f"{self.base_url}/token",
            data={
                "grant_type": "password",
                "username": "johndoe",
                "password": "secret",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access_token"], "test_token")

    @patch.object(httpx.Client, "get")
    def test_get_users_me(self, mock_get):
        access_token = "test_token"
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"username": "johndoe", "email": "johndoe@example.com"},
        )

        response = self.client.get_users_me(access_token)

        mock_get.assert_called_with(
            f"{self.base_url}/user/users/me/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "johndoe")
        self.assertEqual(response.json()["email"], "johndoe@example.com")

    @patch.object(httpx.Client, "get")
    def test_get_items_me(self, mock_get):
        access_token = "test_token"
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: [
                {"item_name": "item1", "price": 10},
                {"item_name": "item2", "price": 20},
            ],
        )

        response = self.client.get_items_me(access_token)

        mock_get.assert_called_with(
            f"{self.base_url}/user/items/get_own_items/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"item_name": "item1", "price": 10}, {"item_name": "item2", "price": 20}],
        )
