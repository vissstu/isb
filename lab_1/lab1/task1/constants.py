# Константы для русского алфавита
ALPHABET_UPPER = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
ALPHABET_LOWER = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


REVERSED_ALPHABET_UPPER = ALPHABET_UPPER[::-1]
REVERSED_ALPHABET_LOWER = ALPHABET_LOWER[::-1]

# Словари для шифрования и расшифровки
CIPHER_DICT_UPPER = {char: REVERSED_ALPHABET_UPPER[idx] for idx, char in enumerate(ALPHABET_UPPER)}
CIPHER_DICT_LOWER = {char: REVERSED_ALPHABET_LOWER[idx] for idx, char in enumerate(ALPHABET_LOWER)}


DECIPHER_DICT_UPPER = {value: key for key, value in CIPHER_DICT_UPPER.items()}
DECIPHER_DICT_LOWER = {value: key for key, value in CIPHER_DICT_LOWER.items()}

# Дополнительные константы
FILE_ENCODING = 'utf-8'

# Пути к файлам
INPUT_FILE_PATH = 'the original text.txt'
OUTPUT_FILE_PATH = 'encrypted text.txt'
KEY_FILE_PATH = 'decryption_key.json'