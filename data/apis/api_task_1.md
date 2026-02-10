**Пример запроса:**

```json
{
  "client_id": "string",
  "client_secret": "string",
  "code": "string",
  "grant_type": "string",
  "redirect_uri": "string",
  "refresh_token": "string"
}
```

**Request Body schema:** `application/json`

**Примеры ответа:**

**200 Токен доступа**

```json
{
  "access_token": "string",
  "expires_in": 0,
  "refresh_token": "string",
  "scope": [
    "string"
  ],
  "token_type": "string"
}
```

**Default Ошибка**

```json
{
  "code": 0,
  "details": [
    {
      "@type": "string"
    }
  ],
  "message": "string"
}
```