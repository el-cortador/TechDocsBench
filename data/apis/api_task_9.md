**POST** `https://api-seller.ozon.ru/v1/warehouse/list`

**Примеры запроса**

```json
{
  "limit": 0,
  "offset": 0
}
```

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
      "has_entrusted_acceptance": true,
      "is_rfbs": true,
      "name": "string",
      "warehouse_id": 0,
      "can_print_act_in_advance": true,
      "first_mile_type": {
        "dropoff_point_id": "string",
        "dropoff_timeslot_id": 0,
        "first_mile_is_changing": true,
        "first_mile_type": "DropOff"
      },
      "has_postings_limit": true,
      "is_karantin": true,
      "is_kgt": true,
      "is_economy": true,
      "is_timetable_editable": true,
      "min_postings_limit": 0,
      "postings_limit": 0,
      "min_working_days": 0,
      "status": "string",
      "working_days": [
        "1"
      ]
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