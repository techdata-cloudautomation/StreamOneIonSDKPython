import requests
from typing import Dict, Optional, Union, List
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError


class SubscriptionsV3:
    def __init__(self, base_url: str, access_token: str, account_id: str):
        self.base_url = base_url
        self.access_token = access_token
        self.account_id = account_id

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def list_subscriptions(
        self,
        customerId: Optional[str] = None,
        subscriptionId: Optional[str] = None,
        resellerId: Optional[int] = None,
        providerId: Optional[int] = None,
        subscriptionStatus: Optional[str] = None,
        startDateRange: Optional[Dict[str, Union[str, Dict[str, str]]]] = None,
        endDate: Optional[str] = None,
        endDateRange: Optional[Dict[str, Union[str, Dict[str, str]]]] = None,
        billingTerm: Optional[str] = None,
        totalLicense: Optional[str] = None,
        ccpProductId: Optional[str] = None,
        providerProductId: Optional[str] = None,
        customerPo: Optional[str] = None,
        resellerPo: Optional[str] = None,
        customField: Optional[Dict[str, str]] = None,
        cloudProviderName: Optional[str] = None,
        accountName: Optional[str] = None,
        customerName: Optional[str] = None,
        subscriptionName: Optional[str] = None,
        resourceType: Optional[str] = None,
        pageSize: Optional[int] = 10,
        filter: Optional[str] = None,
        sortBy: Optional[str] = None,
        sortOrder: Optional[str] = None,
        userId: Optional[int] = None,
    ) -> iter:
        """
        List subscriptions with various filtering and sorting options.

        :param customerId: The unique customer ID.
        :param subscriptionId: The unique subscription ID.
        :param resellerId: The unique reseller ID.
        :param providerId: The unique cloud provider ID.
        :param subscriptionStatus: The current status of the subscription.
        :param startDateRange: The relative or fixed start date range of the subscriptions.
        :param endDate: The time when the subscription ends in ISO 8601 format.
        :param endDateRange: The relative or fixed end date range of the subscriptions.
        :param billingTerm: The period for which the subscription service is active.
        :param totalLicense: The total number of subscriptions available for the account.
        :param ccpProductId: The unique product ID in the CCP catalog.
        :param providerProductId: The unique product ID in the provider catalog.
        :param customerPo: The end customer's purchase order.
        :param resellerPo: The reseller's purchase order.
        :param customField: Filter CustomerCustomFields attributes (key-value pairs).
        :param cloudProviderName: Name of the cloud provider (e.g., AWS, GCP).
        :param accountName: Name of the account.
        :param customerName: Name of the customer.
        :param subscriptionName: Name of the subscription.
        :param resourceType: The resource type identifier within the subscriptions.
        :param pageSize: Number of results per page.
        :param filter: Additional filtering options.
        :param sortBy: Field to sort by.
        :param sortOrder: Sort order (asc or desc).
        :param userId: The user ID for filtering.
        :return: An iterable object containing subscription data.
        """
        headers = self._get_headers()
        params = {
            "pagination.limit": pageSize,
            "pagination.offset": 0
        }
        if filter:
            params["pagination.filter"] = filter
        if sortBy:
            params["pagination.sortBy"] = sortBy
        if sortOrder:
            params["pagination.sortOrder"] = sortOrder
        if userId:
            params["pagination.userId"] = userId
        if customerId:
            params["customerId"] = customerId
        if subscriptionId:
            params["subscriptionId"] = subscriptionId
        if resellerId:
            params["resellerId"] = resellerId
        if providerId:
            params["providerId"] = providerId
        if subscriptionStatus:
            params["subscriptionStatus"] = subscriptionStatus
        if startDateRange:
            for key, value in startDateRange.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        params[f"startDateRange.{key}.{sub_key}"] = sub_value
                else:
                    params[f"startDateRange.{key}"] = value
        if endDate:
            params["endDate"] = endDate
        if endDateRange:
            for key, value in endDateRange.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        params[f"endDateRange.{key}.{sub_key}"] = sub_value
                else:
                    params[f"endDateRange.{key}"] = value
        if billingTerm:
            params["billingTerm"] = billingTerm
        if totalLicense:
            params["totalLicense"] = totalLicense
        if ccpProductId:
            params["ccpProductId"] = ccpProductId
        if providerProductId:
            params["providerProductId"] = providerProductId
        if customerPo:
            params["customerPo"] = customerPo
        if resellerPo:
            params["resellerPo"] = resellerPo
        if customField:
            params.update({f"customField.{k}": v for k,
                          v in customField.items()})
        if cloudProviderName:
            params["cloudProviderName"] = cloudProviderName
        if accountName:
            params["accountName"] = accountName
        if customerName:
            params["customerName"] = customerName
        if subscriptionName:
            params["subscriptionName"] = subscriptionName
        if resourceType:
            params["resourceType"] = resourceType
        if filter:
            params["pagination.filter"] = filter
        if sortBy:
            params["pagination.sortBy"] = sortBy
        if sortOrder:
            params["pagination.sortOrder"] = sortOrder
        if userId:
            params["pagination.userId"] = userId
        print(params)

        def fetch_subscriptions():
            while True:
                response = requests.get(
                    f"{self.base_url}/api/v3/accounts/{self.account_id}/subscriptions",
                    headers=headers,
                    params=params,
                )
                data = self._handle_response(response)
                yield from data.get("items", [])
                if not data.get("items"):
                    break
                params["pagination.offset"] += pageSize

        return fetch_subscriptions()

    def get_customer_subscription_details(self, customerId: str, subscriptionId: str, refresh: Optional[bool] = None) -> Dict:
        """
        Retrieve details of a specific subscription for a customer.

        :param customerId: The unique customer ID.
        :param subscriptionId: The unique subscription ID.
        :param refresh: Optional. If True, updates the results.
        :return: A dictionary containing subscription details.
        """
        headers = self._get_headers()
        params = {}
        if refresh is not None:
            params["refresh"] = str(refresh).lower()

        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/customers/{customerId}/subscriptions/{subscriptionId}"
        response = requests.get(url, headers=headers, params=params)
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
