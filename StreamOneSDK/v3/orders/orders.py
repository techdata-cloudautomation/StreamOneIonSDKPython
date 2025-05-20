import requests
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError


class OrdersV3:
    def __init__(self, base_url: str, access_token: str, account_id: str):
        self.base_url = base_url
        self.access_token = access_token
        self.account_id = account_id

    def _get_headers(self) -> Dict[str, str]:
        """
        Constructs the headers required for the API request.

        :return: A dictionary containing the headers.
        """
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def list_account_orders(self, page_size: Optional[int] = None,  status: Optional[str] = None) -> iter:
        """
        Retrieves a list of orders with optional filtering and handles pagination.

        :param page_size: The number of results per page.
        :param page_token: The token for the next page of results.
        :param status: The status of the orders to filter by.
        :return: An iterator yielding orders.
        """
        headers = self._get_headers()
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if status:
            params["status"] = status
        page_token = ""

        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/orders"

        def fetch_orders():
            current_page_token = page_token
            while True:
                if current_page_token:
                    params["pageToken"] = current_page_token
                response = requests.get(url, headers=headers, params=params)
                data = self._handle_response(response)
                yield from data.get("orders", [])
                current_page_token = data.get("nextPageToken")
                if not current_page_token:
                    break

        return fetch_orders()

    def list_customer_orders(self, customer_id: str, page_size: Optional[int] = None, status: Optional[str] = None) -> iter:
        """
        Retrieves a list of orders for a specific customer with optional filtering and handles pagination.

        :param customer_id: The unique customer ID.
        :param page_size: The number of results per page.
        :param status: The status of the orders to filter by.
        :return: An iterator yielding orders.
        """
        headers = self._get_headers()
        params = {}
        if page_size:
            params["pageSize"] = page_size
        if status:
            params["status"] = status
        page_token = ""

        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/customers/{customer_id}/orders"

        def fetch_orders():
            current_page_token = page_token
            while True:
                if current_page_token:
                    params["pageToken"] = current_page_token
                response = requests.get(url, headers=headers, params=params)
                data = self._handle_response(response)
                yield from data.get("orders", [])
                current_page_token = data.get("nextPageToken")
                if not current_page_token:
                    break

        return fetch_orders()

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
        """
        Handles the HTTP response and raises appropriate exceptions for error codes.

        :param response: The HTTP response object.
        :return: The parsed JSON response if the status code is 200.
        :raises: Raises appropriate exceptions for HTTP error codes.
        """
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            raise BadRequestError(response.text)
        elif response.status_code == 401:
            raise AuthenticationError(response.text)
        elif response.status_code == 403:
            raise AuthorizationError(response.text)
        elif response.status_code == 404:
            return {}
        elif response.status_code >= 500:
            raise ServerError(response.text)
        else:
            response.raise_for_status()
