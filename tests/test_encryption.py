import random
import unittest

from encryption_manager.models import AESCipher, get_hash

PASSWORDCHARS = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
STRCHARS = ' abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


# Encryption module test
class TestEncryption(unittest.TestCase):

    def test_get_hashe(self):
        """ Тест функции get_hash. Задаем вручную пароль 1 и сравниваем с заранее определнном для него хешем"""
        password = '1'
        password_code = password.encode("utf-8")
        self.assertEqual(get_hash(password_code), '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b')

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

        count_tests = 30  # Количество проверяемых паролей и строк
        for _ in range(count_tests):
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
