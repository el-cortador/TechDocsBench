**POST** `/iam/v1/service_users`

**Authorizations:**  
iam_token_account_scoped  
API Key: iam_token_account_scoped  
IAM token for account.  
Header parameter name: X-Auth-Token

**Примеры запроса**

```json
{
  "description": "string",
  "enabled": true,
  "group_ids": [
    "string"
  ],
  "name": "string",
  "password": "string",
  "roles": [
    {
      "project_id": "string",
      "role_name": "string",
      "scope": "account"
    }
  ]
}
```

**Request Body schema:** `application/json` required

| Параметр | Тип |
| --- | --- |
| `description` | string |
| `enabled` | boolean |
| `group_ids` | Array of strings |
| `name` | string |
| `password` | string |
| `roles` | Array of objects (models.RoleRequest) |
| `project_id` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |

**Ответы**

**200 OK**  

**Response Schema:** `*/*`

| Поле | Тип |
| --- | --- |
| `description` | string |
| `enabled` | boolean |
| `id` | string |
| `name` | string |
| `roles` | Array of objects (models.Role) |
| `project_id` | string |
| `project_name` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |

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

**409 Conflict**  

**Response Schema:** `*/*`

| Поле | Тип |
| --- | --- |
| `code` | string |
| `message` | string |

---