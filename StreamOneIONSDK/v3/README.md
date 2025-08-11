# StreamOne SDK v3 API

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

### Sample Response

```json
[
  {
    "id": "1",
    "name": "accounts/0/customers/1",
    "customerOrganization": "DC 3 June 2024",
    "customerAddress": {
      "street": "123 Main St",
      "city": "Sample City",
      "state": "Sample State",
      "zip": "12345",
      "country": "US"
    },
    "customerName": "John Doe",
    "customerEmail": "john.doe@example.com",
    "customerTitle": "Mr",
    "customerPhone": "123456789",
    "createTime": "2024-06-03T09:55:19Z",
    "updateTime": "2024-06-03T09:55:20Z",
    "languageCode": "EN",
    "uid": "askjd8721nkas",
    "customerStatus": "ACTIVE"
  }
]
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

````python
```json
{
  "name": "accounts/123/products/FakeProduct-es",
  "type": "SUBSCRIPTION_PRODUCT",
  "categories": ["accounts/123/categories/Fake-Category"],
  "hasPublishedVersions": true,
  "marketing": {
    "description": "Fake Product is a scalable service platform designed to modernize applications, accelerate deployment, and drive digital transformation. It includes architecture for various environments and tools to manage resources effectively.",
    "displayName": "Fake Product on Cloud",
    "caption": "Scalable Service Platform on Cloud",
    "defaultImage": {
      "title": "Logo",
      "content": "https://fake-storage.com/fake-data/products/FakeProduct-es/images/logo.png",
      "type": "MEDIA_TYPE_IMAGE"
    }
  },
  "definition": {
    "supportedCurrencies": ["USD"],
    "billingMode": "POSTPAY",
    "features": [
      { "id": "Cost-effective", "displayName": "Cost effective" },
      { "id": "Developer-friendly", "displayName": "Developer friendly" },
      { "id": "Flexible", "displayName": "Flexible" },
      { "id": "Corporate-control", "displayName": "Corporate control" }
    ],
    "skus": [
      {
        "id": "sku--Fake-Product-on-Cloud-n0",
        "displayName": "Fake Product on Cloud",
        "description": "Based on Usage",
        "cancelTiming": "END_OF_TERM",
        "plans": [
          {
            "id": "plan--Fake-Product-on-Cloud-n0",
            "displayName": "Fake Product on Cloud",
            "billingPeriod": "MONTHLY",
            "phases": [{ "type": "UNLIMITED_PHASE", "recurringPrice": { "USD": 0 } }],
            "icon": "https://fake-storage.com/fake-data/products/FakeProduct-es/images/plan_icon.png",
            "supportPlan": {},
            "priceDisplay": "PRICE_DISPLAY_SHOW_PLAN"
          }
        ],
        "productCloudProviderName": "accounts/123/cloudProviders/1",
        "disabled": true,
        "supportPlanAsProductPlan": { "details": {} }
      }
    ],
    "customFields": [
      { "name": "productType", "content": "fakeType", "type": "STRING" },
      { "name": "solutionName", "content": "FakeSolutionV1", "type": "STRING" },
      { "name": "region", "content": "FAKE_REGION", "type": "STRING" },
      { "name": "ProvisioningCategory", "content": "FakeCategory", "type": "STRING" },
      { "name": "disablePriceAdjustment", "content": "true", "type": "STRING" },
      { "name": "skip-price-book", "content": "true", "type": "STRING" }
    ]
  },
  "isSharedProduct": true,
  "etag": "FAKE_ETAG",
  "createTime": "2024-01-01T00:00:00Z",
  "updateTime": "2024-01-02T00:00:00Z"
}
````

## Getting Product Details

The `get_product` method retrieves detailed information for a specific product.

### Example

```python
product_detail = client.get_product(product["id"], exclude_pricing=False, client_role="OWNER")
print(product_detail)
```

#### Sample Response

````python
```json
{
  "id": "FAKE-ID-12345",
  "name": "accounts/999/products/FAKE-PRODUCT",
  "type": "SUBSCRIPTION_PRODUCT",
  "categories": [
    "accounts/999/categories/FAKE-CATEGORY"
  ],
  "hasPublishedVersions": true,
  "idsInUse": [
    "FAKE-ID-12345",
    "Fake-Plan-1",
    "Fake-Plan-2"
  ],
  "termUid": "FAKE-TERM-UID-12345",
  "previewAuthToken": "/+blob-signature+/FAKE-TOKEN-12345+FAKE-TOKEN-67890=",
  "etag": "FAKE-ETAG-12345",
  "tagsValues": [
    {
      "name": "accounts/999/product/tags/999/value/1001",
      "displayName": "Fake Tag 1",
      "tagDisplayName": "tag",
      "tagName": "accounts/999/product/tags/999"
    },
    {
      "name": "accounts/999/product/tags/999/value/1002",
      "displayName": "Fake Tag 2",
      "tagDisplayName": "tag",
      "tagName": "accounts/999/product/tags/999"
    },
    {
      "name": "accounts/999/product/tags/999/value/1003",
      "displayName": "Fake Tag 3",
      "tagDisplayName": "tag",
      "tagName": "accounts/999/product/tags/999"
    },
    {
      "name": "accounts/999/product/tags/999/value/1004",
      "displayName": "Fake Tag 4",
      "tagDisplayName": "tag",
      "tagName": "accounts/999/product/tags/999"
    }
  ],
  "createTime": "2020-01-01T00:00:00Z",
  "updateTime": "2025-01-01T00:00:00Z",
  "legacyProductId": "FAKE-LEGACY-ID-12345"
}
````

````

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
    subscriptionStatus="ACTIVE",
    startDateRange={"relativeDateRange": "MONTH_TO_DATE"},
    pageSize=5
)
for subscription in subscriptions:
    print(subscription)
````

### Sample Response

```json
{
  "id": "5555",
  "customerId": "12345",
  "resellerId": "222",
  "isvId": "222",
  "cloudProviderId": "99",
  "subscriptionId": "abc12345-def6-7890-ghij-klmnopqrstuv",
  "subscriptionName": "Fake Subscription Plan",
  "resourceType": "FAKE::Resource",
  "ccpProductId": "FAKEPROD-001",
  "ccpSkuId": "FAKESKU-002",
  "ccpPlanId": "FakePlan-003",
  "subscriptionProductId": "FAKEPRODID",
  "subscriptionSkuId": "FAKESKUID",
  "subscriptionOfferId": "FAKEPRODID:FAKESKUID:FAKEOFFERID",
  "unitType": "Licenses",
  "subscriptionStatus": "active",
  "subscriptionPurchasedDate": "2024-02-01T00:00:00Z",
  "subscriptionStartDate": "2024-02-01T00:00:00Z",
  "subscriptionEndDate": "2025-02-01T00:00:00Z",
  "cancellationAllowedUntilDate": "2024-02-10T00:00:00Z",
  "subscriptionBillingType": "license",
  "subscriptionBillingCycle": "monthly",
  "subscriptionBillingTerm": "P1M",
  "subscriptionRenewStatus": "ENABLED",
  "ccpProductInfo": {
    "productId": "FAKEPROD-001",
    "productDisplayName": "Fake Product",
    "skuId": "FAKESKU-002",
    "skuDisplayName": "Fake SKU",
    "planId": "FakePlan-003",
    "planDisplayName": "Fake Plan"
  },
  "isTrial": false,
  "autoRenew": true,
  "customerName": "Fake Customer",
  "partnerName": "Fake Partner",
  "lastUpdatedDate": "2024-02-01T00:00:00Z",
  "price": 49.99,
  "cost": 39.99,
  "currency": "USD",
  "margin": 10,
  "total": 49.99,
  "msrp": 60.0,
  "renewalDate": "2025-02-01T00:00:00Z",
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
    subscriptionId="59a53ae5-9abf-4002-dbbc-714dee01dffd",
    refresh=True
)
print(subscription_details)
```

### Sample Response

```json
{
  "id": "9999",
  "customerId": "1",
  "resellerId": "888",
  "isvId": "888",
  "cloudProviderId": "77",
  "subscriptionId": "59a53ae5-9abf-4002-dbbc-714dee01dffd",
  "subscriptionName": "Fake Subscription",
  "resourceType": "FAKE::Resource",
  "ccpProductId": "FAKEPROD-123",
  "ccpSkuId": "FAKESKU-456",
  "ccpPlanId": "FakePlan-789",
  "subscriptionProductId": "FAKEPRODID",
  "subscriptionSkuId": "FAKESKUID",
  "subscriptionOfferId": "FAKEPRODID:FAKESKUID:FAKEOFFERID",
  "unitType": "Licenses",
  "subscriptionStatus": "active",
  "subscriptionPurchasedDate": "2024-01-01T00:00:00Z",
  "subscriptionStartDate": "2024-01-01T00:00:00Z",
  "subscriptionEndDate": "2025-01-01T00:00:00Z",
  "cancellationAllowedUntilDate": "2024-01-10T00:00:00Z",
  "subscriptionBillingType": "license",
  "subscriptionBillingCycle": "monthly",
  "subscriptionBillingTerm": "P1M",
  "subscriptionRenewStatus": "ENABLED",
  "activityLogs": {},
  "ccpProductInfo": {
    "productId": "FAKEPROD-123",
    "productDisplayName": "Fake Product",
    "skuId": "FAKESKU-456",
    "skuDisplayName": "Fake SKU",
    "planId": "FakePlan-789",
    "planDisplayName": "Fake Plan"
  },
  "isTrial": false,
  "autoRenew": true,
  "customerName": "Fake Customer",
  "partnerName": "Fake Partner",
  "lastUpdatedDate": "2024-01-01T00:00:00Z",
  "price": 99.99,
  "cost": 89.99,
  "currency": "USD",
  "margin": 10,
  "total": 99.99,
  "msrp": 120.0,
  "renewalDate": "2025-01-01T00:00:00Z",
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
    report_module="REPORTS_REPORTS_MODULE",
    category="BILLING_REPORTS",
    relative_date_range="MONTH_TO_DATE",
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
  "referenceId": "customers/4567/carts/112",
  "displayName": "Cart - 1715100000000",
  "userId": "5432",
  "userName": "Test User Account",
  "userEmail": "testuser@example.com",
  "status": "ON_HOLD",
  "currencyCode": "EUR",
  "cartId": "112",
  "orderItems": [
    {
      "name": "accounts/123/customers/4567/orders/891011/orderItems/121314",
      "referenceId": "customers/4567/cartItems/151",
      "action": "CREATE",
      "productId": "GenericProd-DB",
      "skuId": "Fake-Software-Database-Lrg",
      "planId": "Standard-Monthly-Plan",
      "quantity": 2,
      "providerName": "UNSPECIFIED",
      "cartItemId": "151",
      "status": "ACTIVE",
      "additionalInformation": "new_system",
      "createTime": "2023-01-15T09:30:00Z",
      "updateTime": "2025-03-10T10:15:30Z",
      "isEligibleForPromo": "VERIFIED",
      "productName": "Fake Corp Generic Database Service",
      "skuName": "Fake Corp Premium Database License",
      "planName": "Fake Corp Premium Database License",
      "productOwnerCountryCode": "DE"
    }
  ],
  "createTime": "2023-01-15T09:29:50Z",
  "updateTime": "2023-01-15T09:35:10Z",
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
orders = client.list_customer_orders(
    customer_id=1,
    page_size="10",
    status="ON_HOLD",
)
for order in orders:
  print(order)
```

### Sample Response

```json
{
  "name": "accounts/123/customers/1/orders/891011",
  "referenceId": "customers/4567/carts/112",
  "displayName": "Cart - 1715100000000",
  "userId": "5432",
  "userName": "Test User Account",
  "userEmail": "testuser@example.com",
  "status": "ON_HOLD",
  "currencyCode": "EUR",
  "cartId": "112",
  "orderItems": [
    {
      "name": "accounts/123/customers/4567/orders/891011/orderItems/121314",
      "referenceId": "customers/4567/cartItems/151",
      "action": "CREATE",
      "productId": "GenericProd-DB",
      "skuId": "Fake-Software-Database-Lrg",
      "planId": "Standard-Monthly-Plan",
      "quantity": 2,
      "providerName": "UNSPECIFIED",
      "cartItemId": "151",
      "status": "ACTIVE",
      "additionalInformation": "new_system",
      "createTime": "2023-01-15T09:30:00Z",
      "updateTime": "2025-03-10T10:15:30Z",
      "isEligibleForPromo": "VERIFIED",
      "productName": "Fake Corp Generic Database Service",
      "skuName": "Fake Corp Premium Database License",
      "planName": "Fake Corp Premium Database License",
      "productOwnerCountryCode": "DE"
    }
  ],
  "createTime": "2023-01-15T09:29:50Z",
  "updateTime": "2023-01-15T09:35:10Z",
  "scheduledAt": "2023-01-15T09:35:10Z"
}
```

---

## API Documentation

For more details, refer to the [StreamOne API Documentation](https://docs.streamone.cloud/#end-customer).
