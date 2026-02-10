**GET** `https://api-seller.ozon.ru/v1/product/certificate/accordance-types`

**Header Parameters**

| Параметр | Описание |
| --- | --- |
| `Client-Id` required | string |
| `Api-Key` required | string |

**Примеры ответа**

**200**

```json
{
  "result": [
    {
      "name": "ГОСТ",
      "value": "gost"
    },
    {
      "name": "Технический регламент РФ",
      "value": "technical_regulations_rf"
    },
    {
      "name": "Технический регламент ТС",
      "value": "technical_regulations_cu"
    }
  ]
}
```

**400**

```json
{
  "code": 0,
  "details": [
    {
      "typeUrl": "string",
      "value": "string"
    }
  ],
  "message": "string"
}
```

**403**

```json
{
  "code": 0,
  "details": [
    {
      "typeUrl": "string",
      "value": "string"
    }
  ],
  "message": "string"
}
```

**404**

```json
{
  "code": 0,
  "details": [
    {
      "typeUrl": "string",
      "value": "string"
    }
  ],
  "message": "string"
}
```

**409**

```json
{
  "code": 0,
  "details": [
    {
      "typeUrl": "string",
      "value": "string"
    }
  ],
  "message": "string"
}
```

**500**

```json
{
  "code": 0,
  "details": [
    {
      "typeUrl": "string",
      "value": "string"
    }
  ],
  "message": "string"
}
```