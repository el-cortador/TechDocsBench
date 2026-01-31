**GET** `https://postgresql.api.cloud.ru/v1/clusters/{cluster_id}/users`

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `cluster_id` required | string |

**Примеры ответа**

**200**

```json
{
  "users": [
    {
      "name": "string",
      "supported_roles": [
        {
          "name": "string"
        }
      ],
      "granted_roles": [
        {
          "name": "string"
        }
      ]
    }
  ]
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