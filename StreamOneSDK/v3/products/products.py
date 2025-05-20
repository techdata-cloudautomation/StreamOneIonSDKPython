import requests
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError


class ProductsV3:
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

    def list_products(self,  page_size: Optional[int] = None, language: Optional[str] = None, name: Optional[str] = None, sku_external_id: Optional[str] = None, addon_external_id: Optional[str] = None, sku_id: Optional[str] = None, addon_id: Optional[str] = None, sku_display_name: Optional[str] = None, addon_display_name: Optional[str] = None) -> iter:
        """
        Retrieves a list of products with optional filtering and handles pagination.

        :param page_size: Requested page size. Server may return fewer results than requested. If unspecified, the server will pick a default size.
        :param language: The language for the product data.
        :param name: The product name to filter on.
        :param sku_external_id: The external ID assigned to SKUs.
        :param addon_external_id: The external ID assigned to addons.
        :param sku_id: The ID of the SKU.
        :param addon_id: The ID of the addon.
        :param sku_display_name: The display name of the SKU.
        :param addon_display_name: The display name of the addon.
        :return: An iterator yielding products.
        """
        headers = self._get_headers()
        params = {}
        if page_size:
            params["pageSize"] = page_size

        page_token = None

        if language:
            params["language"] = language
        if name:
            params["filter.name"] = name
        if sku_external_id:
            params["filter.skuExternalId"] = sku_external_id
        if addon_external_id:
            params["filter.addonExternalId"] = addon_external_id
        if sku_id:
            params["filter.skuId"] = sku_id
        if addon_id:
            params["filter.addonId"] = addon_id
        if sku_display_name:
            params["filter.skuDisplayName"] = sku_display_name
        if addon_display_name:
            params["filter.addonDisplayName"] = addon_display_name

        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/products"

        def fetch_products():
            current_page_token = page_token
            while True:
                if current_page_token:
                    params["pageToken"] = current_page_token
                response = requests.get(url, headers=headers, params=params)
                data = self._handle_response(response)
                yield from [{"id": product["name"].split("/")[-1], **product} for product in data.get("products", [])]
                current_page_token = data.get("nextPageToken")
                if not current_page_token:
                    break

        return fetch_products()

    def get_product(self, product_id: str, language: Optional[str] = "", pricebook_customer_id: Optional[int] = None, product_version: Optional[str] = "", exclude_pricing: Optional[bool] = True, exclude_marketing: Optional[bool] = True, exclude_definition: Optional[bool] = True, exclude_version_history: Optional[bool] = True, exclude_deployment: Optional[bool] = True, client_role: Optional[str] = "CUSTOMER") -> Dict:
        """
        Retrieves a list of orders for a specific customer with optional filtering and handles pagination.

        :param customer_id: The unique customer ID.
        :param page_size: The number of results per page.
        :param status: The status of the orders to filter by.
        :return: An iterator yielding orders.
        """
        headers = self._get_headers()
        params = {}
        if language:
            params["language"] = language
        if pricebook_customer_id:
            params["priceBookCustomerId"] = pricebook_customer_id
        if product_version:
            params["productVersion"] = product_version

        params["excludeFilter.excludePricing"] = exclude_pricing
        params["excludeFilter.excludeMarketing"] = exclude_marketing
        params["excludeFilter.excludeDefinition"] = exclude_definition
        params["excludeFilter.excludeVersionHistory"] = exclude_version_history
        params["excludeFilter.excludeDeployment"] = exclude_deployment
        params["clientRole"] = client_role

        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/products/{product_id}"

        response = requests.get(url, headers=headers, params=params)
        product = self._handle_response(response)
        return {"id": product["name"].split("/")[-1], **product}

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
