import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzY0NjIxMTk4fQ.OTCszJuW6oVx7hgMLtEu0q0K2391K2CwRU3x9r9ZYdU"
}

requisition = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)

print(requisition)
print(requisition.json())
