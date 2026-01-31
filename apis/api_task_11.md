**GET** `https://baremetal.api.cloud.ru/v2/distributions`

**Query Parameters**

| Параметр | Описание |
| --- | --- |
| `page_size` | string `<int64>` |
| `page_token` | string |
| `filter` | string |

**Примеры ответа**

**200**

```json
{
  "distributions": [
    {
      "name": "string",
      "slug": "string",
      "kernels": [
        {
          "name": "string",
          "slug": "string",
          "os_type": "OS_TYPE_UNSPECIFIED",
          "pricing_model": "PRICING_MODEL_UNSPECIFIED",
          "description": "string"
        }
      ]
    }
  ],
  "next_page_token": "string"
}
```

**default**

```json
{
  "code": 0,
  "message": "string",
  "details": [
    {
      "@type": "string",
      "property1": {},
      "property2": {}
    }
  ]
}
```