import requests
from typing import Dict, Optional, Union, List
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError

class CustomersV3:
    def __init__(self, base_url: str, access_token: str, account_id: str):
        self.base_url = base_url
        self.access_token = access_token
        self.account_id = account_id

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def list_customers(self, pageSize: int = 10, customerEmail: Optional[str] = None, languageCode: Optional[str] = None, customerStatus: Optional[str] = None, customerName: Optional[str] = None) -> iter:
        """
        Retrieves a paginated list of customers with optional filtering.
        Args:
            pageSize (int, optional): The number of customers to retrieve per page. Defaults to 10.
            customerEmail (Optional[str], optional): Filter customers by email. Defaults to None.
            languageCode (Optional[str], optional): Filter customers by language code. Defaults to None.
            customerStatus (Optional[str], optional): Filter customers by status. Defaults to None.
            customerName (Optional[str], optional): Filter customers by name. Defaults to None.
        Returns:
            iter: An iterator that yields customer dictionaries.
        Raises:
            HTTPError: If the HTTP request fails or returns an error response.
        """
        headers = self._get_headers()
        params = {"pageSize": pageSize}
        if customerEmail:
            params["filter.customerEmail"] = customerEmail
        if languageCode:
            params["filter.languageCode"] = languageCode
        if customerStatus:
            params["filter.customerStatus"] = customerStatus
        if customerName:
            params["filter.customerName"] = customerName

        def fetch_customers():
            next_page_token = None
            while True:
                if next_page_token:
                    params["pageToken"] = next_page_token

                response = requests.get(
                    f"{self.base_url}/api/v3/accounts/{self.account_id}/customers",
                    headers=headers,
                    params=params
                )
                data = self._handle_response(response)
                yield from [{"id": customer["name"].split("/")[-1],**customer} for customer in data.get("customers", [])]
                next_page_token = data.get("nextPageToken")
                if not next_page_token or not data:
                    break

        return fetch_customers()

    def get_customer(self, customerId: str) -> Dict:
        """
        Retrieves customer details by customer ID.
        Args:
            customerId (str): The unique identifier of the customer.
        Returns:
            Dict: A dictionary containing customer details, including the customer ID 
                  extracted from the "name" field and other customer information.
        Raises:
            HTTPError: If the HTTP request to retrieve the customer fails.
        """
        headers = self._get_headers()
        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/customers/{customerId}"
        
        response = requests.get(url, headers=headers)
        customer = self._handle_response(response)
        return {"id": customer["name"].split("/")[-1], **customer}

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
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
