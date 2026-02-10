**GET** `https://advert-api.wildberries.ru/adv/v1/promotion/count`

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Примеры ответа**

**200**

```json
{
  "adverts": [
    {
      "type": 9,
      "status": 8,
      "count": 3,
      "advert_list": [
        {
          "advertId": 6485174,
          "changeTime": "2023-05-10T12:12:52.676254+03:00"
        },
        {
          "advertId": 6500443,
          "changeTime": "2023-05-10T17:08:46.370656+03:00"
        },
        {
          "advertId": 7936341,
          "changeTime": "2023-07-12T15:51:08.367478+03:00"
        }
      ]
    }
  ],
  "all": 3
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