import random
import unittest

from encryption_manager.models import AESCipher

PASSWORDCHARS = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
STRCHARS = ' abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


# Encryption module test
class TestEncryption(unittest.TestCase):
    def test_simple_string(self):
        """
        Тест проверяет шифровку и последующую расшифровку
        на статических пароле и строке
        """

        password = 'D&EXHb(48v'
        str_for_test = 'String for test!!!111'

        cipher = AESCipher(password)

        encrypted = cipher.encrypt(str_for_test)
        result = cipher.decrypt(encrypted)

        self.assertEqual(str_for_test, result)

    def test_simple_string_with_random_password_string(self):
        """
        Тест проверяет шифровку и последующую расшифровку
        на случайно сгенерированных пароле и строке
        """

        COUNTTESTS = 30  # Количество проверяемых паролей и строк
        for _ in range(COUNTTESTS):
            # генерация пароля
            password = ''
            for i in range(20):
                password += random.choice(PASSWORDCHARS)
            # генерация строки
            str_for_test = ''
            for i in range(100):
                str_for_test += random.choice(STRCHARS)

            cipher = AESCipher(password)

            encrypted = cipher.encrypt(str_for_test)
            result = cipher.decrypt(encrypted)

            self.assertEqual(str_for_test, result)


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
