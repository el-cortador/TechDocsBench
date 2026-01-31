**POST** `https://api-seller.ozon.ru/v1/chat/send/file`

**Примеры запроса**

```json
{
  "base64_content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
  "chat_id": "99feb3fc-a474-469f-95d5-268b470cc607",
  "name": "tempor"
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
  "result": "success"
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