import contextlib
import threading
import time
import unittest

import httpx
import uvicorn


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()

        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


# This kind of wierd function won't be needed if I simply used PyTest fixtures but this is a test code so having
# a few wierd things won't be bad :)
def setup_with_context_manager(testcase, cm):
    """Use a contextmanager to setUp a test case."""
    val = cm.__enter__()
    testcase.addCleanup(cm.__exit__, None, None, None)
    return val


# A simple test that only tests the bare minimum, this is not a real app after all...
class TestServer(unittest.TestCase):
    def setUp(self):
        config = uvicorn.Config("server.server_main:app")
        self.client = httpx.Client()
        self.server = Server(config=config)
        setup_with_context_manager(self, self.server.run_in_thread())  # let's use the wierd thingy
        self.base_url = f"http://{self.server.config.host}:{self.server.config.port}"
        self.token = None

    def tearDown(self):
        self.client.close()

    def get_access_token(self):
        if self.token is None:
            endpoint = "/token"
            data = {
                "grant_type": "password",
                "username": "johndoe",
                "password": "secret",
            }
            response = self.client.post(f"{self.base_url}{endpoint}", data=data)
            self.token = response
            return response
        else:
            return self.token

    def test_login_for_access_token(self):
        response = self.get_access_token()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["access_token"])

    def test_read_users_me(self):
        access_token = self.get_access_token().json()["access_token"]

        endpoint = "/user/users/me/"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get(f"{self.base_url}{endpoint}", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "johndoe")
        self.assertEqual(response.json()["email"], "johndoe@example.com")

    def test_get_items_me(self):
        access_token = self.get_access_token().json()["access_token"]

        endpoint = "/user/items/get_own_items/"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get(f"{self.base_url}{endpoint}", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"name": "Item 1", "description": "Description 1", "price": 10.0},
                                           {"name": "Item 2", "description": "Description 2", "price": 20.0}])
