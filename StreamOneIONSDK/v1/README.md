# StreamOne SDK v1 API

**Note:** The v1 API will be deprecated soon. Please migrate to the v3 API.

## Getting My Invoices (v1)

```python
filters: dict = {
    'billingStartDate': {'value': '2025-01-01', 'modifier': 'gte'},
    'billingEndDate': {'value': '2025-02-01', 'modifier': 'lt'},
}
sort: dict = {
    'id': 'asc',
    'cloudUsed': 'desc'
}
relations: list = [
    'lines'
]
invoices: dict = client.get_my_invoices(filters=filters, sort=sort, limit=1000, offset=0, relations=relations)
print(invoices)
```

## Getting Customer Invoices (v1)

```python
customer_id: str = '12345'  # Replace with actual customer ID
filters: dict = {
    'billingStartDate': {'value': '2024-12-01', 'modifier': 'gt'},
}
customer_invoices: dict = client.get_customer_invoices(customer_id=customer_id, filters=filters, limit=100, offset=0)
print(customer_invoices)
```

## Getting Detailed Invoice Data (v1)

```python
detailed_invoice: dict = client.get_detailed_invoice_data(invoice_id='123', save_folder='path/to/save/folder')
print(detailed_invoice)
```

## Getting Customers (v1)

```python
filters: dict = {
    'email': {'value': 'xyz@abc.com'},
}
relations: list = [
    'customFieldsValues'
]
customers: dict = client.get_customers_v1(filters=filters, relations=relations, limit=100, offset=0)
print(customers)
```

## Generating Invoices (v1)

```python
response: dict = client.generate_invoices(source='aws', period='m-01-2025')
print(response)
```

## Filtering Results (v1)

When requesting a list of entities, the results can be filtered by the values of different fields of the requested entity.

The filter modifier is optional and, when present, changes the way the filter value is used to filter the entities. Possible values are:

| Filter   | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| exact    | (default) The entity field value must be the same as the filter value       |
| partial  | The entity field value may only partially match the filter value.           |
| gt       | Matches all values that are greater than the filter value                   |
| lt       | Matches all values that are lower than the filter value                     |
| gte      | Matches all values that are greater than or equal to the filter value       |
| lte      | Matches all values that are lower than or equal to the filter value         |
| min      | Matches all values that are greater than or equal to the filter value (gte) |
| max      | Matches all values that are lower than or equal to the filter value (lte)   |

## Creating the Filtering Dictionary (v1)

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
