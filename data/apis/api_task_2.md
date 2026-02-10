
**POST** `https://content-api.wildberries.ru/content/v2/cards/upload`

**Примеры запроса**

**Content type:** `application/json`

```json
[
  {
    "subjectID": 105,
    "variants": [
      {
        "vendorCode": "АртикулПродавца",
        "wholesale": {
          "enabled": true,
          "quantum": 211
        },
        "title": "Наименование товара",
        "description": "Описание товара",
        "brand": "Бренд",
        "dimensions": {
          "length": 12,
          "width": 7,
          "height": 5,
          "weightBrutto": 1.242
        },
        "characteristics": [
          {
            "id": 12,
            "value": [
              "Turkish flag"
            ]
          },
          {
            "id": 25471,
            "value": 1200
          },
          {
            "id": 14177449,
            "value": [
              "red"
            ]
          }
        ],
        "sizes": [
          {
            "techSize": "S",
            "wbSize": "42",
            "price": 5000,
            "skus": [
              "88005553535"
            ]
          }
        ]
      }
    ]
  }
]
```

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Request Body schema:** `application/json`

**Примеры ответа**

**200**

```json
{
  "data": null,
  "error": false,
  "errorText": "",
  "additionalErrors": {}
}
```

**400**

```json
{
  "data": null,
  "error": true,
  "errorText": "Invalid request format",
  "additionalErrors": {}
}
```

**401**

```json
{
  "title": "unauthorized",
  "detail": "token problem; token is malformed: could not base64 decode signature: illegal base64 data at input byte 84",
  "code": "07e4668e--a53a3d31f8b0-[UK-oWaVDUqNrKG ]; 03bce=277; 84bd353bf-75",
  "requestId": "7b80742415072fe8b6b7f7761f1d1211",
  "origin": "s2s-api-auth-catalog",
  "status": 401,
  "statusText": "Unauthorized",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**413**

```json
{
  "title": "request body too long",
  "detail": "https://openapi.wildberries.ru/content/api/ru/",
  "code": "71d3de1b-001e-488f-bbf5-55c31254fbeb",
  "requestId": "MN8usr6RfrzWHZfucSvNgb",
  "origin": "s2s-api-auth-content",
  "status": 413,
  "statusText": "Request Entity Too Large"
}
```

**429**

```json
{
  "title": "too many requests",
  "detail": "limited by c122a060-a7fb-4bb4-abb0-32fd4e18d489",
  "code": "07e4668e-ac2242c5c8c5-[UK-4dx7JUdskGZ]",
  "requestId": "9d3c02cc698f8b041c661a7c28bed293",
  "origin": "s2s-api-auth-catalog",
  "status": 429,
  "statusText": "Too Many Requests",
  "timestamp": "2024-09-30T06:52:38Z"
}
```