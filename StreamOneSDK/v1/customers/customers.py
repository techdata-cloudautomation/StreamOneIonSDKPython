import requests
import warnings
import base64
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError

class CustomersV1:
    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Basic {base64.b64encode(f'{self.api_key}:{self.api_secret}'.encode()).decode()}",
            "Content-Type": "application/json"
        }

    def get_customers(self, customer_id: Optional[str] = None, filters: Optional[Dict[str, Dict[str, str]]] = None, relations: Optional[List[str]] = None, limit: int = 100, offset: int = 0) -> Union[Dict, List]:
        warnings.warn("get_customers is deprecated and will be removed in a future version. Use the v3 API instead.", DeprecationWarning, stacklevel=2)
        
        if customer_id:
            endpoint = f"{self.base_url}/customers/{customer_id}"
        else:
            endpoint = f"{self.base_url}/customers"
        
        headers = self._get_headers()
        
        params = [f"limit={limit}", f"offset={offset}"]
        if filters:
            filter_str = '&'.join([f"filter[{key}{':' + value['modifier'] if 'modifier' in value else ''}]={value['value']}" for key, value in filters.items()])
            params.append(filter_str)
        if relations:
            relations_str = f"relations={','.join(relations)}"
            params.append(relations_str)
        
        endpoint = f"{endpoint}?{'&'.join(params)}"
        
        response = requests.get(endpoint, headers=headers)
        return self._handle_response(response)

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
            raise NotFoundError(response.text)
        elif response.status_code >= 500:
            raise ServerError(response.text)
        else:
            response.raise_for_status()
