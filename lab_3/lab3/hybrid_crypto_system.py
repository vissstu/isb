import const
from camellia import CamelliaCipher, generate_camellia_key
from rsa import encrypt_rsa, decrypt_rsa, save_rsa_keys, load_rsa_private_key, generate_rsa_keys
from file_work import read_file, write_file


class HybridCryptoSystem:
    def __init__(self):
        """
        Инициализирует новую гибридную криптосистему.
        При создании все ключи системы инициализируются значением None.
        """
        self.camellia_key = None  # Симметричный ключ для Camellia
        self.rsa_public_key = None  # Публичный ключ RSA
        self.rsa_private_key = None  # Приватный ключ RSA

    def generate_keys(self, camellia_key_size=const.DEFAULT_CAMELLIA_KEY_SIZE, rsa_key_size=2048):
        """
        Генерирует новые криптографические ключи для системы.
        Параметры:
            camellia_key_size (int): Размер ключа Camellia в битах (128, 192 или 256)
            rsa_key_size (int): Размер ключа RSA в битах (по умолчанию 2048)
        Возвращает:
            tuple: Кортеж из трех элементов (camellia_key, rsa_public_key, rsa_private_key)
        Исключения:
            ValueError: Если указан неподдерживаемый размер ключа Camellia
        """
        if camellia_key_size not in const.CAMELLIA_KEY_SIZES:
            raise ValueError(
                f"Недопустимый размер ключа Camellia ({camellia_key_size} бит). "
                f"Допустимые значения: {const.CAMELLIA_KEY_SIZES}"
            )
        self.camellia_key = generate_camellia_key(camellia_key_size)
        self.rsa_private_key, self.rsa_public_key = generate_rsa_keys(rsa_key_size)
        return self.camellia_key, self.rsa_public_key, self.rsa_private_key

    def save_keys(self, symmetric_key_path=const.PATH_TO_SYM_KEY,
                  public_key_path=const.PATH_TO_PUBLIC_KEY,
                  private_key_path=const.PATH_TO_PRIVATE_KEY):
        """
        Сохраняет все ключи системы в указанные файлы.
        Параметры:
            symmetric_key_path (str): Путь для сохранения зашифрованного ключа Camellia
            public_key_path (str): Путь для сохранения публичного ключа RSA
            private_key_path (str): Путь для сохранения приватного ключа RSA
        Возвращает:
            bytes: Зашифрованный ключ Camellia
        Исключения:
            ValueError: Если ключи не были сгенерированы
        """
        encrypted_cam_key = self.encrypt_camellia_key()
        write_file(symmetric_key_path, encrypted_cam_key)
        save_rsa_keys(self.rsa_private_key, self.rsa_public_key, private_key_path, public_key_path)
        return encrypted_cam_key

    def encrypt_camellia_key(self):
        """
        Шифрует симметричный ключ Camellia с помощью RSA.
        Возвращает:
            bytes: Зашифрованный ключ Camellia
        Исключения:
            ValueError: Если ключи Camellia или RSA не инициализированы
        """
        if not self.camellia_key or not self.rsa_public_key:
            raise ValueError("Ключи не инициализированы")
        return encrypt_rsa(self.rsa_public_key, self.camellia_key)

    def decrypt_camellia_key(self, encrypted_key):
        """
        Расшифровывает ключ Camellia с помощью RSA.
        Параметры:
            encrypted_key (bytes): Зашифрованный ключ Camellia
        Возвращает:
            bytes: Расшифрованный ключ Camellia
        Исключения:
            ValueError: Если приватный ключ RSA не установлен
        """
        if not self.rsa_private_key:
            raise ValueError("Приватный ключ RSA не установлен")
        self.camellia_key = decrypt_rsa(self.rsa_private_key, encrypted_key)
        return self.camellia_key

    def load_keys(self, symmetric_key_path=const.PATH_TO_SYM_KEY,
                  private_key_path=const.PATH_TO_PRIVATE_KEY):
        """
        Загружает ключи из файлов.
        Параметры:
            symmetric_key_path (str): Путь к файлу с зашифрованным ключом Camellia
            private_key_path (str): Путь к файлу с приватным ключом RSA
        Возвращает:
            bytes: Расшифрованный ключ Camellia или None при ошибке
        """
        self.rsa_private_key = load_rsa_private_key(private_key_path)
        encrypted_cam_key = read_file(symmetric_key_path)
        if encrypted_cam_key:
            return self.decrypt_camellia_key(encrypted_cam_key)
        return None

    def encrypt_file(self, input_file=const.PATH_TO_INPUT_FILE,
                     output_file=const.PATH_TO_ENCRYPTED_FILE):
        """
        Шифрует файл с помощью Camellia.
        Параметры:
            input_file (str): Путь к исходному файлу
            output_file (str): Путь для сохранения зашифрованного файла
        Возвращает:
            bytes: Зашифрованные данные или None при ошибке
        Исключения:
            ValueError: Если ключ Camellia не установлен
        """
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        plaintext = read_file(input_file)
        if plaintext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        ciphertext = cipher.encrypt(plaintext)
        write_file(output_file, ciphertext)
        return ciphertext

    def decrypt_file(self, input_file=const.PATH_TO_ENCRYPTED_FILE,
                     output_file=const.PATH_TO_DECRYPTED_FILE):
        """
        Расшифровывает файл, зашифрованный Camellia.
        Параметры:
            input_file (str): Путь к зашифрованному файлу
            output_file (str): Путь для сохранения расшифрованного файла
        Возвращает:
            bytes: Расшифрованные данные или None при ошибке
        Исключения:
            ValueError: Если ключ Camellia не установлен
        """
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        ciphertext = read_file(input_file)
        if ciphertext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        plaintext = cipher.decrypt(ciphertext)
        write_file(output_file, plaintext)
        return plaintext