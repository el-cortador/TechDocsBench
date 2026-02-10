**PUT** `https://baremetal.api.cloud.ru/v2/reservedServers/{reserved_server_id}`

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `reserved_server_id` required | string |

**Query Parameters**

| Параметр | Описание |
| --- | --- |
| `name` required | string |
| `description` | string |
| `log_group_id` | string |

**Примеры ответа**

**200**

```json
{
  "reserved_server": {
    "id": "string",
    "availability_zone": {
      "zone_id": "string",
      "name": "string"
    },
    "project_id": "string",
    "name": "string",
    "hostname": "string",
    "description": "string",
    "distribution": {
      "name": "string",
      "slug": "string",
      "kernels": [
        {
          "name": "string",
          "slug": "string",
          "os_type": "OS_TYPE_UNSPECIFIED",
          "pricing_model": "PRICING_MODEL_UNSPECIFIED",
          "description": "string"
        }
      ]
    },
    "power_status": "POWER_STATUS_UNSPECIFIED",
    "created_by": {
      "id": "string",
      "subject_type": "SUBJECT_TYPE_UNSPECIFIED"
    },
    "updated_by": {
      "id": "string",
      "subject_type": "SUBJECT_TYPE_UNSPECIFIED"
    },
    "reserved_at": "2019-08-24T14:15:22Z",
    "updated_at": "2019-08-24T14:15:22Z",
    "deleted_at": "2019-08-24T14:15:22Z",
    "deleted": true,
    "server_status": "STATUS_TYPE_UNSPECIFIED",
    "interface": {
      "id": "string",
      "ip_address": "string",
      "subnet": {
        "id": "string",
        "name": "string",
        "address": "string"
      },
      "floating_ip": {
        "id": "string",
        "ip_address": "string",
        "name": "string"
      }
    },
    "flavor": {
      "id": "string",
      "cpu": "string",
      "ram": "string",
      "gpu": 0,
      "disks": [
        {
          "id": "string",
          "size": "string",
          "type": "DISK_TYPE_UNSPECIFIED",
          "count": "string"
        }
      ]
    },
    "dns_servers": [
      "string"
    ],
    "public_key_id": "string",
    "public_key": "string",
    "login": "string",
    "attributes": {
      "disks": [
        {
          "id": "string",
          "size": "string",
          "type": "DISK_TYPE_UNSPECIFIED",
          "count": "string"
        }
      ]
    },
    "remote_type": "REMOTE_TYPE_UNSPECIFIED",
    "log_group": {
      "id": "string",
      "project_id": "string",
      "name": "string",
      "description": "string",
      "retention_period": 0,
      "status": "LOG_GROUP_STATUS_UNSPECIFIED",
      "type": "LOG_GROUP_TYPE_UNSPECIFIED"
    },
    "vpc": {
      "id": "string",
      "name": "string"
    }
  }
}
```

**default**

```json
{
  "code": 0,
  "message": "string",
  "details": [
    {
      "@type": "string",
      "property1": {},
      "property2": {}
    }
  ]
}
```