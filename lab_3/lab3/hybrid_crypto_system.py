import const

from camellia import CamelliaCipher, generate_camellia_key
from rsa import encrypt_rsa, decrypt_rsa, save_rsa_keys, load_rsa_private_key, generate_rsa_keys
from file_work import read_file, write_file


class HybridCryptoSystem:
    def __init__(self):
        self.camellia_key = None
        self.rsa_public_key = None
        self.rsa_private_key = None

    def generate_keys(self, camellia_key_size=const.DEFAULT_CAMELLIA_KEY_SIZE, rsa_key_size=2048):
        # Проверка допустимого размера ключа
        if camellia_key_size not in const.CAMELLIA_KEY_SIZES:
            raise ValueError(
                f"Недопустимый размер ключа Camellia ({camellia_key_size} бит). "
                f"Допустимые значения: {const.CAMELLIA_KEY_SIZES}"
            )
        self.camellia_key = generate_camellia_key(camellia_key_size)
        self.rsa_private_key, self.rsa_public_key = generate_rsa_keys(rsa_key_size)
        return self.camellia_key, self.rsa_public_key, self.rsa_private_key

    def save_keys(self, symmetric_key_path=const.PATH_TO_SYM_KEY, public_key_path=const.PATH_TO_PUBLIC_KEY,
                  private_key_path=const.PATH_TO_PRIVATE_KEY):
        encrypted_cam_key = self.encrypt_camellia_key()
        write_file(symmetric_key_path, encrypted_cam_key)
        save_rsa_keys(self.rsa_private_key, self.rsa_public_key, private_key_path, public_key_path)
        return encrypted_cam_key

    def encrypt_camellia_key(self):
        if not self.camellia_key or not self.rsa_public_key:
            raise ValueError("Ключи не инициализированы")
        return encrypt_rsa(self.rsa_public_key, self.camellia_key)

    def decrypt_camellia_key(self, encrypted_key):
        if not self.rsa_private_key:
            raise ValueError("Закрытый ключ RSA не установлен")
        self.camellia_key = decrypt_rsa(self.rsa_private_key, encrypted_key)
        return self.camellia_key

    def load_keys(self, symmetric_key_path=const.PATH_TO_SYM_KEY,
                  private_key_path=const.PATH_TO_PRIVATE_KEY):
        self.rsa_private_key = load_rsa_private_key(private_key_path)
        encrypted_cam_key = read_file(symmetric_key_path)
        if encrypted_cam_key:
            return self.decrypt_camellia_key(encrypted_cam_key)
        return None

    def encrypt_file(self, input_file=const.PATH_TO_INPUT_FILE, output_file=const.PATH_TO_ENCRYPTED_FILE):
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        plaintext = read_file(input_file)
        if plaintext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        ciphertext = cipher.encrypt(plaintext)
        write_file(output_file, ciphertext)
        return ciphertext

    def decrypt_file(self, input_file=const.PATH_TO_ENCRYPTED_FILE, output_file=const.PATH_TO_DECRYPTED_FILE):
        if not self.camellia_key:
            raise ValueError("Ключ Camellia не установлен")

        ciphertext = read_file(input_file)
        if ciphertext is None:
            return None

        cipher = CamelliaCipher(self.camellia_key)
        plaintext = cipher.decrypt(ciphertext)
        write_file(output_file, plaintext)
        return plaintext
