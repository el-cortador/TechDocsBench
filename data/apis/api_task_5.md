**POST** `https://seller-analytics-api.wildberries.ru/api/v2/search-report/product/search-texts`

**Пример запроса**

**Content type**  
`application/json`

```json
{
  "currentPeriod": {
    "start": "2024-02-10",
    "end": "2024-02-10"
  },
  "pastPeriod": {
    "start": "2024-02-08",
    "end": "2024-02-08"
  },
  "nmIds": [
    162579635,
    166699779
  ],
  "topOrderBy": "openToCart",
  "includeSubstitutedSKUs": true,
  "includeSearchTexts": false,
  "orderBy": {
    "field": "avgPosition",
    "mode": "asc"
  },
  "limit": 20
}
```

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Request Body schema:** `application/json` required

**Примеры ответа**

**200**

```json
{
  "data": {
    "items": [
      {
        "text": "костюм",
        "nmId": 211131895,
        "subjectName": "Phones",
        "brandName": "Apple",
        "vendorCode": "wb3ha2668w",
        "name": "iPhone 13 256 ГБ Серебристый",
        "isCardRated": true,
        "rating": 6,
        "feedbackRating": 1,
        "price": {
          "minPrice": 150,
          "maxPrice": 300
        },
        "frequency": {
          "current": 5,
          "dynamics": 50
        },
        "weekFrequency": 140,
        "medianPosition": {
          "current": 5,
          "dynamics": 50
        },
        "avgPosition": {
          "current": 5,
          "dynamics": 50
        },
        "openCard": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "addToCart": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "openToCart": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "orders": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "cartToOrder": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "visibility": {
          "current": 5,
          "dynamics": 50
        }
      }
    ]
  }
}
```

**400**

```json
{
  "title": "Invalid request body",
  "detail": "code=400, message=invalid: positionCluster (field required), limit (field required), offset (field required), internal=invalid: positionCluster (field required), limit (field required), offset (field required",
  "requestId": "fb25c9e9-cae8-52db-b68e-736c1466a3f5",
  "origin": "analytic-open-api"
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

**403**

```json
{
  "title": "Authorization error",
  "detail": "Authorization error",
  "requestId": "fb25c9e9-cae8-52db-b68e-736c1466a3f5",
  "origin": "analytic-open-api"
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