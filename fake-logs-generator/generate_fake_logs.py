# import requests
# import random
# import time
# from datetime import datetime

# OPENSEARCH_URL = "http://opensearch:9200"
# INDEX = "rest_api_logs/_doc"

# methods = ["GET", "POST", "PUT", "DELETE"]
# status_codes = [200, 201, 400, 404, 500]

# def generate_log():
#     return {
#         "timestamp": datetime.utcnow().isoformat(),
#         "method": random.choice(methods),
#         "duration": round(random.uniform(0.1, 2.5), 3),
#         "status_code": random.choice(status_codes)
#     }

# def send_log(log):
#     try:
#         response = requests.post(f"{OPENSEARCH_URL}/{INDEX}", json=log)
#         print(response.status_code, response.text)
#     except Exception as e:
#         print(f"Ошибка отправки данных: {e}")

# # Отправка логов непрерывно с задержкой в 1 секунду
# while True:
#     log = generate_log()
#     send_log(log)
#     time.sleep(1)

import requests
import random
import time

BASE_URL = "http://bx-nginx/rest/1/xk2tr9yhrdnrzuc2"

# Список возможных запросов
requests_list = [
    {
        "url": f"{BASE_URL}/crm.deal.add",
        "json": {
            "fields": {"TITLE": "Тестовая сделка", "OPPORTUNITY": 10000, "CURRENCY_ID": "RUB"}
        }
    },
    {
        "url": f"{BASE_URL}/crm.deal.list",
        "json": {"filter": {">OPPORTUNITY": 5000}, "select": ["ID", "TITLE", "OPPORTUNITY"]}
    },
    {
        "url": f"{BASE_URL}/crm.deal.delete",
        "json": {"id": random.randint(100, 500)}
    },
    {
        "url": f"{BASE_URL}/crm.deal.productrows.get",
        "json": {"id": random.randint(100, 500)}
    },
    {
        "url": f"{BASE_URL}/crm.contact.add",
        "json": {
            "fields": {
                "NAME": "Иван",
                "LAST_NAME": "Иванов",
                "EMAIL": [{"VALUE": "ivan@example.com", "VALUE_TYPE": "WORK"}]
            }
        }
    },
    {
        "url": f"{BASE_URL}/crm.contact.list",
        "json": {"filter": {"EMAIL": "ivan@example.com"}, "select": ["ID", "NAME", "LAST_NAME"]}
    },
    {
        "url": f"{BASE_URL}/crm.lead.add",
        "json": {"fields": {"TITLE": "Новый лид", "STATUS_ID": "NEW", "SOURCE_ID": "WEB"}}
    },
    {
        "url": f"{BASE_URL}/tasks.task.add",
        "json": {
            "fields": {
                "TITLE": "Тестовая задача",
                "DESCRIPTION": "Описание задачи",
                "RESPONSIBLE_ID": 1,
                "DEADLINE": "2025-04-30"
            }
        }
    },
    {
        "url": f"{BASE_URL}/documentgenerator.document.add",
        "json": {"templateId": 1, "values": {"COMPANY_NAME": "Тестовая компания"}}
    },
    {
        "url": f"{BASE_URL}/crm.deal.update",
        "json": {
            "id": random.randint(100, 500),
            "fields": {"STAGE_ID": "WON", "OPPORTUNITY": 15000, "COMMENTS": "Успешно закрыта"}
        }
    },
    {
        "url": f"{BASE_URL}/crm.lead.convert.to.deal",
        "json": {"ID": random.randint(100, 500), "FIELDS": {"COMPANY_TITLE": "Новая компания", "CONTACT_LAST_NAME": "Петров"}}
    },
    {
        "url": f"{BASE_URL}/crm.product.add",
        "json": {"fields": {"NAME": "Ноутбук Lenovo X1 Carbon", "PRICE": 150000, "CURRENCY_ID": "RUB", "DESCRIPTION": "Премиальный бизнес-ноутбук"}}
    },
    {
        "url": f"{BASE_URL}/crm.dealcategory.list",
        "json": {"filter": {"IS_LOCKED": "N"}, "select": ["ID", "NAME", "SORT"]}
    }
]

# Бесконечный цикл отправки случайных запросов
while True:
    req = random.choice(requests_list)
    try:
        response = requests.post(req["url"], json=req["json"])
        print(f"Запрос: {req['url']}\nСтатус: {response.status_code}\nОтвет: {response.text}\n")
    except Exception as e:
        print(f"Ошибка запроса: {e}")

    # Случайный интервал от 1 до 5 секунд между запросами
    time.sleep(random.uniform(1, 5))