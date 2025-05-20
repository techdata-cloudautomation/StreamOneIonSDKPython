import requests
import base64
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError


class BillingV1:
    """
    BillingV1 provides methods to interact with the v1 billing endpoints of the StreamOneSDK API.
    Handles invoice retrieval, invoice generation, and downloading detailed invoice data.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str):
        """
        Initialize the BillingV1 client with API credentials and base URL.
        Args:
            base_url (str): The base URL for the v1 API.
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_headers(self) -> Dict[str, str]:
        """
        Construct the HTTP headers required for API requests, including authorization.
        Returns:
            Dict[str, str]: Headers with authorization and content type.
        """
        return {
            "Authorization": f"Basic {base64.b64encode(f'{self.api_key}:{self.api_secret}'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    def get_my_invoices(self, filters: Optional[Dict[str, Dict[str, str]]] = None, sort: Optional[Dict[str, str]] = None, limit: int = 100, offset: int = 0, relations: Optional[List[str]] = None) -> Union[Dict, List]:
        """
        Retrieve a list of invoices for the authenticated user.
        Args:
            filters (Optional[Dict[str, Dict[str, str]]]): A dictionary of filters to apply to the invoices.
            Each key represents a field to filter on, and the value is another dictionary with:
                - 'value': The value to filter by.
                - 'modifier' (optional): A modifier for the filter (e.g., 'eq', 'lt', 'gt').
            sort (Optional[Dict[str, str]]): A dictionary specifying sorting options.
            Each key represents a field to sort by, and the value is the sort direction ('asc' or 'desc').
            limit (int): The maximum number of invoices to retrieve. Default is 100.
            offset (int): The number of invoices to skip before starting to retrieve. Default is 0.
            relations (Optional[List[str]]): A list of related entities to include in the response.
        Returns:
            Union[Dict, List]: The response containing the list of invoices or an error message.
        Raises:
            HTTPError: If the HTTP request fails or returns an error response.
        """
        endpoint = f"{self.base_url}/invoices/myinvoices"
        headers = self._get_headers()

        params = [f"limit={limit}", f"offset={offset}"]
        if filters:
            filter_str = '&'.join(
                [f"filter[{key}{':' + value['modifier'] if 'modifier' in value else ''}]={value['value']}" for key, value in filters.items()])
            params.append(filter_str)
        if sort:
            sort_str = '&'.join(
                [f"sort[{key}]={value}" for key, value in sort.items()])
            params.append(sort_str)
        if relations:
            relations_str = f"relations={','.join(relations)}"
            params.append(relations_str)

        endpoint = f"{endpoint}?{'&'.join(params)}"

        response = requests.get(endpoint, headers=headers)
        return self._handle_response(response)

    def get_customer_invoices(self, customer_id: str, filters: Optional[Dict[str, Dict[str, str]]] = None, limit: int = 100, offset: int = 0) -> Union[Dict, List]:
        """
        Retrieve a list of invoices for a specific customer.
        Args:
            customer_id (str): The customer ID to retrieve invoices for.
            filters (Optional[Dict[str, Dict[str, str]]]): Filters to apply to the invoices.
            limit (int): Maximum number of invoices to retrieve. Default is 100.
            offset (int): Number of invoices to skip before starting to retrieve. Default is 0.
        Returns:
            Union[Dict, List]: The response containing the list of invoices or an error message.
        Raises:
            HTTPError: If the HTTP request fails or returns an error response.
        """
        endpoint = f"{self.base_url}/invoices"
        headers = self._get_headers()

        params = [f"limit={limit}", f"offset={offset}"]
        if filters:
            filter_str = '&'.join(
                [f"filter[{key}{':' + value['modifier'] if 'modifier' in value else ''}]={value['value']}" for key, value in filters.items()])
            params.append(filter_str)

        endpoint = f"{endpoint}?{'&'.join(params)}&customerId={customer_id}"

        response = requests.get(endpoint, headers=headers)
        return self._handle_response(response)

    def get_detailed_invoice_data(self, invoice_id: str, save_folder: str) -> None:
        """
        Download detailed invoice data files for a given invoice ID and save them to a folder.
        Args:
            invoice_id (str): The invoice ID to retrieve detailed data for.
            save_folder (str): The folder to save downloaded invoice files.
        Returns:
            None
        Raises:
            HTTPError: If the HTTP request fails or returns an error response.
        """
        endpoint = f"{self.base_url}/invoices/{invoice_id}/detailed"
        headers = self._get_headers()

        response = requests.get(endpoint, headers=headers)
        detailed_invoice_data = self._handle_response(response)

        invoices_created = []
        for url in detailed_invoice_data["data"]["invoice"]["detailedInvoiceFilesUrls"]:
            response = requests.get(url)
            if response.status_code == 200:
                file_name = os.path.join(
                    save_folder, os.path.basename(url.split("?")[0]))
                invoices_created.append(file_name)
                with open(file_name, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {url}")
        return invoices_created

    def generate_invoices(self, source: str, period: Optional[str] = None, status: str = 'open', customers: Optional[List[str]] = None, resellers: Optional[List[str]] = None, sendEmails: bool = False) -> Union[Dict, List]:
        """
        Generate invoices for the specified source and period.
        Args:
            source (str): The source for invoice generation.
            period (Optional[str]): The period for which to generate invoices. If None, defaults to last month.
            status (str): The status of the invoices to generate. Default is 'open'.
            customers (Optional[List[str]]): List of customer IDs to generate invoices for.
            resellers (Optional[List[str]]): List of reseller IDs to generate invoices for.
            sendEmails (bool): Whether to send emails after invoice generation. Default is False.
        Returns:
            Union[Dict, List]: Response from the API or error message.
        Raises:
            HTTPError: If the HTTP request fails or returns an error response.
        """
        endpoint = f"{self.base_url}/invoices/generate"
        headers = self._get_headers()

        if period is None:
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            period = f"m-{last_month.strftime('%m-%Y')}"

        data = {
            'source': source,
            'period': period,
            'status': status,
            'sendEmails': sendEmails
        }

        if customers:
            data['customers'] = ','.join(customers)
        if resellers:
            data['resellers'] = ','.join(resellers)

        response = requests.post(endpoint, headers=headers, data=data)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
        """
        Handle the HTTP response from API requests, raising appropriate exceptions for error codes.
        Args:
            response (requests.Response): The HTTP response object.
        Returns:
            Union[Dict, List]: The parsed JSON response if successful.
        Raises:
            BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError: For respective HTTP error codes.
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
            raise NotFoundError(response.text)
        elif response.status_code >= 500:
            raise ServerError(response.text)
        else:
            response.raise_for_status()
