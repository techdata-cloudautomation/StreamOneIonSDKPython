import json
from typing import Dict, List, Optional, Union
import requests
import datetime
from .exceptions import StreamOneSDKException
from .v1.customers.customers import CustomersV1
from .v1.billing.billing import BillingV1
from .v3.customers.customers import CustomersV3
from .v3.subscriptions.subscriptions import SubscriptionsV3
from .v3.reports.reports import ReportsV3
from .v3.orders.orders import OrdersV3
from .v3.products.products import ProductsV3


class StreamOneClient:
    """
    Main client class for interacting with the StreamOneSDK API.
    Handles authentication, configuration, and provides access to v1 and v3 API modules.
    """

    def __init__(self, config: str):
        """
        Initialize the StreamOneClient with the given configuration file.
        Loads credentials and sets up API modules for v1 and v3 endpoints.

        Args:
            config (str): Path to the JSON configuration file containing credentials and account ID.
        Raises:
            StreamOneSDKException: If required credentials are missing from the configuration.
        """
        with open(config, 'r') as f:
            env_data = json.load(f)

        if ('v1' not in env_data and 'v3' not in env_data) or "accountid" not in env_data:
            raise StreamOneSDKException("Configuration must include either v1 or v3 credentials. Example structure:\n"
                                        "{\n"
                                        "    \"v1\": {\n"
                                        "        \"api_key\": \"your_v1_api_key\",\n"
                                        "        \"api_secret\": \"your_v1_api_secret\"\n"
                                        "    },\n"
                                        "    \"v3\": {\n"
                                        "        \"access_token\": \"your_v3_access_token\",\n"
                                        "        \"refresh_token\": \"your_v3_refresh_token\"\n"
                                        "    },\n"
                                        "    \"accountid\": \"your_account_id\"\n"
                                        "}")
        self.account_id = env_data.get("accountid")
        if 'v1' in env_data:
            v1api_key = env_data['v1']["api_key"]
            v1api_secret = env_data['v1']["api_secret"]
            self.v1_base_url = "https://ion.tdsynnex.com/api/v1"
            self.customers_v1 = CustomersV1(
                self.v1_base_url, v1api_key, v1api_secret)
            self.billing_v1 = BillingV1(
                self.v1_base_url, v1api_key, v1api_secret)
        else:
            self.v1_base_url = None
            self.customers_v1 = None
            self.billing_v1 = None

        if 'v3' in env_data:
            v3_access_token = env_data['v3']["access_token"]
            v3_refresh_token = env_data['v3']["refresh_token"]
            self.v3_base_url = "https://ion.tdsynnex.com"
            self.v3_access_token = v3_access_token
            self.v3_refresh_token = v3_refresh_token
            self.customers_v3 = CustomersV3(
                self.v3_base_url, v3_access_token, env_data["accountid"])
            self.subscriptions_v3 = SubscriptionsV3(
                self.v3_base_url, v3_access_token, env_data["accountid"])
            self.reports_v3 = ReportsV3(
                self.v3_base_url, v3_access_token, env_data["accountid"])
            self.orders_v3 = OrdersV3(
                self.v3_base_url, v3_access_token, env_data["accountid"])
            self.products_v3 = ProductsV3(
                self.v3_base_url, v3_access_token, env_data["accountid"])

        else:
            self.v3_base_url = None
            self.customers_v3 = None
            self.subscriptions_v3 = None

        self.config_path = config

    def refresh_access_token(self):
        """
        Refresh the v3 access token using the refresh token if the current access token is invalid or expired.
        Updates the configuration file and instance variables with new tokens.

        Raises:
            StreamOneSDKException: If v3 refresh token is not configured.
        """
        if not self.v3_refresh_token:
            raise StreamOneSDKException("v3 refresh token is not configured.")

        with open(self.config_path, 'r') as f:
            config = json.load(f)

        # Validate the current access token
        validate_response = requests.post(
            self.v3_base_url + "/oauth/validateAccess",
            data={"access_token": config["v3"]["access_token"]},
            headers={"content-type": "application/x-www-form-urlencoded"}
        )
        if validate_response.status_code == 200:
            return

        # Refresh the token
        response = requests.post(
            self.v3_base_url + "/oauth/token",
            data={
                "grant_type": "refresh_token",
                "redirect_uri": "http://localhost/",
                "refresh_token": config["v3"]["refresh_token"]
            },
            headers={"content-type": "application/x-www-form-urlencoded"}
        )
        token_data = response.json()
        config["v3"]["access_token"] = token_data["access_token"]
        config["v3"]["refresh_token"] = token_data["refresh_token"]

        # Update instance variables
        self.v3_access_token = token_data["access_token"]
        self.v3_refresh_token = token_data["refresh_token"]
        self.subscriptions_v3 = SubscriptionsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        self.customers_v3 = CustomersV3(
            self.v3_base_url, self.v3_access_token, self.account_id)

        with open(self.config_path, "w") as f_out:
            json.dump(config, f_out, indent=2)

    def get_my_invoices(self, filters: Optional[Dict[str, Dict[str, str]]] = None, sort: Optional[Dict[str, str]] = None, limit: int = 100, offset: int = 0, relations: Optional[List[str]] = None) -> Union[Dict, List]:
        """
        Retrieve a list of invoices for the authenticated user (v1 API).

        Args:
            filters (Optional[Dict[str, Dict[str, str]]]): Filters to apply to the invoices.
            sort (Optional[Dict[str, str]]): Sorting options.
            limit (int): Maximum number of invoices to retrieve.
            offset (int): Number of invoices to skip before starting to retrieve.
            relations (Optional[List[str]]): Related entities to include in the response.

        Returns:
            Union[Dict, List]: List of invoices or error message.

        Raises:
            StreamOneSDKException: If v1 credentials are not configured.
        """
        if not self.billing_v1:
            raise StreamOneSDKException("v1 credentials are not configured.")
        return self.billing_v1.get_my_invoices(filters, sort, limit, offset, relations)

    def get_customer_invoices(self, customer_id: str, filters: Optional[Dict[str, Dict[str, str]]] = None, limit: int = 100, offset: int = 0) -> Union[Dict, List]:
        """
        Retrieve a list of invoices for a specific customer (v1 API).

        Args:
            customer_id (str): The customer ID.
            filters (Optional[Dict[str, Dict[str, str]]]): Filters to apply to the invoices.
            limit (int): Maximum number of invoices to retrieve.
            offset (int): Number of invoices to skip before starting to retrieve.

        Returns:
            Union[Dict, List]: List of invoices or error message.

        Raises:
            StreamOneSDKException: If v1 credentials are not configured.
        """
        if not self.billing_v1:
            raise StreamOneSDKException("v1 credentials are not configured.")
        return self.billing_v1.get_customer_invoices(customer_id, filters, limit, offset)

    def get_detailed_invoice_data(self, invoice_id: str, save_folder: str) -> None:
        """
        Download detailed invoice data files for a given invoice ID and save them to a folder (v1 API).

        Args:
            invoice_id (str): The invoice ID.
            save_folder (str): The folder to save downloaded invoice files.

        Returns:
            None

        Raises:
            StreamOneSDKException: If v1 credentials are not configured.
        """
        if not self.billing_v1:
            raise StreamOneSDKException("v1 credentials are not configured.")
        return self.billing_v1.get_detailed_invoice_data(invoice_id, save_folder)

    def get_customers_v1(self, customer_id: Optional[str] = None, filters: Optional[Dict[str, Dict[str, str]]] = None, relations: Optional[List[str]] = None, limit: int = 100, offset: int = 0) -> Union[Dict, List]:
        """
        Retrieve customer(s) from the v1 API.

        Args:
            customer_id (Optional[str]): The customer ID to retrieve (optional).
            filters (Optional[Dict[str, Dict[str, str]]]): Filters to apply to the customers.
            relations (Optional[List[str]]): Related entities to include in the response.
            limit (int): Maximum number of customers to retrieve.
            offset (int): Number of customers to skip before starting to retrieve.

        Returns:
            Union[Dict, List]: List of customers or error message.

        Raises:
            StreamOneSDKException: If v1 credentials are not configured.
        """
        if not self.customers_v1:
            raise StreamOneSDKException("v1 credentials are not configured.")
        return self.customers_v1.get_customers(customer_id, filters, relations, limit, offset)

    def generate_invoices(self, source: str, period: Optional[str] = None, status: str = 'open', customers: Optional[List[str]] = None, resellers: Optional[List[str]] = None, sendEmails: bool = False) -> Union[Dict, List]:
        """
        Generate invoices for the specified source and period (v1 API).

        Args:
            source (str): The source for invoice generation.
            period (Optional[str]): The period for which to generate invoices.
            status (str): The status of the invoices to generate.
            customers (Optional[List[str]]): List of customer IDs to generate invoices for.
            resellers (Optional[List[str]]): List of reseller IDs to generate invoices for.
            sendEmails (bool): Whether to send emails after invoice generation.

        Returns:
            Union[Dict, List]: Response from the API or error message.

        Raises:
            StreamOneSDKException: If v1 credentials are not configured.
        """
        if not self.billing_v1:
            raise StreamOneSDKException("v1 credentials are not configured.")
        return self.billing_v1.generate_invoices(source, period, status, customers, resellers, sendEmails)

    def list_customers(self, pageSize: int = 1, customerEmail: Optional[str] = None, languageCode: Optional[str] = None, customerStatus: Optional[str] = None, customerName: Optional[str] = None) -> iter:
        """
        Retrieves a list of customers with optional filtering parameters (v3 API).

        Args:
            pageSize (int, optional): The number of customers to retrieve per page. Defaults to 1.
            customerEmail (Optional[str], optional): Filter by customer email. Defaults to None.
            languageCode (Optional[str], optional): Filter by language code. Defaults to None.
            customerStatus (Optional[str], optional): Filter by customer status. Defaults to None.
            customerName (Optional[str], optional): Filter by customer name. Defaults to None.

        Returns:
            iter: An iterator containing the list of customers.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.customers_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.customers_v3 = CustomersV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.customers_v3.list_customers(pageSize, customerEmail, languageCode, customerStatus, customerName)

    def get_customer(self, customerId: str) -> Dict:
        """
        Retrieve customer details using the provided customer ID.

        Args:
            customerId (str): The unique identifier of the customer to retrieve.

        Returns:
            Dict: A dictionary containing customer details, including the customer ID 
                  extracted from the "name" field and other customer information.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.customers_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.customers_v3 = CustomersV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.customers_v3.get_customer(customerId)

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

        Args:
            customerId (Optional[str]): The unique customer ID.
            subscriptionId (Optional[str]): The unique subscription ID.
            resellerId (Optional[int]): The unique reseller ID.
            providerId (Optional[int]): The unique cloud provider ID.
            subscriptionStatus (Optional[str]): The current status of the subscription.
            startDateRange (Optional[Dict[str, Union[str, Dict[str, str]]]]): The relative or fixed start date range of the subscriptions.
            endDate (Optional[str]): The time when the subscription ends in ISO 8601 format.
            endDateRange (Optional[Dict[str, Union[str, Dict[str, str]]]]): The relative or fixed end date range of the subscriptions.
            billingTerm (Optional[str]): The period for which the subscription service is active.
            totalLicense (Optional[str]): The total number of subscriptions available for the account.
            ccpProductId (Optional[str]): The unique product ID in the CCP catalog.
            providerProductId (Optional[str]): The unique product ID in the provider catalog.
            customerPo (Optional[str]): The end customer's purchase order.
            resellerPo (Optional[str]): The reseller's purchase order.
            customField (Optional[Dict[str, str]]): Filter CustomerCustomFields attributes (key-value pairs).
            cloudProviderName (Optional[str]): Name of the cloud provider (e.g., AWS, GCP).
            accountName (Optional[str]): Name of the account.
            customerName (Optional[str]): Name of the customer.
            subscriptionName (Optional[str]): Name of the subscription.
            resourceType (Optional[str]): The resource type identifier within the subscriptions.
            pageSize (Optional[int]): Number of results per page.
            filter (Optional[str]): Additional filtering options.
            sortBy (Optional[str]): Field to sort by.
            sortOrder (Optional[str]): Sort order (asc or desc).
            userId (Optional[int]): The user ID for filtering.

        Returns:
            iter: An iterable object containing subscription data.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.subscriptions_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.subscriptions_v3 = SubscriptionsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.subscriptions_v3.list_subscriptions(
            customerId=customerId,
            subscriptionId=subscriptionId,
            resellerId=resellerId,
            providerId=providerId,
            subscriptionStatus=subscriptionStatus,
            startDateRange=startDateRange,
            endDate=endDate,
            endDateRange=endDateRange,
            billingTerm=billingTerm,
            totalLicense=totalLicense,
            ccpProductId=ccpProductId,
            providerProductId=providerProductId,
            customerPo=customerPo,
            resellerPo=resellerPo,
            customField=customField,
            cloudProviderName=cloudProviderName,
            accountName=accountName,
            customerName=customerName,
            subscriptionName=subscriptionName,
            resourceType=resourceType,
            pageSize=pageSize,
            filter=filter,
            sortBy=sortBy,
            sortOrder=sortOrder,
            userId=userId,
        )

    def get_customer_subscription_details(self, customerId: str, subscriptionId: str, refresh: Optional[bool] = None) -> Dict:
        """
        Retrieve details of a specific subscription for a customer.

        Args:
            customerId (str): The unique customer ID.
            subscriptionId (str): The unique subscription ID.
            refresh (Optional[bool]): If True, updates the results.

        Returns:
            Dict: A dictionary containing subscription details.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.subscriptions_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.subscriptions_v3 = SubscriptionsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.subscriptions_v3.get_customer_subscription_details(customerId, subscriptionId, refresh)

    def list_reports(self, module: Optional[str] = "REPORTS_MODULE_UNSPECIFIED") -> List[Dict]:
        """
        List all report specifications for the given module.

        Args:
            module (Optional[str]): The requesting module. Possible values are:
                - "REPORTS_MODULE_UNSPECIFIED"
                - "REPORTS_REPORTS_MODULE"
                - "DASHBOARDS_REPORTS_MODULE"
                - "BUDGET_MANAGEMENT_REPORTS_MODULE"
                - "INVOICE_REPORTS_MODULE"
                - "V1_BILLING_REPORTS_MODULE"
                - "CACHING_REPORTS_MODULE"

        Returns:
            List[Dict]: A list of report definitions.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.reports_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.reports_v3 = ReportsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.reports_v3.list_reports(module)

    def get_report_data_csv(self, report_id: str, report_module: str, category: str, start_date: str = None, end_date: str = None, relative_date_range: str = "MONTH_TO_DATE", path: str = "") -> requests.Response:
        """
        Fetches the report data in CSV format.

        Args:
            report_id (str): The ID of the report.
            report_module (str): The module that uses the reports service.
            category (str): The type of report produced.
            start_date (Optional[str]): The start date for the report data in the format %Y-%m-%dT%H:%M:%SZ (used if relative_date_range is not provided).
            end_date (Optional[str]): The end date for the report data in the format %Y-%m-%dT%H:%M:%SZ  (used if relative_date_range is not provided).
            relative_date_range (Optional[str]): A relative date range (e.g.,"UNKNOWN_RELATIVE_DATE_RANGE", "CUSTOM", "TODAY", "MONTH_TO_DATE", "QUARTER_TO_DATE", "YEAR_TO_DATE", "LAST_MONTH", "LAST_QUARTER", "LAST_YEAR", "LATEST_MONTH", "WEEK_TO_DATE", "LAST_WEEK", "TWO_MONTHS_AGO").
            path (Optional[str]): Path to save the CSV file.

        Returns:
            requests.Response: Path to the csv file with the data.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.reports_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.reports_v3 = ReportsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.reports_v3.get_report_data_csv(report_id, report_module, category, start_date=start_date, end_date=end_date, relative_date_range=relative_date_range, path=path)

    def list_account_orders(self, page_size: Optional[int] = None, status: Optional[str] = None) -> iter:
        """
        Retrieves a list of orders with optional filtering and handles pagination.

        Args:
            page_size (Optional[int]): The number of results per page.
            status (Optional[str]): The status of the orders to filter by.

        Returns:
            iter: An iterator yielding orders.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.orders_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.orders_v3 = OrdersV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.orders_v3.list_account_orders(page_size, status)

    def list_customer_orders(self, customer_id: str, page_size: Optional[int] = None, status: Optional[str] = None) -> iter:
        """
        Retrieves a list of orders for a specific customer with optional filtering and handles pagination.

        Args:
            customer_id (str): The unique customer ID.
            page_size (Optional[int]): The number of results per page.
            status (Optional[str]): The status of the orders to filter by.

        Returns:
            iter: An iterator yielding orders.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.orders_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.orders_v3 = OrdersV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.orders_v3.list_customer_orders(customer_id, page_size, status)

    def list_products(self, page_size: Optional[int] = None, language: Optional[str] = None, name: Optional[str] = None, sku_external_id: Optional[str] = None, addon_external_id: Optional[str] = None, sku_id: Optional[str] = None, addon_id: Optional[str] = None, sku_display_name: Optional[str] = None, addon_display_name: Optional[str] = None) -> iter:
        """
        Retrieves a list of products with optional filtering and handles pagination.

        Args:
            page_size (Optional[int]): Requested page size. Server may return fewer results than requested. If unspecified, the server will pick a default size.
            language (Optional[str]): The language for the product data.
            name (Optional[str]): The product marketing display name to filter on.
            sku_external_id (Optional[str]): The external ID assigned to SKUs.
            addon_external_id (Optional[str]): The external ID assigned to addons.
            sku_id (Optional[str]): The ID of the SKU.
            addon_id (Optional[str]): The ID of the addon.
            sku_display_name (Optional[str]): The display name of the SKU.
            addon_display_name (Optional[str]): The display name of the addon.

        Returns:
            iter: An iterator yielding products.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.products_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.products_v3 = ProductsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.products_v3.list_products(page_size=page_size, language=language, name=name, sku_external_id=sku_external_id, addon_external_id=addon_external_id, sku_id=sku_id, addon_id=addon_id, sku_display_name=sku_display_name, addon_display_name=addon_display_name)

    def get_product(self, product_id: str, language: Optional[str] = "", pricebook_customer_id: Optional[int] = None, product_version: Optional[str] = "", exclude_pricing: Optional[bool] = True, exclude_marketing: Optional[bool] = True, exclude_definition: Optional[bool] = True, exclude_version_history: Optional[bool] = True, exclude_deployment: Optional[bool] = True, client_role: Optional[str] = "CUSTOMER"):
        """
        Retrieve detailed information about a specific product.

        Args:
            product_id (str): The unique identifier of the product.
            language (Optional[str]): The language for the product data.
            pricebook_customer_id (Optional[int]): The customer ID for pricebook filtering.
            product_version (Optional[str]): The version of the product.
            exclude_pricing (Optional[bool]): Whether to exclude pricing information.
            exclude_marketing (Optional[bool]): Whether to exclude marketing information.
            exclude_definition (Optional[bool]): Whether to exclude product definition.
            exclude_version_history (Optional[bool]): Whether to exclude version history.
            exclude_deployment (Optional[bool]): Whether to exclude deployment information.
            client_role (Optional[str]): The role of the client (e.g., "CUSTOMER").

        Returns:
            Dict: A dictionary containing product details.

        Raises:
            StreamOneSDKException: If v3 credentials are not configured.
        """
        if not self.products_v3:
            raise StreamOneSDKException("v3 credentials are not configured.")
        self.refresh_access_token()
        self.products_v3 = ProductsV3(
            self.v3_base_url, self.v3_access_token, self.account_id)
        return self.products_v3.get_product(product_id=product_id, language=language, pricebook_customer_id=pricebook_customer_id, product_version=product_version, exclude_pricing=exclude_pricing, exclude_marketing=exclude_marketing, exclude_definition=exclude_definition, exclude_version_history=exclude_version_history, exclude_deployment=exclude_deployment, client_role=client_role)
