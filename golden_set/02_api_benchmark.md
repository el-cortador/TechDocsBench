## Получение токена доступа (API)

Позволяет обменять код авторизации на токен доступа для работы с методами Seller API, а также обновить ранее полученный токен.

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

| Параметр | Описание |
| --- | --- |
| `client_id` | string Идентификатор OAuth-клиента. Если `grant_type` = `authorization_code` / `refresh_token` / `client_credentials`, параметр обязательный. |
| `client_secret` | string Секретный ключ OAuth-клиента. Если `grant_type` = `authorization_code` / `refresh_token` / `client_credentials`, параметр обязательный. |
| `code` | string Код авторизации. Если `grant_type` = `authorization_code`, параметр обязательный. |
| `grant_type` | string Тип гранта: 1. `authorization_code` — если используется код авторизации; 2. `refresh_token` — если используется токен для обновления токена доступа; 3. `client_credentials` — если используются клиентские данные. |
| `redirect_uri` | string URL, указанный при авторизации продавца. Если `grant_type` = `authorization_code`, параметр обязательный. |
| `refresh_token` | string Токен для обновления токена доступа. Если `grant_type` = `refresh_token`, параметр обязательный. |

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

**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `access_token` | string Токен доступа. |
| `expires_in` | integer `<int64>` Время действия токена доступа в секундах. |
| `refresh_token` | string Токен для обновления токена доступа. Не возвращается, если `access_type` = `online`. |
| `scope` | Array of strings Список разрешений, предоставленных продавцу. |
| `token_type` | string Тип токена. |

**default Ошибка**

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

**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Создание карточек товаров

**POST** `https://content-api.wildberries.ru/content/v2/cards/upload`

**Описание метода**

Метод создаёт карточки товаров c указанием описаний и характеристик товаров.  
Габариты товаров можно указать только в сантиметрах, вес товара с упаковкой — в килограммах.  
Создание карточки товара происходит асинхронно. Синхронизация новой карточки с сервисами может занимать до 30 минут. В течение этого времени невозможно добавить остатки на склады и настроить цены.  
Одним запросом можно создать максимум 100 отдельных карточек товаров или 100 групп объединённых карточек товаров по 30 карточек в каждой. Максимальный размер запроса 10 Мб.  
Если ответ Успешно (200), но какие-то карточки не создались, проверьте список несозданных карточек товаров.

**Примеры запроса**

**Content type:** `application/json`

```json
[
  {
    "subjectID": 105,
    "variants": [
      {
        "vendorCode": "АртикулПродавца",
        "wholesale": {
          "enabled": true,
          "quantum": 211
        },
        "title": "Наименование товара",
        "description": "Описание товара",
        "brand": "Бренд",
        "dimensions": {
          "length": 12,
          "width": 7,
          "height": 5,
          "weightBrutto": 1.242
        },
        "characteristics": [
          {
            "id": 12,
            "value": [
              "Turkish flag"
            ]
          },
          {
            "id": 25471,
            "value": 1200
          },
          {
            "id": 14177449,
            "value": [
              "red"
            ]
          }
        ],
        "sizes": [
          {
            "techSize": "S",
            "wbSize": "42",
            "price": 5000,
            "skus": [
              "88005553535"
            ]
          }
        ]
      }
    ]
  }
]
```

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Request Body schema:** `application/json`

| Параметр | Описание |
| --- | --- |
| Array | Array |
| `subjectID` required | integer ID предмета |
| `variants` required | Array of objects [ items [ 1 .. 30 ] ] Объединённые карточки товаров. Чтобы создать отдельную карточку, передайте только один объект |

**Примеры ответа**

**200**

```json
{
  "data": null,
  "error": false,
  "errorText": "",
  "additionalErrors": {}
}
```

**400**

```json
{
  "data": null,
  "error": true,
  "errorText": "Invalid request format",
  "additionalErrors": {}
}
```

**401**

```json
{
  "title": "unauthorized",
  "detail": "token problem; token is malformed: could not base64 decode signature: illegal base64 data at input byte 84",
  "code": "07e4668e--a53a3d31f8b0-[UK-oWaVDUqNrKG ]; 03bce=277; 84bd353bf-75",
  "requestId": "7b80742415072fe8b6b7f7761f1d1211",
  "origin": "s2s-api-auth-catalog",
  "status": 401,
  "statusText": "Unauthorized",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**413**

```json
{
  "title": "request body too long",
  "detail": "https://openapi.wildberries.ru/content/api/ru/",
  "code": "71d3de1b-001e-488f-bbf5-55c31254fbeb",
  "requestId": "MN8usr6RfrzWHZfucSvNgb",
  "origin": "s2s-api-auth-content",
  "status": 413,
  "statusText": "Request Entity Too Large"
}
```

**429**

```json
{
  "title": "too many requests",
  "detail": "limited by c122a060-a7fb-4bb4-abb0-32fd4e18d489",
  "code": "07e4668e-ac2242c5c8c5-[UK-4dx7JUdskGZ]",
  "requestId": "9d3c02cc698f8b041c661a7c28bed293",
  "origin": "s2s-api-auth-catalog",
  "status": 429,
  "statusText": "Too Many Requests",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**Описание ответов**

**200 Успешно**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `data` | object or null Данные ответа |
| `error` | boolean Флаг ошибки |
| `errorText` | string Описание ошибки |
| `additionalErrors` | (object or null) or (string or null) or object Дополнительные ошибки |

**400 Неправильный запрос**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `data` | object or null Данные ошибки |
| `error` | boolean Флаг ошибки |
| `errorText` | string Текст ошибки |
| `additionalErrors` | object or null Дополнительные ошибки |

**401 Не авторизован**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

**413 Превышен лимит объёма данных в запросе**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |

**429 Слишком много запросов**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

---

## Загрузить медиафайл

**POST** `https://content-api.wildberries.ru/content/v3/media/file`

**Описание метода**

Метод загружает и добавляет один медиафайл к карточке товара.

**Требования к изображениям:**
1. максимум изображений для одной карточки товара — 30
2. минимальное разрешение — 700x900 px
3. максимальный размер — 32 Мб
4. минимальное качество — 65%
5. форматы — JPG, PNG, BMP, GIF (статичные), WebP

**Требования к видео:**
1. максимум одно видео для одной карточки товара
2. максимальный размер — 50 Мб
3. форматы — MOV, MP4

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Header Parameters**

| Параметр | Описание |
| --- | --- |
| `X-Nm-Id` required | string Example: 213864079 Артикул WB |
| `X-Photo-Number` required | integer Example: 2 Номер медиафайла на загрузку, начинается с 1. При загрузке видео всегда указывайте 1. Чтобы добавить изображение к уже загруженным, номер медиафайла должен быть больше количества уже загруженных медиафайлов. |

**Request Body schema:** `multipart/form-data`

| Параметр | Описание |
| --- | --- |
| `uploadfile` required | string `<binary>` |

**Примеры ответа**

**200**

```json
{
  "data": {},
  "error": false,
  "errorText": "",
  "additionalErrors": null
}
```

**400**

```json
{
  "additionalErrors": null,
  "data": null,
  "error": true,
  "errorText": "Текст ошибки"
}
```

**401**

```json
{
  "title": "unauthorized",
  "detail": "token problem; token is malformed: could not base64 decode signature: illegal base64 data at input byte 84",
  "code": "07e4668e--a53a3d31f8b0-[UK-oWaVDUqNrKG ]; 03bce=277; 84bd353bf-75",
  "requestId": "7b80742415072fe8b6b7f7761f1d1211",
  "origin": "s2s-api-auth-catalog",
  "status": 401,
  "statusText": "Unauthorized",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**403**

```json
{
  "additionalErrors": null,
  "data": null,
  "error": true,
  "errorText": "Текст ошибки"
}
```

**429**

```json
{
  "title": "too many requests",
  "detail": "limited by c122a060-a7fb-4bb4-abb0-32fd4e18d489",
  "code": "07e4668e-ac2242c5c8c5-[UK-4dx7JUdskGZ]",
  "requestId": "9d3c02cc698f8b041c661a7c28bed293",
  "origin": "s2s-api-auth-catalog",
  "status": 429,
  "statusText": "Too Many Requests",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**Описание ответов**

**200 Успешно**

| Поле | Описание |
| --- | --- |
| `data` | object |
| `error` | boolean Флаг ошибки |
| `errorText` | string Описание ошибки |
| `additionalErrors` | object or null Дополнительные ошибки |

**400 Неправильный запрос**

| Поле | Описание |
| --- | --- |
| `additionalErrors` | object or null Дополнительные ошибки |
| `data` | object or null Данные ошибки |
| `error` | boolean Флаг ошибки |
| `errorText` | string Текст ошибки |

**401 Не авторизован**

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

**403 Доступ запрещён**

| Поле | Описание |
| --- | --- |
| `additionalErrors` | object or null Дополнительные ошибки |
| `data` | object or null Данные ошибки |
| `error` | boolean Флаг ошибки |
| `errorText` | string Текст ошибки |

**429 Слишком много запросов**

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

---

## Списки кампаний

**GET** `https://advert-api.wildberries.ru/adv/v1/promotion/count`

**Описание метода**

Метод возвращает списки всех рекламных кампаний продавца с их ID. Кампании сгруппированы по типу и статусу, у каждой указана дата последнего изменения.

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Примеры ответа**

**200**

```json
{
  "adverts": [
    {
      "type": 9,
      "status": 8,
      "count": 3,
      "advert_list": [
        {
          "advertId": 6485174,
          "changeTime": "2023-05-10T12:12:52.676254+03:00"
        },
        {
          "advertId": 6500443,
          "changeTime": "2023-05-10T17:08:46.370656+03:00"
        },
        {
          "advertId": 7936341,
          "changeTime": "2023-07-12T15:51:08.367478+03:00"
        }
      ]
    }
  ],
  "all": 3
}
```

**401**

```json
{
  "title": "unauthorized",
  "detail": "token problem; token is malformed: could not base64 decode signature: illegal base64 data at input byte 84",
  "code": "07e4668e--a53a3d31f8b0-[UK-oWaVDUqNrKG ]; 03bce=277; 84bd353bf-75",
  "requestId": "7b80742415072fe8b6b7f7761f1d1211",
  "origin": "s2s-api-auth-catalog",
  "status": 401,
  "statusText": "Unauthorized",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**429**

```json
{
  "title": "too many requests",
  "detail": "limited by c122a060-a7fb-4bb4-abb0-32fd4e18d489",
  "code": "07e4668e-ac2242c5c8c5-[UK-4dx7JUdskGZ]",
  "requestId": "9d3c02cc698f8b041c661a7c28bed293",
  "origin": "s2s-api-auth-catalog",
  "status": 429,
  "statusText": "Too Many Requests",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**Описание ответов**

**200 Успешно**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `adverts` | Array of objects or null Данные по кампаниям |
| `all` | integer Общее количество кампаний всех статусов и типов |

**401 Не авторизован**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

**429 Слишком много запросов**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

---

## Поисковые запросы по товару

**POST** `https://seller-analytics-api.wildberries.ru/api/v2/search-report/product/search-texts`

**Описание метода**

Метод формирует топ поисковых запросов по товару.

**Параметры выбора поисковых запросов:**
1. `limit` — количество запросов, максимум 30 (для тарифа Продвинутый — 100)
2. `topOrderBy` — способ выбора топа запросов

Параметры `includeSubstitutedSKUs` и `includeSearchTexts` не могут одновременно иметь значение `false`.

**Пример запроса**

**Content type**  
`application/json`

```json
{
  "currentPeriod": {
    "start": "2024-02-10",
    "end": "2024-02-10"
  },
  "pastPeriod": {
    "start": "2024-02-08",
    "end": "2024-02-08"
  },
  "nmIds": [
    162579635,
    166699779
  ],
  "topOrderBy": "openToCart",
  "includeSubstitutedSKUs": true,
  "includeSearchTexts": false,
  "orderBy": {
    "field": "avgPosition",
    "mode": "asc"
  },
  "limit": 20
}
```

**Authorizations:**  
HeaderApiKey  
API Key: HeaderApiKey  
Header parameter name: Authorization

**Request Body schema:** `application/json` required

| Параметр | Описание |
| --- | --- |
| `currentPeriod` required | object (Period) Текущий период |
| `pastPeriod` | object (pastPeriod) Прошлый период для сравнения. Количество дней — меньше или равно currentPeriod |
| `nmIds` required | Array of integers `<uint64>` <= 50 items [ items `<uint64>` ] Список артикулов WB |
| `topOrderBy` required | string Enum: `"openCard"` `"addToCart"` `"openToCart"` `"orders"` `"cartToOrder"` Фильтрация по поисковым запросам, по которым больше всего: * `openCard` — перешли в карточку * `addToCart` — добавили в корзину * `openToCart` — конверсия в корзину * `orders` — заказали товаров * `cartToOrder` — конверсия в заказ |
| `includeSubstitutedSKUs` | boolean Default: true Показать данные по прямым запросам с подменным артикулом |
| `includeSearchTexts` | boolean Default: true Показать данные по поисковым запросам без учёта подменного артикула |
| `orderBy` required | object (OrderByGrTe) Параметры сортировки |
| `limit` required | StandardTariff (integer) or AdvancedTariff (integer) (TextLimit) |

**Примеры ответа**

**200**

```json
{
  "data": {
    "items": [
      {
        "text": "костюм",
        "nmId": 211131895,
        "subjectName": "Phones",
        "brandName": "Apple",
        "vendorCode": "wb3ha2668w",
        "name": "iPhone 13 256 ГБ Серебристый",
        "isCardRated": true,
        "rating": 6,
        "feedbackRating": 1,
        "price": {
          "minPrice": 150,
          "maxPrice": 300
        },
        "frequency": {
          "current": 5,
          "dynamics": 50
        },
        "weekFrequency": 140,
        "medianPosition": {
          "current": 5,
          "dynamics": 50
        },
        "avgPosition": {
          "current": 5,
          "dynamics": 50
        },
        "openCard": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "addToCart": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "openToCart": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "orders": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "cartToOrder": {
          "current": 5,
          "dynamics": 50,
          "percentile": 50
        },
        "visibility": {
          "current": 5,
          "dynamics": 50
        }
      }
    ]
  }
}
```

**400**

```json
{
  "title": "Invalid request body",
  "detail": "code=400, message=invalid: positionCluster (field required), limit (field required), offset (field required), internal=invalid: positionCluster (field required), limit (field required), offset (field required",
  "requestId": "fb25c9e9-cae8-52db-b68e-736c1466a3f5",
  "origin": "analytic-open-api"
}
```

**401**

```json
{
  "title": "unauthorized",
  "detail": "token problem; token is malformed: could not base64 decode signature: illegal base64 data at input byte 84",
  "code": "07e4668e--a53a3d31f8b0-[UK-oWaVDUqNrKG ]; 03bce=277; 84bd353bf-75",
  "requestId": "7b80742415072fe8b6b7f7761f1d1211",
  "origin": "s2s-api-auth-catalog",
  "status": 401,
  "statusText": "Unauthorized",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**403**

```json
{
  "title": "Authorization error",
  "detail": "Authorization error",
  "requestId": "fb25c9e9-cae8-52db-b68e-736c1466a3f5",
  "origin": "analytic-open-api"
}
```

**429**

```json
{
  "title": "too many requests",
  "detail": "limited by c122a060-a7fb-4bb4-abb0-32fd4e18d489",
  "code": "07e4668e-ac2242c5c8c5-[UK-4dx7JUdskGZ]",
  "requestId": "9d3c02cc698f8b041c661a7c28bed293",
  "origin": "s2s-api-auth-catalog",
  "status": 429,
  "statusText": "Too Many Requests",
  "timestamp": "2024-09-30T06:52:38Z"
}
```

**Описание ответов**

**200 Успешно**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `data` required | object Данные ответа |

**400 Неправильный запрос**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `title` required | string Заголовок ошибки |
| `detail` required | string Детали ошибки |
| `requestId` required | string Уникальный ID запроса |
| `origin` required | string ID внутреннего сервиса WB |

**401 Не авторизован**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

**403 Доступ запрещён**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `title` required | string Заголовок ошибки |
| `detail` required | string Детали ошибки |
| `requestId` required | string Уникальный ID запроса |
| `origin` required | string ID внутреннего сервиса WB |

**429 Слишком много запросов**  
**Response Schema:** `application/problem+json`

| Поле | Описание |
| --- | --- |
| `title` | string Заголовок ошибки |
| `detail` | string Детали ошибки |
| `code` | string Внутренний код ошибки |
| `requestId` | string Уникальный ID запроса |
| `origin` | string ID внутреннего сервиса WB |
| `status` | number HTTP статус-код |
| `statusText` | string Расшифровка HTTP статус-кода |
| `timestamp` | string `<date-time>` Дата и время запроса |

---

## Создание или обновление товара

**POST** `https://api-seller.ozon.ru/v3/product/import`

**Описание**

Метод для создания товаров и обновления информации о них.  
В сутки можно создать или обновить определённое количество товаров. Чтобы узнать лимит, используйте `/v4/product/info/limit`. Если количество загрузок и обновлений товаров превысит лимит, появится ошибка `item_limit_exceeded`.  
В одном запросе можно передать до 100 товаров. Каждый товар — это отдельный элемент в массиве `items`. Укажите всю информацию о товаре: его характеристики, штрихкод, изображения, габариты, цену и валюту цены.  
При обновлении товара передайте в запросе всю информацию о нём.  
Указанная валюта должна совпадать с той, которая установлена в настройках личного кабинета. По умолчанию передаётся `RUB` — российский рубль. Например, если у вас установлена валюта юань, передавайте значение `CNY`, иначе вернётся ошибка.  
Товар не будет создан или обновлён, если вы заполните неправильно или не укажете:  
1. **Обязательные характеристики**: характеристики отличаются для разных категорий — их можно посмотреть в Базе знаний продавца или получить методом `/v1/description-category/attribute`.  
2. **Реальные объёмно-весовые характеристики**: `depth`, `width`, `height`, `dimension_unit`, `weight`, `weight_unit`. Не пропускайте эти параметры в запросе и не указывайте 0.  

Для некоторых характеристик можно использовать HTML-теги.  
После модерации товар появится в вашем личном кабинете, но не будет виден пользователям, пока вы не выставите его на продажу.  
Каждый товар в запросе — отдельный элемент массива `items`.  
Чтобы объединить две карточки, для каждой передайте `9048` в массиве `attributes`. Все атрибуты в этих карточках, кроме размера или цвета, должны совпадать.

**Примеры запроса**

**Content type**  
`application/json`

```json
{
  "items": [
    {
      "attributes": [
        {
          "complex_id": 0,
          "id": 5076,
          "values": [
            {
              "dictionary_value_id": 971082156,
              "value": "Стойка для акустической системы"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 9048,
          "values": [
            {
              "value": "Комплект защитных плёнок для X3 NFC. Темный хлопок"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 8229,
          "values": [
            {
              "dictionary_value_id": 95911,
              "value": "Комплект защитных плёнок для X3 NFC. Темный хлопок"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 85,
          "values": [
            {
              "dictionary_value_id": 5060050,
              "value": "Samsung"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 10096,
          "values": [
            {
              "dictionary_value_id": 61576,
              "value": "серый"
            }
          ]
        }
      ],
      "barcode": "112772873170",
      "description_category_id": 17028922,
      "new_description_category_id": 0,
      "color_image": "",
      "complex_attributes": [],
      "currency_code": "RUB",
      "depth": 10,
      "dimension_unit": "mm",
      "height": 250,
      "images": [],
      "images360": [],
      "name": "Комплект защитных плёнок для X3 NFC. Темный хлопок",
      "offer_id": "143210608",
      "old_price": "1100",
      "pdf_list": [],
      "price": "1000",
      "primary_image": "",
      "promotions": [
        {
          "operation": "UNKNOWN",
          "type": "REVIEWS_PROMO"
        }
      ],
      "type_id": 91565,
      "vat": "0.1",
      "weight": 100,
      "weight_unit": "g",
      "width": 150
    }
  ]
}
```

**Header Parameters**

| Параметр | Описание |
| --- | --- |
| `Client-Id` required | string Идентификатор клиента. |
| `Api-Key` required | string API-ключ. |

**Request Body schema:** `application/json`

| Параметр | Описание |
| --- | --- |
| `items` | Array of objects Массив данных. |
| `attributes` | Array of objects Массив с характеристиками товара. Характеристики отличаются для разных категорий — их можно посмотреть в Базе знаний продавца или через API. |
| `barcode` | string Штрихкод товара. |
| `color_image` | string Маркетинговый цвет. Формат: адрес ссылки на изображение в общедоступном облачном хранилище. Формат изображения по ссылке — JPG. |
| `complex_attributes` | Array of objects Массив характеристик, у которых есть вложенные атрибуты. |
| `currency_code` | string Валюта ваших цен. Переданное значение должно совпадать с валютой, которая установлена в настройках личного кабинета. По умолчанию передаётся `RUB` — российский рубль. Например, если у вас установлена валюта взаиморасчётов юань, передавайте значение `CNY`, иначе вернётся ошибка. Возможные значения: * `RUB` — российский рубль, * `BYN` — белорусский рубль, * `KZT` — тенге, * `EUR` — евро, * `USD` — доллар США, * `CNY` — юань. |
| `depth` | integer `<int32>` Глубина упаковки. |
| `description_category_id` required | integer `<int64>` Идентификатор категории. Можно получить с помощью метода `/v1/description-category/tree` |
| `new_description_category_id` | integer `<int64>` Новый идентификатор категории. Укажите его, если нужно изменить текущую категорию товара. |
| `dimension_unit` | string Единица измерения габаритов: * `mm` — миллиметры, * `cm` — сантиметры, * `in` — дюймы. |
| `geo_names` | Array of strings Геоограничения — при необходимости заполните параметр в личном кабинете при создании или редактировании товара. Необязательный параметр. |
| `height` | integer `<int32>` Высота упаковки. |
| `images` | Array of strings Массив изображений. До 30 штук. Изображения показываются на сайте в таком же порядке, как в массиве. Если не передать значение `primary_image`, первое изображение в массиве будет главным для товара. Если вы передали значение `primary_image`, передайте до 29 изображений. Если параметр `primary_image` пустой, передайте до 30 изображений. Формат: адрес ссылки на изображение в общедоступном облачном хранилище. Формат изображения по ссылке — JPG или PNG. |
| `images360` | Array of strings Массив изображений 360. До 70 штук. Формат: адрес ссылки на изображение в общедоступном облачном хранилище. Формат изображения по ссылке — JPG. |
| `name` | string Название товара. До 500 символов. |
| `offer_id` | string Идентификатор товара в системе продавца — артикул. Максимальная длина строки — 50 символов. |
| `old_price` | string Цена до скидок (будет зачёркнута на карточке товара). Указывается в рублях. Разделитель дробной части — точка, до двух знаков после точки. Если вы раньше передавали `old_price`, то при обновлении `price` также обновите `old_price`. |
| `pdf_list` | Array of objects Список PDF-файлов. |
| `price` required | string Цена товара с учётом скидок, отображается на карточке товара. Если на товар нет скидок, укажите значение `old_price` в этом параметре. |
| `primary_image` | string Ссылка на главное изображение товара. |
| `promotions` | Array of objects Акции. |
| `service_type` | string Default: `"IS_CODE_SERVICE"` Enum: `"IS_CODE_SERVICE"` `"IS_NO_CODE_SERVICE"` |
| `type_id` required | integer `<int64>` Идентификатор типа товара. Значения можно получить из такого же параметра `type_id` в ответе метода `/v1/description-category/tree`. При заполнении этого параметра можно не указывать в `attibutes` атрибут с параметром `id:8229`, `type_id` будет использоваться в приоритете. |
| `vat` | string Ставка НДС для товара: * `0` — не облагается НДС, * `0.05` — 5%, * `0.07` — 7%, * `0.1` — 10%, * `0.2` — 20%, * `0.22` — 22%. Передавайте значение ставки, актуальное на данный момент. |
| `weight` | integer `<int32>` Вес товара в упаковке. Предельное значение — 1000 килограммов или конвертированная величина в других единицах измерения. |
| `weight_unit` | string Единица измерения веса: * `g` — граммы, * `kg` — килограммы, * `lb` — фунты. |
| `width` | integer `<int32>` Ширина упаковки. |

**Примеры ответа**

**200**

```json
{
  "result": {
    "task_id": 172549793
  }
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

**Ответы**

**200 Создан новый товар / Информация о товаре обновлена**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `result` | object Результаты запроса. |
| `task_id` | integer `<int64>` Номер задания на загрузку товаров. Проверьте статус создания или обновления товара методом `/v1/product/import/info` |

**400 Неверный параметр**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**403 Доступ запрещён**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**404 Ответ не найден**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**409 Конфликт запроса**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**500 Внутренняя ошибка сервера**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Список акций

**GET** `https://api-seller.ozon.ru/v1/actions`

**Описание**  
Метод для получения списка акций Ozon, в которых можно участвовать.

**Примеры ответа**

**200**

```json
{
  "result": [
    {
      "id": 71342,
      "title": "test voucher #2",
      "date_start": "2021-11-22T09:46:38Z",
      "date_end": "2021-11-30T20:59:59Z",
      "potential_products_count": 0,
      "is_participating": true,
      "participating_products_count": 5,
      "description": "",
      "action_type": "DISCOUNT",
      "banned_products_count": 0,
      "with_targeting": false,
      "discount_type": "UNKNOWN",
      "discount_value": 0,
      "order_amount": 0,
      "freeze_date": "",
      "is_voucher_action": true
    }
  ]
}
```

**default**

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

**Ответы**

**200 Список акций**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `result` | Array of objects Результаты запроса. |
| `id` | number `<double>` Идентификатор акции. |
| `title` | string Название акции. |
| `action_type` | string Тип акции. |
| `description` | string Описание акции. |
| `date_start` | string Дата начала акции. |
| `date_end` | string Дата окончания акции. |
| `freeze_date` | string Дата приостановки акции. Если поле заполнено, продавец не может повышать цены, изменять список товаров и уменьшать количество единиц товаров в акции. Продавец может понижать цены и увеличивать количество единиц товара в акции. |
| `potential_products_count` | number `<double>` Количество товаров, доступных для акции. |
| `participating_products_count` | number `<double>` Количество товаров, которые участвуют в акции. |
| `is_participating` | boolean Участвуете вы в этой акции или нет. |
| `is_voucher_action` | boolean Признак, что для участия в акции покупателям нужен промокод. |
| `banned_products_count` | number `<double>` Количество заблокированных товаров. |
| `with_targeting` | boolean Признак, что акция с целевой аудиторией. |
| `order_amount` | number `<double>` Сумма заказа. |
| `discount_type` | string Тип скидки. |
| `discount_value` | number `<double>` Размер скидки. |

**Default Ошибка**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Список типов соответствия требованиям

**GET** `https://api-seller.ozon.ru/v1/product/certificate/accordance-types`

**Описание**  
Метод получения типов соответствия товаров требованиям сертификатов.

**Header Parameters**

| Параметр | Описание |
| --- | --- |
| `Client-Id` required | string Идентификатор клиента. |
| `Api-Key` required | string API-ключ. |

**Примеры ответа**

**200**

```json
{
  "result": [
    {
      "name": "ГОСТ",
      "value": "gost"
    },
    {
      "name": "Технический регламент РФ",
      "value": "technical_regulations_rf"
    },
    {
      "name": "Технический регламент ТС",
      "value": "technical_regulations_cu"
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

**Ответы**

**200 Cправочник типов соответствия требованиям**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `result` | Array of objects Список типов и названий сертификатов. |
| `name` | string Название документа. |
| `value` | string Значение справочника. |

**400 Неверный параметр**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**403 Доступ запрещён**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**404 Ответ не найден**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**409 Конфликт запроса**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**500 Внутренняя ошибка сервера**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Список складов

**POST** `https://api-seller.ozon.ru/v1/warehouse/list`

**Описание**  
Возвращает список складов FBS и rFBS. Метод можно использовать 1 раз в минуту.

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
| `Client-Id` required | string Идентификатор клиента. |
| `Api-Key` required | string API-ключ. |

**Request Body schema:** `application/json`

| Параметр | Описание |
| --- | --- |
| `limit` required | integer `<int64>` <= 200 Количество значений в ответе. |
| `offset` | integer `<int64>` Количество элементов, которое будет пропущено в ответе. Например, если offset = 10, то ответ начнётся с 11-го найденного элемента. |

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

**Ответы**

**200 Список складов**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `result` | Array of objects Список складов. |
| `has_entrusted_acceptance` | boolean Признак доверительной приёмки. true, если доверительная приёмка включена на складе. |
| `is_rfbs` | boolean Признак работы склада по схеме rFBS: 1. true — склад работает по схеме rFBS; 2. false — не работает по схеме rFBS. |
| `name` | string Название склада. |
| `warehouse_id` | integer `<int64>` Идентификатор склада. |
| `can_print_act_in_advance` | boolean Возможность печати акта приёма-передачи заранее. true, если печатать заранее возможно. |
| `first_mile_type` | object Первая миля FBS. |
| `has_postings_limit` | boolean Признак наличия лимита минимального количества заказов. true, если лимит есть. |
| `is_karantin` | boolean Признак, что склад не работает из-за карантина. |
| `is_kgt` | boolean Признак, что склад принимает крупногабаритные товары. |
| `is_economy` | boolean true, если склад работает с эконом-товарами. |
| `is_timetable_editable` | boolean Признак, что можно менять расписание работы складов. |
| `min_postings_limit` | integer `<int32>` Минимальное значение лимита — количество заказов, которые можно привезти в одной поставке. |
| `postings_limit` | integer `<int32>` Значение лимита. -1, если лимита нет. |
| `min_working_days` | integer `<int64>` Количество рабочих дней склада. |
| `status` | string Статус склада. Соответствие статусов склада со статусами с личном кабинете: 1. new — Активируется 2. created — Активный 3. disabled — В архиве 4. blocked — Заблокирован 5. disabled_due_to_limit — На паузе 6. error — Ошибка |
| `working_days` | Array of strings Items Enum: "1" "2" "3" "4" "5" "6" "7" Рабочие дни склада. |

**400 Неверный параметр**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**403 Доступ запрещён**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**404 Ответ не найден**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**409 Конфликт запроса**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**500 Внутренняя ошибка сервера**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Отправить файл

**POST** `https://api-seller.ozon.ru/v1/chat/send/file`

**Описание**  
Отправляет файл в существующий чат по его идентификатору.  

Для отправлений:  
1. **FBO** — вы можете отправить файл в течение 48 часов с момента получения последнего сообщения от покупателя.  
2. **FBS или rFBS** — вы можете отправить файл покупателю после оплаты и в течение 72 часов после доставки отправления. После этого вы можете только отвечать на сообщения в течение 48 часов с момента получения последнего сообщения от покупателя.

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
| `Client-Id` required | string Идентификатор клиента. |
| `Api-Key` required | string API-ключ. |

**Request Body schema:** `application/json`

| Параметр | Описание |
| --- | --- |
| `base64_content` | string Файл в виде строки base64. |
| `chat_id` required | string Идентификатор чата. |
| `name` | string Название файла с расширением. |

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

**Ответы**

**200 Файл отправлен**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `result` | string Результат обработки запроса. |

**400 Неверный параметр**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**403 Доступ запрещён**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**404 Ответ не найден**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**409 Конфликт запроса**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

**500 Внутренняя ошибка сервера**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `details` | Array of objects Дополнительная информация об ошибке. |
| `message` | string Описание ошибки. |

---

## Возврат списка дистрибутивов

**GET** `https://baremetal.api.cloud.ru/v2/distributions`

**Описание**  
Возвращает список дистрибутивов.

**Query Parameters**

| Параметр | Описание |
| --- | --- |
| `page_size` | string `<int64>` Желаемое количество записей в ответе на запрос. Значение по умолчанию — 50. Максимальное значение — 100. Если записей больше, чем указано в page_size: 1. ответ разобьется на несколько страниц; 2. в ответе появится параметр next_page_token, который используется при последующих аналогичных запросах и позволяет посмотреть записи со следующей страницы. |
| `page_token` | string Токен запрашиваемой страницы с результатами. Используется для просмотра записей, которые не попали в первый ответ на запрос. Равен значению параметра next_page_token, который возвращается в первом ответе на запрос. |
| `filter` | string Фильтрующее выражение. Условие имеет форму <поле><operator><значение>: 1. <поле> имя поля для фильтрации; 2. <operator> логический оператор = (равно); 3. <значение> значение поля. Зарезервировано для дальнейшего расширения. |

**Примеры ответа**

**200**

```json
{
  "distributions": [
    {
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
    }
  ],
  "next_page_token": "string"
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

**Ответы**

**200 A successful response.**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `distributions` | Array of objects (cloudru.iaas.baremetal.v2.Distribution) Список дистрибутивов. |
| `name` | string Название дистрибутива. |
| `slug` | string Машиночитаемое название дистрибутива. |
| `kernels` | Array of objects (cloudru.iaas.baremetal.v2.Kernel) Ядра, доступные для дистрибутива. |
| `name` | string Название ядра дистрибутива. |
| `slug` | string Название ядра дистрибутива для машинной обработки. |
| `os_type` | string (cloudru.iaas.baremetal.v2.OSType) Default: "OS_TYPE_UNSPECIFIED" Enum: "OS_TYPE_UNSPECIFIED" "OS_TYPE_X64" Тип операционной системы. 1. OS_TYPE_UNSPECIFIED: Тип не определен. 2. OS_TYPE_X64: 64 битная операционная система. |
| `pricing_model` | string (cloudru.iaas.baremetal.v2.PricingModel) Default: "PRICING_MODEL_UNSPECIFIED" Enum: "PRICING_MODEL_UNSPECIFIED" "PRICING_MODEL_FREE" "PRICING_MODEL_PAID" Модель тарификации дистрибутива. 1. PRICING_MODEL_UNSPECIFIED: Модель тарификации не определена. 2. PRICING_MODEL_FREE: Бесплатная модель тарификации. 3. PRICING_MODEL_PAID: Платная модель тарификации. |
| `description` | string Описание карточки дистрибутива. |
| `next_page_token` | string Токен следующей страницы. |

**default An unexpected error response.**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` |
| `message` | string |
| `details` | Array of objects (google.protobuf.Any) |
| `@type` | string |
| `property name* additional property` | object |

---

## Изменение информации о сервере

**PUT** `https://baremetal.api.cloud.ru/v2/reservedServers/{reserved_server_id}`

**Описание**  
Изменяет информацию о сервере.

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `reserved_server_id` required | string Идентификатор арендованного сервера. |

**Query Parameters**

| Параметр | Описание |
| --- | --- |
| `name` required | string Название арендованного сервера. |
| `description` | string Описание. |
| `log_group_id` | string Идентификатор лог-группы. |

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

**Ответы**

**200 A successful response.**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `reserved_server` | object (cloudru.iaas.baremetal.v2.ReservedServer) Информация об арендованном сервере. |
| `id` | string Виртуальный идентификатор сервера, указывающий на объект аренды физического сервера. Если в случае проблем будет заменен физический сервер, то данный идентификатор никак не изменится. |
| `availability_zone` | object (cloudru.iaas.baremetal.v2.AvailabilityZone) Зона доступности. |
| `project_id` required | string Идентификатор проекта. |
| `name` required | string Название арендованного сервера. |
| `hostname` required | string Имя хоста арендованного сервера. |
| `description` | string Описание сервера. |
| `distribution` | object (cloudru.iaas.baremetal.v2.Distribution) Информация о дистрибутиве. |
| `power_status` | string (cloudru.iaas.baremetal.v2.PowerStatus) Default: "POWER_STATUS_UNSPECIFIED" Enum: "POWER_STATUS_UNSPECIFIED" "POWER_STATUS_ON" "POWER_STATUS_OFF" "POWER_STATUS_STOPPING" "POWER_STATUS_STARTING" "POWER_STATUS_REBOOTING" "POWER_STATUS_ERROR" Статус питания арендованного сервера. |
| `created_by` | object (cloudru.iaas.baremetal.v2.Subject) Информация о субъекте. |
| `updated_by` | object (cloudru.iaas.baremetal.v2.Subject) Информация о субъекте. |
| `reserved_at` | string `<date-time>` Дата аренды сервера. |
| `updated_at` | string `<date-time>` Дата последнего обновления записи. |
| `deleted_at` | string `<date-time>` Дата и время прекращения аренды сервера. |
| `deleted` | boolean Прекращена ли аренда сервера. |
| `server_status` | string (cloudru.iaas.baremetal.v2.StatusType) Default: "STATUS_TYPE_UNSPECIFIED" Enum: "STATUS_TYPE_UNSPECIFIED" "STATUS_TYPE_RESERVED" "STATUS_TYPE_OS_INSTALL" "STATUS_TYPE_OS_INSTALL_COMPLETED" "STATUS_TYPE_VPC_FAILURE" "STATUS_TYPE_OS_INSTALL_FAILURE" "STATUS_TYPE_RESERVING" "STATUS_TYPE_CREATED" Статус арендованного сервера. |
| `interface` | object (cloudru.iaas.baremetal.v2.Interface) Информация об IP-адресе сервера. |
| `flavor` | object (cloudru.iaas.baremetal.v2.FlavorShort) Типовая конфигурация сервера. |
| `dns_servers` | Array of strings Адреса DNS-серверов, используемые в сети арендованного сервера. |
| `public_key_id` required | string Идентификатор публичного SSH-ключа пользователя ОС. |
| `public_key` | string Публичный SSH-ключ для подключения к серверу. |
| `login` required | string Логин учетной записи в ОС, установленной на сервере. |
| `attributes` | object (cloudru.iaas.baremetal.v2.Attributes) Атрибуты сервера. |
| `remote_type` | string (cloudru.iaas.baremetal.v2.RemoteType) Default: "REMOTE_TYPE_UNSPECIFIED" Enum: "REMOTE_TYPE_UNSPECIFIED" "REMOTE_TYPE_VNC" "REMOTE_TYPE_LENOVO" "REMOTE_TYPE_INSPUR" "REMOTE_TYPE_HUAWEI" Тип удаленной консоли сервера. |
| `log_group` | object (cloudru.iaas.baremetal.v2.LogGroup) Группа логирования. |
| `vpc` | object (cloudru.iaas.baremetal.v2.VPC) Описание подключения арендованного сервера к сети Virtual Private Cloud. |

**default An unexpected error response.**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` |
| `message` | string |
| `details` | Array of objects (google.protobuf.Any) |
| `@type` | string |
| `property name* additional property` | object |

---

## Список пользователей кластера

**GET** `https://postgresql.api.cloud.ru/v1/clusters/{cluster_id}/users`

**Описание**  
Возвращает список пользователей кластера PostgreSQL.

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `cluster_id` required | string Идентификатор кластера. |

**Примеры ответа**

**200**

```json
{
  "users": [
    {
      "name": "string",
      "supported_roles": [
        {
          "name": "string"
        }
      ],
      "granted_roles": [
        {
          "name": "string"
        }
      ]
    }
  ]
}
```

**default**

```json
{
  "code": 0,
  "message": "string",
  "details": [
    {
      "@type": "string"
    }
  ]
}
```

**Ответы**

**200 OK**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `users` | Array of objects (cloudru.dbaas.postgresql.v1.User) Список пользователей кластера. |
| `name` required | string Имя пользователя. |
| `supported_roles` | Array of objects (cloudru.dbaas.postgresql.v1.PostgreSQLRole) Доступные роли. |
| `name` | string Название роли. |
| `granted_roles` | Array of objects (cloudru.dbaas.postgresql.v1.PostgreSQLRole) Назначенные роли. |
| `name` | string Название роли. |

---

## Получение информации об операции по идентификатору.

**GET** `https://postgresql.api.cloud.ru/v1/operations/{operation_id}`

**Описание**  
Получает информацию об операции по ее идентификатору.

**Path Parameters**

| Параметр | Описание |
| --- | --- |
| `operation_id` required | string Идентификатор операции. |

**Примеры ответа**

**200**

```json
{
  "id": "string",
  "resource_name": "urn:cloud:postgresql::265c6f28-9c84-4cef-bbc5-4472c1743bc0:backend",
  "resource_id": "54295782-7aef-43e6-b33b-c9735938677a",
  "created_at": "2019-08-24T14:15:22Z",
  "updated_at": "2019-08-24T14:15:22Z",
  "done": true,
  "description": "string",
  "error": {
    "code": 0,
    "message": "string",
    "details": [
      {
        "@type": "string"
      }
    ]
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
      "@type": "string"
    }
  ]
}
```

**Ответы**

**200 OK**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `id` required | string Идентификатор операции. |
| `resource_name` | string `<urn:cloud:SERVICE:ZONE_OPT:PROJECT_OPT:RESOURCE_TYPE_OPT>` Информация о ресурсе, над которым производится операция. |
| `resource_id` | string Уникальный идентификатор ресурса, над которым производится операция. |
| `created_at` | string `<date-time>` Время создания операции. |
| `updated_at` | string `<date-time>` Время последнего изменения операции. |
| `done` | boolean Флаг завершенности операции. 1. true — операция завершена. Операция считается завершенной, даже если в ходе ее выполнения возникла ошибка. 2. false — операция не завершена. |
| `description` | string Описание операции. От 0 до 255 символов. |
| `error` | object Результат операции в случае ошибки. |
| `code` | integer `<int32>` Код ошибки. |
| `message` | string Описание ошибки. |
| `details` | Array of objects (google.protobuf.Any) Дополнительная информация об ошибке. |
| `@type` | string URL-адрес или имя ресурса, которое определяет тип сериализованного сообщения. |
| `property name* additional property` | any |

**default Default error response**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `code` | integer `<int32>` Код ошибки. |
| `message` | string Описание ошибки. |
| `details` | Array of objects (google.protobuf.Any) Дополнительная информация об ошибке. |
| `@type` | string URL-адрес или имя ресурса, которое определяет тип сериализованного сообщения. |
| `property name* additional property` | any |

---

## Информация о стоимости используемых ресурсов Managed Kubernetes

**POST** `https://mk8s.api.cloud.ru/v2/billing/calculate-price`

**Описание**  
Получение расчета по предоставленным ресурсам.

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

**Request Body schema:** `application/json` required

| Параметр | Описание |
| --- | --- |
| `projectId` required | string Идентификатор проекта. |
| `master` | object Описание мастер-узла. |
| `count` | integer `<uint32>` Количество мастер-узлов. |
| `flavorId` | string Идентификатор типа |
| `nodePools` | Array of objects (CalculatePriceRequest_NodePool) Описание групп узлов. |
| `count` required | integer `<uint32>` Количество рабочих узлов в группе. |
| `disk` required | object Информация о хранилище для группы узлов. |
| `size` | string `<uint64>` Размер хранилища в ГБ. |
| `typeId` | string Идентификатор типа диска. |
| `flavorId` | string Идентификатор типа |
| `disks` | Array of objects (CalculatePriceRequest_Disk) Описание дисков. |
| `size` | string `<uint64>` Размер хранилища в ГБ. |
| `typeId` | string Идентификатор типа диска. |
| `rentPublicIpCount` | integer `<uint32>` Количество привязанных публичных IP-адресов в шт. |
| `addon` | object Описание плагина. |
| `addonName` | string Название плагина. |
| `clusterAttributes` | Array of objects (CalculatePriceRequest_ClusterAttribute) Описание аттрибутов кластера. |
| `name` | string `<enum>` Value: "NAME_PUBLIC_IP" |
| `count` | integer `<uint32>` |

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

**Ответы**

**200 OK**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `masterPrice` required | number `<double>` Стоимость мастер-узлов. |
| `nodePoolPrices` required | Array of objects (CalculatePriceResponse_NodePoolPrice) Стоимость групп узлов в разбивке по каждой группе. |
| `disk` | number `<double>` Стоимость использования диска в час. |
| `flavor` | number `<double>` Стоимость RAM, CPU в час. |
| `diskPrices` required | Array of numbers `<double>` [ items `<double>` ] Стоимость дополнительных дисков для томов в разбивке по дискам. |
| `rentPublicIpPrice` required | number `<double>` Стоимость аренды публичных IP. |
| `totalPricePerMonth` required | number `<double>` Итоговая стоимость за месяц. |
| `totalPricePerHour` required | number `<double>` Итоговая стоимость за час. |
| `addonPrice` required | number `<double>` Стоимость использования плагина. |

---

## Список групп пользователей

**GET** `/iam/v1/groups`

**Описание**  
Получение списка групп пользователей.

**Authorizations:**  
iam_token_account_scoped  
API Key: iam_token_account_scoped  
IAM token for account.  
Header parameter name: X-Auth-Token

**Ответы**

**200 OK**  
**Response Schema:** `*/*`

| Поле | Описание |
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

---

## Обновление названия или описания группы пользователей

**PATCH** `/iam/v1/groups/{group_id}`

**Описание**  
Обновляет название или описание группы пользователей.

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
| `group_id` required | string group id |

**Request Body schema:** `application/json` required

| Параметр | Описание |
| --- | --- |
| `description` | string |
| `name` | string |

**Ответы**

**200 OK**  
**Response Schema:** `*/*`

| Поле | Описание |
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

---

## Создание пользователя

**POST** `/iam/v1/service_users`

**Описание**  
Создает нового пользователя сервиса.

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

| Параметр | Описание |
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

| Поле | Описание |
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

| Поле | Описание |
| --- | --- |
| `code` | string |
| `message` | string |

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

---

## Удаление групп пользователей

**DELETE** `/iam/v1/service_users/{user_id}/groups`

**Описание**  
Удаляет группы пользователей.

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

| Параметр | Описание |
| --- | --- |
| `user_id` required | string user id |

**Request Body schema:** `application/json` required

| Параметр | Описание |
| --- | --- |
| `group_ids` | Array of strings |

**Ответы**

**204 No Content**  
**400 Bad Request**  
**Response Schema:** `*/*`

| Поле | Описание |
| --- | --- |
| `code` | string |
| `message` | string |

**401 Unauthorized**  
**404 Not Found**  
**Response Schema:** `*/*`

| Поле | Описание |
| --- | --- |
| `code` | string |
| `message` | string |

---

## Список событий

**GET** `/client/v2/event`

**Описание**  
Получение списка событий.

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

| Параметр | Описание |
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

**Ответы**

**200 Get event list**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `execution_time` | number |
| `item_count` | integer |
| `limit` | integer |
| `page` | integer |
| `progress` | integer |
| `result` | Array of objects (EventModel) |
| `status` | string |
| `task_id` required | string = 36 characters Unique task UUID v4 |

**303 Returns async result**  
**Response Schema:** `application/json`

| Поле | Описание |
| --- | --- |
| `execution_time` | number |
| `item_count` | integer |
| `limit` | integer |
| `page` | integer |
| `progress` | integer |
| `result` required | object Object which contains result of computed request |
| `status` | string |
| `task_id` required | string = 36 characters Unique task UUID v4 |