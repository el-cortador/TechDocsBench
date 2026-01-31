**POST** `https://mk8s.api.cloud.ru/v2/billing/calculate-price`

**Примеры запроса**

```json
{
  "projectId": "string",
  "master": {
    "count": 0,
    "type": "MASTER_TYPE_SMALL",
    "flavorId": "string"
  },
  "nodePools": [
    {
      "count": 0,
      "cpu": 0,
      "ram": 0,
      "disk": {
        "size": "string",
        "type": "DISK_TYPE_SSD_NVME",
        "typeId": "string"
      },
      "oversubscription": "OVERSUBSCRIPTION_3",
      "gpu": 0,
      "type": "FLAVOR_TYPE_GENERAL",
      "flavorId": "string"
    }
  ],
  "disks": [
    {
      "size": "string",
      "type": "DISK_TYPE_SSD_NVME",
      "typeId": "string"
    }
  ],
  "rentPublicIpCount": 0,
  "addon": {
    "addonName": "string"
  },
  "clusterAttributes": [
    {
      "name": "NAME_PUBLIC_IP",
      "count": 0
    }
  ]
}
```

**Примеры ответа**

**200**

```json
{
  "masterPrice": 0.1,
  "nodePoolPrices": [
    {
      "disk": 0.1,
      "flavor": 0.1
    }
  ],
  "diskPrices": [
    0.1
  ],
  "rentPublicIpPrice": 0.1,
  "totalPricePerMonth": 0.1,
  "totalPricePerHour": 0.1,
  "addonPrice": 0.1
}
```