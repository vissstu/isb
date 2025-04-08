import json
import chardet
from constants import *

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

def main():
    try:
        # Определяем кодировку файла
        try:
            file_encoding = chardet.detect(open(INPUT_FILE_PATH, 'rb').read())['encoding']
            print(f"Кодировка файла: {file_encoding}")
        except Exception as e:
            print(f"Не удалось определить кодировку файла: {e}. Будем использовать {FILE_ENCODING}.")
            file_encoding = FILE_ENCODING

        # Читаем исходный текст из файла
        with open(INPUT_FILE_PATH, "r", encoding=file_encoding) as f:
            original_text = f.read().strip()

        # Шифрование текста
        rev_encrypted_text = reverse_alphabet_cipher(original_text)

        # Сохранение результатов
        with open(OUTPUT_FILE_PATH, "w", encoding=file_encoding) as f:
            f.write(rev_encrypted_text)

        # Сохранение ключа расшифровки в отдельный файл
        decipher_key = {char: key for key, char in DECIPHER_DICT_UPPER.items()}
        with open("decipher_key.json", "w", encoding=file_encoding) as f:
            json.dump(decipher_key, f, indent=4, ensure_ascii=False)

        print(f"Шифровка текста прошла!")
    except Exception as e:
        print(f"Не удалось зашифровать текст: {e} :(")


if __name__ == "__main__":
    main()