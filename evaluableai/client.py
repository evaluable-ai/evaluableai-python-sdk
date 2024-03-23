import json

import httpx
from evaluableai.auth import Auth


class EvaluableAI:
    def __init__(self, token=None):
        self.auth = Auth(token)
        self.base_url = "https://api.evaluable.ai"

    def make_request(self, method="GET", endpoint="", data=None):
        """
        Synchronous request method.
        """
        headers = self.auth.get_headers()
        url = f"{self.base_url}{endpoint}"
        pretty_json = json.dumps(data, indent=4, sort_keys=True)
        print(pretty_json)
        # Using httpx for synchronous request to allow for easier switch between sync/async
        with httpx.Client() as client:
            response = client.request(method, url, headers=headers, json=data)
            if response.status_code not in [200, 201]:
                print("Request failed with status code:", response.status_code)
            return response

    async def async_make_request(self, method="GET", endpoint="", data=None):
        """
        Asynchronous request method.
        """
        headers = self.auth.get_headers()
        url = f"{self.base_url}{endpoint}"
        # Asynchronous request using httpx.AsyncClient
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, json=data)
        return response


class AsyncEvaluableAI:
    def __init__(self, token=None):
        self.auth = Auth(token)
        # Adjust the base URL as needed, e.g., for production use
        self.base_url = "https://api.evaluable.ai"

    async def async_make_request(self, method="GET", endpoint="", data=None):
        """
        Asynchronous request method.
        """
        headers = self.auth.get_headers()
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, json=data)
            if response.status_code not in [200, 201]:
                print(f"Request failed with status code: {response.status_code}")
            return response
