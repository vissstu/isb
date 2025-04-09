import chardet
import json

from constants import *


def read_file(filename):
    with open(filename, "r", encoding=FILE_ENCODING) as file:
        return file.read()

# Функция для шифрования в обратном порядке алфавита
def reverse_alphabet_cipher(text):
    encrypted_text = ''
    for char in text:
        if char.isupper():
            encrypted_text += CIPHER_DICT_UPPER.get(char, char)
        elif char.islower():
            encrypted_text += CIPHER_DICT_LOWER.get(char, char)
        else:
            encrypted_text += char
    return encrypted_text


def  save_encrypted_text(rev_encrypted_text):
    with open(OUTPUT_FILE_PATH, "w", encoding=FILE_ENCODING) as f:
        f.write(rev_encrypted_text)


def main():
    try:
        # Читаем исходный текст из файла
        original_text = read_file(INPUT_FILE_PATH)

        # Шифрование текста
        rev_encrypted_text = reverse_alphabet_cipher(original_text)

        # Сохранение результатов
        save_encrypted_text(rev_encrypted_text)

        # Сохранение ключа расшифровки в отдельный файл
        decipher_key = {char: key for key, char in DECIPHER_DICT_UPPER.items()}
        with open("decipher_key.json", "w", encoding=FILE_ENCODING) as f:
            json.dump(decipher_key, f, indent=4, ensure_ascii=False)

        print(f"Шифровка текста прошла!")
    except Exception as e:
        print(f"Не удалось зашифровать текст: {e} :(")


if __name__ == "__main__":
    main()