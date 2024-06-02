import requests
idcm = "" #id-дообученной модели
IAM =  "" #значение IAM-токена сервисного аккаунта.
folderId = "" #идентификаторкаталога
def generate_message(query):
    req = {
            "modelUri": f"ds://{idcm}", #подключение к дообученной модели yandexgpt на датасете
            "completionOptions": {
                "stream": False,
                "temperature": 0.1,
                "maxTokens": "2000"
            },
            "messages": [
                {
                "role": "user",
                "text": query
                }
            ]
    }
    headers = {"Authorization" : "Api-Key " + IAM,
            "x-folder-id": folderId, }
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers, json=req)
    if response.status_code == 200:
        return response.text
    return "bad request"