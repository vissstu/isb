import json
from constants import *

def read_decryption_key(file_path):
    with open(file_path, 'r', encoding=FILE_ENCODING) as file:
        decryption_key = json.load(file)
    return decryption_key

def decrypt_text(ciphertext, decryption_key):
    plaintext = ''
    for char in ciphertext:
        if char in decryption_key:
            plaintext += decryption_key[char]
        else:
            plaintext += char  # Оставляем символы, которых нет в ключе, без изменений
    return plaintext

def read_file(filename):
    with open(filename, "r", encoding=FILE_ENCODING) as file:
        return file.read()

def write_to_file(filename, content):
    with open(filename, 'w', encoding=FILE_ENCODING) as file:
        file.write(content)


def frequency_calculation(text):
    text_length = len(text)
    counts = {}

    for char in text:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1

    # Преобразование в список кортежей с частотами
    frequencies = []
    for char, count in counts.items():
        frequencies.append((char, count / text_length))

    # Сортировка по частоте в порядке убывания
    def get_second_item(item):
        return item[1]

    frequencies.sort(key=get_second_item, reverse=True)
    return frequencies


def main():
    try:
        # Чтение зашифрованного текста
        original_text = read_file(INPUT_FILE_PATH)

        # Расчет частот символов в зашифрованном тексте
        frequencies = frequency_calculation(original_text)

        # Вывод частот символов в зашифрованном тексте
        print("\nИндекс частот появления символов:")
        print(frequencies)

        # Чтение ключа дешифрации
        decryption_key = read_decryption_key('decryption_key.json')

        # Расшифровка текста с использованием ключа дешифрации
        decrypted_text = decrypt_text(original_text, decryption_key)
        write_to_file('decrypted_text.txt', decrypted_text)
        print("\nРасшифровка прошла успешно!")

    except Exception as e:
        print(f"Произошла ошибка при попытке открыть или прочитать файл: {e}")

if __name__ == "__main__":
    main()