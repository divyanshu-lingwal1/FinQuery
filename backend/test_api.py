import requests

data = {
    "date": "2026-09-09",
    "description": "Bus ticket",
    "category": "Transport",
    "amount": 100
}

response = requests.post(
    "http://127.0.0.1:5000/api/transactions",
    json=data
)

print(response.json())