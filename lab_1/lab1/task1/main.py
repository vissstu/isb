import chardet
import json

from constants import *


def read_file(filename):
    """
    Читает содержимое файла и возвращает его в виде строки.

    :param filename: Путь к файлу, который нужно прочитать.
    :return: Содержимое файла.
    """
    with open(filename, "r", encoding=FILE_ENCODING) as file:
        return file.read()


def reverse_alphabet_cipher(text):
    """
    Шифрует текст, заменяя каждую букву на противоположную ей в алфавите.

    :param text: Исходный текст для шифрования.
    :return: Зашифрованный текст.
    """
    encrypted_text = ''
    for char in text:
        if char.isupper():
            encrypted_text += CIPHER_DICT_UPPER.get(char, char)
        elif char.islower():
            encrypted_text += CIPHER_DICT_LOWER.get(char, char)
        else:
            encrypted_text += char
    return encrypted_text


def save_encrypted_text(rev_encrypted_text):
    """
    Сохраняет зашифрованный текст в файл.

    :param rev_encrypted_text: Зашифрованный текст.
    """
    with open(OUTPUT_FILE_PATH, "w", encoding=FILE_ENCODING) as f:
        f.write(rev_encrypted_text)


def generate_decipher_key():
    """
    Генерирует ключ для расшифровки зашифрованного текста.

    :return: Словарь, содержащий пары символ-значение для расшифровки.
    """
    return {char: key for key, char in DECIPHER_DICT_UPPER.items()}


def save_decipher_key(decipher_key):
    """
    Сохраняет ключ для расшифровки в файл.

    :param decipher_key: Ключ для расшифровки.
    """
    with open(KEY_FILE_PATH, "w", encoding=FILE_ENCODING) as f:
        json.dump(decipher_key, f, indent=4, ensure_ascii=False)


def main():
    """
    Основная функция программы. Читает текст из файла, шифрует его, сохраняет зашифрованный текст и ключ для расшифровки.
    """
    try:
        # Читаем исходный текст из файла
        original_text = read_file(INPUT_FILE_PATH)

        # Шифруем текст
        rev_encrypted_text = reverse_alphabet_cipher(original_text)

        # Сохраняем зашифрованный текст
        save_encrypted_text(rev_encrypted_text)

        # Генерируем и сохраняем ключ для расшифровки
        decipher_key = generate_decipher_key()
        save_decipher_key(decipher_key)

        print(f"Шифровка текста прошла!")
    except Exception as e:
        print(f"Не удалось зашифровать текст: {e} :(")


if __name__ == "__main__":
    main()
