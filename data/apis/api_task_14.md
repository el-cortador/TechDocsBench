**GET** `https://postgresql.api.cloud.ru/v1/operations/{operation_id}`

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `operation_id` required | string |

**Примеры ответа**

**200**

```json
{
  "id": "string",
  "resource_name": "urn:cloud:postgresql::265c6f28-9c84-4cef-bbc5-4472c1743bc0:backend",
  "resource_id": "54295782-7aef-43e6-b33b-c9735938677a",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "done": true,
  "description": "string",
  "error": {
    "code": 0,
    "message": "string",
    "details": [
      {
        "@type": "string"
      }
    ]
  }
}
```

**default**

```json
{
  "code": 0,
  "message": "string",
  "details": [
    {
      "@type": "string"
    }
  ]
}
```