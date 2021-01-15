from valid_all import fnc
import json

if __name__ == '__main__':
    with open('json_test.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # загружаем из файла данные в словарь data
    fnc(data)
