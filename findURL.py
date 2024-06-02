import json

# Функция для поиска совпадений и получения URL
def find_match_url(query):
    with open('dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    query_words = query.lower().split()
    for item in data['data']:
        title_words = item['title'].lower().split()
        if all(word in title_words for word in query_words):
            return item['url']
    return "https://www.tinkoff.ru/help/"
