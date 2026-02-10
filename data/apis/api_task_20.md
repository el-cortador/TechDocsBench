**GET** `/client/v2/event`

**Authorizations:**  
iam_token_account_scoped  
iam_token_project_scoped  
API Key: iam_token_account_scoped  
IAM token for account  
Header parameter name: X-AUTH-TOKEN  
API Key: iam_token_project_scoped  
IAM token for project  
Header parameter name: X-AUTH-TOKEN

**Query Parameters**

| Параметр | Тип |
| --- | --- |
| `action_name` | string Action name |
| `item_name` | string Item name |
| `item_uuid` | string Items per page |
| `request_uuid` | string Staff id |
| `limit` | integer Items per page |
| `page` | integer Page number |

**Примеры ответа**

**200**

```json
{
  "execution_time": 0,
  "item_count": 0,
  "limit": 0,
  "page": 0,
  "progress": 0,
  "result": [
    {
      "action_name": "string",
      "change_data": {},
      "item_name": "string",
      "item_uuid": "string",
      "keystone_uid": "string",
      "request_uuid": "00000000-0000-0000-A000-000000000000",
      "secondary_user_id": "string",
      "staff_id": 0,
      "user_id": 0
    }
  ],
  "status": "string",
  "task_id": "00000000-0000-0000-A000-000000000000"
}
```

**303**

```json
{
  "execution_time": 0,
  "item_count": 0,
  "limit": 0,
  "page": 0,
  "progress": 0,
  "result": {},
  "status": "string",
  "task_id": "00000000-0000-0000-A000-000000000000"
}
```