import requests

url = "http://192.168.1.37:11434/api/chat"
data = {
    "model": "qwen3:4b",
    "prompt": "Как работает нейросеть?",
    "stream": False
}

response = requests.post(url, json=data)
if response.status_code == 200:
    print(response.json()["response"])
else:
    print("Ошибка:", response.text)