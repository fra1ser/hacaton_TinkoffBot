import json
from flask import Flask, request, jsonify
from gpt import generate_message
from findURL import find_match_url
app = Flask(__name__)
@app.route('/assist', methods=['POST'])
def assist():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({
            "detail": [
                {
                    "loc": ["body", "query"],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }), 422

    query = data['query']
    print("generation started")
    response_text = generate_message(query)
    try:
        result = json.loads(response_text)
        result_latest = result['result']['alternatives'][0]['message']['text']
        linkSearch = find_match_url(query)
        return jsonify({
            "text": result_latest,
            "links": linkSearch
        }), 200
    except:

        return jsonify({
            "text": "Наблюдаются ошибки в работе бота. Мы постараемся оперативно их решить.",
            "links": "https://www.tinkoff.ru/help/"
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
