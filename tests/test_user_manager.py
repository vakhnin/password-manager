import os
import unittest
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.models import Base, UserManager
from encryption_manager.models import get_hash


class TestUserManager(unittest.TestCase):
    _session_for_user = None
    _conn_sqlite = None
    _cursor_sqlite = None
    file_path = 'databases/users.sqlite'

    def setUp(self) -> None:
        """Настройка окружения"""

        # Инициализация User
        # БД в памяти, без файла
        engine = create_engine(f'sqlite:///{self.file_path}', echo=False)

        # Создание файла БД, если его нет
        Base.metadata.create_all(engine,
                                 tables=[Base.metadata.tables['users']])

        self._session_for_user = sessionmaker(bind=engine)()

        # Инициализация sqlite3
        self._conn_sqlite = sqlite3.connect(self.file_path)
        self._cursor_sqlite = self._conn_sqlite.cursor()

    def tearDown(self) -> None:
        """Чистка, после завершения тестов"""
        self._session_for_user.close()
        self._conn_sqlite.close()
        # Если для того, чтобы посмотреть, что в БД,
        # комментируем строку ниже. Не забываем удалить
        # файл БД вручную, перед следующим прогоном
        os.remove(self.file_path)

    def test_add_user(self):
        """
        Проверка метод add_user
        """
        user_for_test = 'test-user'
        password_for_test = 'test-password'
        user_obj = UserManager(self._session_for_user, user_for_test)

        user_obj.add_user(password_for_test)

        sql = "SELECT user, password FROM users WHERE user = ?"
        self._cursor_sqlite.execute(sql, ([user_for_test]))
        result = self._cursor_sqlite.fetchall()

        # проверяем что результат только одна строка
        self.assertEqual(1, len(result))
        # проверяем, что поле user верное
        self.assertEqual(user_for_test, result[0][0])
        # Дальше проверяем что хэш user + password записан верно.
        # Проверяем добавление еще одного пользователя. Проверяем
        # что выдается exeption, при добавлении пользоввателя, который уже существует
        # и так далее ...

    def test_check_user(self):
        """
        Проверяем метод check_user, по аналогии с test_add_user
        И далее, остальные методы
        """


if __name__ == '__main__':
    unittest.main()
