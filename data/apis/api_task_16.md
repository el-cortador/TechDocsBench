**GET** `/iam/v1/groups`

**Authorizations:**  
iam_token_account_scoped  
API Key: iam_token_account_scoped  
IAM token for account.  
Header parameter name: X-Auth-Token

**Ответы**

**200 OK**  
*Response Schema: `*/*`*

| Поле | Тип |
| --- | --- |
| `groups` | Array of objects (models.GroupWithUserCount) |
| `description` | string |
| `id` | string |
| `name` | string |
| `roles` | Array of objects (models.Role) |
| `project_id` | string |
| `project_name` | string |
| `role_name` | string |
| `scope` | string (models.Scope) Enum: "account" "project" |
| `users_count` | integer |

**401 Unauthorized**