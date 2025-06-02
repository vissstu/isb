import const

from hybrid_crypto_system import HybridCryptoSystem
from file_work import file_exists


class CryptoManager:
    @staticmethod
    def generate_keys(sym_key_path=const.PATH_TO_SYM_KEY,
                      pub_key_path=const.PATH_TO_PUBLIC_KEY,
                      priv_key_path=const.PATH_TO_PRIVATE_KEY,
                      camellia_key_size=const.DEFAULT_CAMELLIA_KEY_SIZE):
        """
        Генерация ключевой пары.
        Параметры:
            sym_key_path: Путь к файлу симметричного ключа
            pub_key_path: Путь к публичному ключу RSA
            priv_key_path: Путь к приватному ключу RSA
            camellia_key_size: Размер ключа Camellia в битах
        """
        crypto = HybridCryptoSystem()
        crypto.generate_keys(camellia_key_size)
        crypto.save_keys(sym_key_path, pub_key_path, priv_key_path)
        print(f"Ключи сгенерированы (Camellia: {camellia_key_size} бит)")

    @staticmethod
    def encrypt_file(input_path, output_path=const.PATH_TO_ENCRYPTED_FILE,
                     priv_key_path=const.PATH_TO_PRIVATE_KEY,
                     sym_key_path=const.PATH_TO_SYM_KEY):
        """
        Шифрование файла.
        Параметры:
            input_path: Путь к исходному файлу
            output_path: Путь для зашифрованного файла
            priv_key_path: Путь к приватному ключу RSA
            sym_key_path: Путь к симметричному ключу
        Возвращает:
            bool: Статус операции
        """
        if not file_exists(input_path):
            print(f"Файл не найден: {input_path}")
            return False

        crypto = HybridCryptoSystem()
        if not crypto.load_keys(sym_key_path, priv_key_path):
            print("Ошибка загрузки ключей")
            return False

        if crypto.encrypt_file(input_path, output_path):
            print(f"Файл зашифрован: {input_path} → {output_path}")
            return True
        return False

    @staticmethod
    def decrypt_file(input_path, output_path=const.PATH_TO_DECRYPTED_FILE,
                     priv_key_path=const.PATH_TO_PRIVATE_KEY,
                     sym_key_path=const.PATH_TO_SYM_KEY):
        """
        Дешифрование файла.
        Параметры:
            input_path: Путь к зашифрованному файлу
            output_path: Путь для расшифрованного файла
            priv_key_path: Путь к приватному ключу RSA
            sym_key_path: Путь к симметричному ключу
        Возвращает:
            bool: Статус операции
        """
        if not file_exists(input_path):
            print(f"Файл не найден: {input_path}")
            return False

        crypto = HybridCryptoSystem()
        if not crypto.load_keys(sym_key_path, priv_key_path):
            print("Ошибка загрузки ключей")
            return False

        if crypto.decrypt_file(input_path, output_path):
            print(f"Файл расшифрован: {input_path} → {output_path}")
            return True
        return False