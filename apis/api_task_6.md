**POST** `https://api-seller.ozon.ru/v3/product/import`

**Примеры запроса**

*Content type: `application/json`*

```json
{
  "items": [
    {
      "attributes": [
        {
          "complex_id": 0,
          "id": 5076,
          "values": [
            {
              "dictionary_value_id": 971082156,
              "value": "Стойка для акустической системы"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 9048,
          "values": [
            {
              "value": "Комплект защитных плёнок для X3 NFC. Темный хлопок"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 8229,
          "values": [
            {
              "dictionary_value_id": 95911,
              "value": "Комплект защитных плёнок для X3 NFC. Темный хлопок"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 85,
          "values": [
            {
              "dictionary_value_id": 5060050,
              "value": "Samsung"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 10096,
          "values": [
            {
              "dictionary_value_id": 61576,
              "value": "серый"
            }
          ]
        }
      ],
      "barcode": "112772873170",
      "description_category_id": 17028922,
      "new_description_category_id": 0,
      "color_image": "",
      "complex_attributes": [],
      "currency_code": "RUB",
      "depth": 10,
      "dimension_unit": "mm",
      "height": 250,
      "images": [],
      "images360": [],
      "name": "Комплект защитных плёнок для X3 NFC. Темный хлопок",
      "offer_id": "143210608",
      "old_price": "1100",
      "pdf_list": [],
      "price": "1000",
      "primary_image": "",
      "promotions": [
        {
          "operation": "UNKNOWN",
          "type": "REVIEWS_PROMO"
        }
      ],
      "type_id": 91565,
      "vat": "0.1",
      "weight": 100,
      "weight_unit": "g",
      "width": 150
    }
  ]
}
```

**Header Parameters**

| Параметр | Описание |
| --- | --- |
| `Client-Id` required | string  |
| `Api-Key` required | string |

**Примеры ответа**

**200**

```json
{
  "result": {
    "task_id": 172549793
  }
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