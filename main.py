import json
import re

# Путь к исходному файлу
input_file_path = 'dataset.json'
# Путь к файлу, который будет содержать данные в формате JSON Lines
output_file_path = 'formatted_dataset.jsonl'

# Максимальная длина ответа
MAX_RESPONSE_LENGTH = 2000

# Чтение данных из исходного файла
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Извлечение списка с данными
items = data['data']


# Функция для разбивки текста на части по предложениям
def split_text_by_sentences(text, max_length):
    sentences = re.split(r'(?<=\.) ', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_length:
            chunks.append(current_chunk.strip() + '\n')
            current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Создание нового файла в формате JSON Lines
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for item in items:
        response = item["description"]
        # Разбиение ответа на части по предложениям, если он превышает максимальную длину
        response_chunks = split_text_by_sentences(response, MAX_RESPONSE_LENGTH)
        # Запись каждой части в формате JSON Lines(Требует YandexGPT)
        for chunk in response_chunks:
            new_item = {
                "request": [
                    {"role": "system", "text": "Ты генеративный ассистент для помощи клиентам по бизнес вопросам. \n Работаешь с базой знаний Тинькофф-Помощи. \nТы говоришь коротко и емко. \nТы отвечаешь от лица мужского рода. \nТвое предназначение – помогать людям в сфере бизнес вопросов. \nТы эксперт в сфере бизнеса."},
                    {"role": "user", "text": item["title"]}
                ],
                "response": chunk
            }
            json.dump(new_item, outfile, ensure_ascii=False)
            outfile.write('\n')

print("Done")