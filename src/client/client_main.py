import httpx


class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.Client()

    def login_for_access_token(self, username, password):
        endpoint = "/token"
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        return self.client.post(f"{self.base_url}{endpoint}", data=data)

    def get_users_me(self, access_token):
        endpoint = "/user/users/me/"
        headers = {"Authorization": f"Bearer {access_token}"}
        return self.client.get(f"{self.base_url}{endpoint}", headers=headers)

    def get_items_me(self, access_token):
        endpoint = "/user/items/get_own_items/"
        headers = {"Authorization": f"Bearer {access_token}"}
        return self.client.get(f"{self.base_url}{endpoint}", headers=headers)

    def close(self):
        self.client.close()


if __name__ == "__main__":
    # Example usage, make sure that the server is already running
    base_url = "http://127.0.0.1:8000"
    client = Client(base_url)

    # Login and get access token
    response = client.login_for_access_token(username="johndoe", password="secret")
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        print("Access Token:", access_token)

        # Read user's information
        response = client.get_users_me(access_token)
        if response.status_code == 200:
            user_info = response.json()
            print("User Information:", user_info)

        # Read user's items
        response = client.get_items_me(access_token)
        if response.status_code == 200:
            user_items = response.json()
            print("User Items:", user_items)

    # Close the client when done
    client.close()
