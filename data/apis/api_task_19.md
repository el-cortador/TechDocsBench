**DELETE** `/iam/v1/service_users/{user_id}/groups`

**Authorizations:**  
iam_token_account_scoped  
API Key: iam_token_account_scoped  
IAM token for account.  
Header parameter name: X-Auth-Token

**Примеры запроса**

```json
{
  "group_ids": [
    "string"
  ]
}
```

**Path Parameters**

| Параметр | Тип |
| --- | --- |
| `user_id` required | string |

**Request Body schema:** `application/json` required

| Параметр | Тип |
| --- | --- |
| `group_ids` | Array of strings |

**Ответы**

**204 No Content**  

**400 Bad Request**  

**Response Schema:** `*/*`

| Поле | Тип |
| --- | --- |
| `code` | string |
| `message` | string |

**401 Unauthorized**  

**404 Not Found**  

**Response Schema:** `*/*`

| Поле | Тип |
| --- | --- |
| `code` | string |
| `message` | string |