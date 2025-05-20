# StreamOne SDK

This is a Python SDK for interacting with the StreamOne API.

## Installation

To install the SDK, run the following command:

```bash
pip install .
```

## Authentication

The StreamOne Ion API uses Basic HTTP Authentication. You will use the StreamOne Ion API Key as the Username and API Secret as the Password in your requests.

The API Key and API Secret can be found in your Admin Portal account. After logging into your Admin Portal account, select the Settings option from either the landing page (distributor view) or from the menu on the top right of the screen (partner view). Under Account settings, select the first tab Account Information. API Key and API Secret will display at the bottom of the page. You can view existing API keys or generate new ones.

## Configuration

The SDK requires a configuration file in JSON format. The structure of the configuration file should be as follows:

```json
{
  "v1": {
    "api_key": "your_v1_api_key",
    "api_secret": "your_v1_api_secret"
  },
  "v3": {
    "access_token": "your_v3_access_token",
    "refresh_token": "your_v3_refresh_token"
  },
  "accountid": "your_account_id"
}
```

## Usage

### Initializing the Client

```python
from StreamOneSDK.client import StreamOneClient

client = StreamOneClient(config='path/to/config.json')
```

---

# v1 API (Deprecated Soon)

**Note:** The v1 API will be deprecated soon. Please migrate to the v3 API.

## Getting My Invoices (v1)

```python
filters = {
    'billingStartDate': {'value': '2025-01-01', 'modifier': 'gte'},
    'billingEndDate': {'value': '2025-02-01', 'modifier': 'lt'},
}
sort = {
    'id': 'asc',
    'cloudUsed': 'desc'
}
relations = [
    'lines'
]
invoices = client.get_my_invoices(filters=filters, sort=sort, limit=1000, offset=0, relations=relations)
print(invoices)
```

## Getting Customer Invoices (v1)

```python
customer_id = '12345'  # Replace with actual customer ID
filters = {
    'billingStartDate': {'value': '2024-12-01', 'modifier': 'gt'},
}
customer_invoices = client.get_customer_invoices(customer_id=customer_id, filters=filters, limit=100, offset=0)
print(customer_invoices)
```

## Getting Detailed Invoice Data (v1)

```python
detailed_invoice = client.get_detailed_invoice_data(invoice_id='123', save_folder='path/to/save/folder')
print(detailed_invoice)
```

## Getting Customers (v1)

```python
filters = {
    'email': {'value': 'xyz@abc.com'},
}
relations = [
    'customFieldsValues'
]
customers = client.get_customers_v1(filters=filters, relations=relations, limit=100, offset=0)
print(customers)
```

## Generating Invoices (v1)

```python
response = client.generate_invoices(source='aws', period='m-01-2025')
print(response)
```

## Filtering Results (v1)

When requesting a list of entities, the results can be filtered by the values of different fields of the requested entity.

The filter modifier is optional and, when present, changes the way the filter value is used to filter the entities. Possible values are:

| Filter  | Description                                                                 |
| ------- | --------------------------------------------------------------------------- |
| exact   | (default) The entity field value must be the same as the filter value       |
| partial | The entity field value may only partially match the filter value.           |
| gt      | Matches all values that are greater than the filter value                   |
| lt      | Matches all values that are lower than the filter value                     |
| gte     | Matches all values that are greater than or equal to the filter value       |
| lte     | Matches all values that are lower than or equal to the filter value         |
| min     | Matches all values that are greater than or equal to the filter value (gte) |
| max     | Matches all values that are lower than or equal to the filter value (lte)   |

### Creating the Filtering Dictionary (v1)

To create the filtering dictionary, use the following format:

```python
filters = {
    'FIELD_NAME': {'value': 'FIELD_VALUE', 'modifier': 'MODIFIER'}
}
```

- `FIELD_NAME`: The name of the field to filter by.
- `FIELD_VALUE`: The value to filter by.
- `MODIFIER`: The filter modifier (optional). If not provided, the default is `exact`.

Example:

The following filters will find all the entities with name “John Doe” in the group with ID=23:

```python
filters = {
    'name': {'value': 'John Doe'},
    'groupId': {'value': '23'}
}
```

The following filters will find all the entities that have the name starting with "Jo":

```python
filters = {
    'name': {'value': 'Jo%', 'modifier': 'partial'}
}
```

## Sorting Results (v1)

You can specify the sort fields using the sort parameter.

### Creating the Sorting Dictionary (v1)

To create the sorting dictionary, use the following format:

```python
sort = {
    'FIELD_NAME': 'asc|desc'
}
```

- `FIELD_NAME`: The name of the field to sort by.
- `asc|desc`: The sort order, either `asc` for ascending or `desc` for descending.

Example:

The following sorting dictionary will sort the results first by name ascending, then by company descending:

```python
sort = {
    'name': 'asc',
    'company': 'desc'
}
```

## Paging the Results (v1)

The number of results per request can be limited using the limit parameter and the results offset within the entire results set can be specified using the offset parameter. Using these two parameters you can paginate the results for a large list of entities.

By default, the limit parameter is set to 100 and the offset parameter is set to 0 (zero).

## Creating the Relations List (v1)

**Note:** The `relations` parameter is limited to the v1 API.

To create the relations list, use the following format:

```python
relations = [
    'RELATED_ENTITY_1',
    'RELATED_ENTITY_2'
]
```

- `RELATED_ENTITY_1`, `RELATED_ENTITY_2`: The names of the related entities to return.

Example:

The following relations list will include the related invoices and group entities:

```python
relations = [
    'invoices',
    'group'
]
```

---

## Customizing the Results

The StreamOne Ion API offers the possibility to customize the returned fields for the requested entities.

---

# v3 API

## Initializing the Client

```python
from StreamOneSDK.client import StreamOneClient

client = StreamOneClient(config='path/to/config.json')
```

## Getting Customers

```python
customers = client.list_customers(pageSize=10, customerEmail='example@example.com')
for customer in customers:
    print(customer)
```

### Examples

```python
# List customers with a page size of 20
customers = client.list_customers(pageSize=20)
for customer in customers:
    print(customer)

# List customers with a specific email
customers = client.list_customers(pageSize=100, customerEmail="john.doe@example.com")
for customer in customers:
    print(customer)

# List active customers with a specific language code
customers = client.list_customers(pageSize=100, languageCode="EN", customerStatus="ACTIVE")
for customer in customers:
    print(customer)

# List customers with a specific name
customers = client.list_customers(pageSize=100, customerName="John Doe")
for customer in customers:
    print(customer)
```

## Getting a Specific Customer

```python
customer = client.get_customer(customerId='12345')
print(customer)
```

## Listing Products

The `list_products` method allows you to retrieve a list of products with optional filtering and automatic pagination.

### Example

```python
for product in client.list_products(page_size=3):
    print(product)
```

#### Sample Response

```json
{
  "name": "accounts/123/products/FakeProduct-es",
  "updateTime": "2024-01-02T00:00:00Z"
}
```

## Getting Product Details

The `get_product` method retrieves detailed information for a specific product.

### Example

```python
product_detail = client.get_product(product["id"], exclude_pricing=False, client_role="OWNER")
print(product_detail)
```

#### Sample Response

```json
{
  "id": "FAKE-ID-12345",
  "legacyProductId": "FAKE-LEGACY-ID-12345"
}
```

## Listing Subscriptions

The `list_subscriptions` method allows you to retrieve a list of subscriptions with various filtering and sorting options.

### Parameters

| Parameter          | Data Type | Description                                                  | Example                                    | Required |
| ------------------ | --------- | ------------------------------------------------------------ | ------------------------------------------ | -------- |
| customerId         | String    | The unique customer ID.                                      | `12345`                                    | No       |
| subscriptionId     | String    | The unique subscription ID.                                  | `12345`                                    | No       |
| resellerId         | Integer   | The unique reseller ID.                                      | `12345`                                    | No       |
| providerId         | Integer   | The unique cloud provider ID.                                | `12345`                                    | No       |
| subscriptionStatus | String    | The current status of the subscription.                      | `ACTIVE`                                   | No       |
| startDateRange     | Dict      | The relative or fixed start date range of the subscriptions. | `{"relativeDateRange": "MONTH_TO_DATE"}`   | No       |
| endDate            | String    | The time when the subscription ends in ISO 8601 format.      | `2023-10-17T09:48:16Z`                     | No       |
| endDateRange       | Dict      | The relative or fixed end date range of the subscriptions.   | `{"fixedDateRange": {"startDate": "..."}}` | No       |
| billingTerm        | String    | The period for which the subscription service is active.     | `Monthly`                                  | No       |
| totalLicense       | String    | The total number of subscriptions available for the account. | `1`                                        | No       |
| ccpProductId       | String    | The unique product ID in the CCP catalog.                    | `TechDataAzureSentinel-smp`                | No       |
| providerProductId  | String    | The unique product ID in the provider catalog.               | `Microsoft-product-id`                     | No       |
| customerPo         | String    | The end customer's purchase order.                           | `customerpurchaseorder`                    | No       |
| resellerPo         | String    | The reseller's purchase order.                               | `resellerpurchaseorder`                    | No       |
| customField        | Dict      | Filter CustomerCustomFields attributes (key-value pairs).    | `{"field": "domainName", "value": "..."}`  | No       |
| cloudProviderName  | String    | Name of the cloud provider (e.g., AWS, GCP).                 | `AWS`                                      | No       |
| accountName        | String    | Name of the account.                                         | `Account Name`                             | No       |
| customerName       | String    | Name of the customer.                                        | `John Doe`                                 | No       |
| subscriptionName   | String    | Name of the subscription.                                    | `Microsoft-subscription`                   | No       |
| resourceType       | String    | The resource type identifier within the subscriptions.       | `AWS::Resource`                            | No       |
| pageSize           | Integer   | Number of results per page.                                  | `10`                                       | No       |
| filter             | String    | Additional filtering options.                                | `status:ACTIVE`                            | No       |
| sortBy             | String    | Field to sort by.                                            | `name`                                     | No       |
| sortOrder          | String    | Sort order (`asc` or `desc`).                                | `asc`                                      | No       |
| userId             | Integer   | The user ID for filtering.                                   | `123`                                      | No       |

### Subscription Status Options

The `subscriptionStatus` parameter supports the following values:

- ACCEPTED
- ACTIVE
- AVAILABLE
- CANCELLED
- COMPLETE
- CONFIRMED
- DELETED
- DISABLED
- ENABLED
- ERROR
- EXPIRED
- FAILED
- INITIATED
- IN_PROGRESS
- PAUSED
- PENDING
- RUNNING
- STOPPED
- SUSPENDED

### Relative Date Range Options

The `startDateRange.relativeDateRange` and `endDateRange.relativeDateRange` parameters support the following values:

- UNKNOWN_RELATIVE_DATE_RANGE
- TODAY
- MONTH_TO_DATE
- QUARTER_TO_DATE
- YEAR_TO_DATE
- LAST_MONTH
- LAST_QUARTER
- LAST_YEAR
- LATEST_MONTH
- WEEK_TO_DATE
- LAST_WEEK
- TWO_MONTHS_AGO

### Example

```python
subscriptions = client.list_subscriptions(
    customerId="12345",
    pageSize=5
)
for subscription in subscriptions:
    print(subscription)
```

### Sample Response

```json
{
  "id": "5555",
  "mfgPartNumber": "FAKEPRODID:FAKESKUID:P1M:M"
}
```

**Note:** In v3 endpoints, methods return an iterable object that handles pagination automatically.

## Getting Customer Subscription Details

The `get_customer_subscription_details` method retrieves details of a specific subscription for a customer.

### Parameters

| Parameter      | Data Type | Description                                  | Example                                | Required |
| -------------- | --------- | -------------------------------------------- | -------------------------------------- | -------- |
| customerId     | String    | The unique customer ID.                      | `9072`                                 | Yes      |
| subscriptionId | String    | The unique subscription ID.                  | `59a53ae5-9abf-4002-dbbc-714dee01dffd` | Yes      |
| refresh        | Boolean   | If True, updates the results (default None). | `True`                                 | No       |

### Example

```python
subscription_details = client.get_customer_subscription_details(
    customerId="1",
    refresh=True
)
print(subscription_details)
```

### Sample Response

```json
{
  "id": "9999",
  "mfgPartNumber": "FAKEPRODID:FAKESKUID:P1M:M"
}
```

## Listing Reports

The `list_reports` method allows you to retrieve a list of reports for a specific module.

### Parameters

| Parameter | Data Type | Description                                 | Example                      | Required |
| --------- | --------- | ------------------------------------------- | ---------------------------- | -------- |
| module    | String    | The module for which reports are retrieved. | `REPORTS_MODULE_UNSPECIFIED` | No       |

### Example

```python
reports = client.list_reports(module="REPORTS_MODULE_UNSPECIFIED")
for report in reports:
    print(report)
```

### Sample Response

```json
[
  {
    "reportId": "12345",
    "displayName": "AWS Billing Report",
    "category": "BILLING_REPORTS",
    "createdBy": "admin@example.com",
    "lastUpdatedBy": "editor@example.com",
    "createTime": "2024-06-01T12:00:00Z",
    "reportTemplateId": "template_001",
    "reportModule": "REPORTS_REPORTS_MODULE"
  }
]
```

**Note:** The `list_reports` method returns a list of reports filtered by the specified module. If no module is specified, it defaults to `REPORTS_MODULE_UNSPECIFIED`.

---

## Fetching Report Data in CSV Format

The `get_report_data_csv` method allows you to fetch report data in CSV format and save it to a file.

### Parameters

| Parameter           | Data Type | Description                                                               | Example                  | Required |
| ------------------- | --------- | ------------------------------------------------------------------------- | ------------------------ | -------- |
| report_id           | String    | The ID of the report.                                                     | `12345`                  | Yes      |
| report_module       | String    | The module that uses the reports service.                                 | `REPORTS_REPORTS_MODULE` | Yes      |
| category            | String    | The type of report produced.                                              | `BILLING_REPORTS`        | Yes      |
| start_date          | String    | The start date for the report data in ISO 8601 format.                    | `2024-01-01T00:00:00Z`   | No       |
| end_date            | String    | The end date for the report data in ISO 8601 format.                      | `2024-01-31T23:59:59Z`   | No       |
| relative_date_range | String    | A relative date range (e.g., `MONTH_TO_DATE`, `LAST_MONTH`).              | `MONTH_TO_DATE`          | No       |
| path                | String    | The file path where the CSV data will be saved. Defaults to `report.csv`. | `path/to/report.csv`     | No       |

### Example

```python
csv_path = client.get_report_data_csv(
    report_id="12345",
    path="billing_report.csv"
)
print(f"Report saved to: {csv_path}")
```

### Notes

- If `relative_date_range` is provided, `start_date` and `end_date` are ignored.
- The method saves the CSV data to the specified file path and returns the path.

---

## Fetching Account Order Data

The `list_account_orders` method allows you to fetch report data in CSV format and save it to a file.

### Parameters

| Parameter | Data Type | Description                          | Example     | Required |
| --------- | --------- | ------------------------------------ | ----------- | -------- |
| page_size | Integer   | The size of page to request.         | `10`        | No       |
| status    | String    | The status of the orders to request. | `COMPLETED` | No       |

### Example

```python
orders = client.list_account_orders(
    page_size="10",
    status="ON_HOLD",
)
for order in orders:
  print(order)
```

### Sample Response

```json
{
  "name": "accounts/123/customers/4567/orders/891011",
  "scheduledAt": "2023-01-15T09:35:10Z"
}
```

---

## Fetching Customer Order Data

The `list_account_orders` method allows you to fetch report data in CSV format and save it to a file.

### Parameters

| Parameter   | Data Type | Description                               | Example     | Required |
| ----------- | --------- | ----------------------------------------- | ----------- | -------- |
| customer_id | Integer   | The id of the customer to get orders for. | `10`        | Yes      |
| page_size   | Integer   | The size of page to request.              | `10`        | No       |
| status      | String    | The status of the orders to request.      | `COMPLETED` | No       |

### Example

```python
# Example usage for fetching customer order data
orders = client.list_account_orders(customer_id=10, page_size=10, status="COMPLETED")
for order in orders:
    print(order)
```

---

## Response Format

StreamOne Ion API offers two encoding formats for the response: JSON and XML. By default, the responses are encoded in JSON but you can change that using the Accept request header:

```http
Accept: text/xml
Accept: application/json (default)
```
