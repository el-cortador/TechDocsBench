**PATCH** `/iam/v1/groups/{group_id}`

**Authorizations:**  
iam_token_account_scoped  
API Key: iam_token_account_scoped  
IAM token for account.  
Header parameter name: X-Auth-Token

**Примеры запроса**

```json
{
  "description": "string",
  "name": "string"
}
```

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `group_id` required | string |

| Параметр | Описание |
| --- | --- |
| `description` | string |
| `name` | string |

**Ответы**

**200 OK**

**Response Schema:** `*/*`

| Поле | Тип |
| --- | --- |
| `description` | string |
| `id` | string |
| `name` | string |
| `roles` | Array of objects (models.Role) |
| `project_id` | string |
| `project_name` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |
| `service_users` | Array of objects (models.ServiceUserResponse) |
| `description` | string |
| `enabled` | boolean |
| `id` | string |
| `name` | string |
| `roles` | Array of objects (models.Role) |
| `project_id` | string |
| `project_name` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |
| `users` | Array of objects (models.UserResponse) |
| `auth_type` | string (models.UserAuthType) Enum: "local" "federated" |
| `description` | string |
| `federation` | object (models.FederationInfo) |
| `id` | string |
| `keystone_id` | string |
| `roles` | Array of objects (models.Role) |
| `project_id` | string |
| `project_name` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |

**401 Unauthorized**

**404 Not Found**

**Response Schema:** `*/*`

| Поле | Описание |
| --- | --- |
| `code` | string |
| `message` | string |

**409 Conflict**

**Response Schema:** `*/*`

| Поле | Описание |
| --- | --- |
| `code` | string |
| `message` | string |