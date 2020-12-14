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
        check for add_user
        """
        user_for_test = 'test-user'
        password_for_test = 'test-password'
        user_obj = UserManager(self._session_for_user, user_for_test)

        user_obj.add_user(password_for_test)

        sql = "SELECT user, password FROM users WHERE user = ?"
        self._cursor_sqlite.execute(sql, ([user_for_test]))
        result = self._cursor_sqlite.fetchall()

        # check that the result is only one line
        self.assertEqual(1, len(result))
        # check that 'user' field is correct
        self.assertEqual(user_for_test, result[0][0])
        # check that the hash(user + password) is written correctly
        pass_hash = get_hash((user_for_test + password_for_test).encode("utf-8"))
        self.assertEqual(pass_hash, result[0][1])
        # сheck that exeption is occur when adding a user that already exists
        exception_occur = False
        try:
            user_obj.add_user(password_for_test)
        except Exception:
            exception_occur = True
        self.assertEqual(True, exception_occur)

    def test_check_user(self):
        """
        check for check_user
        """
        # add user to BD
        user_for_test = 'test-user'
        password_for_test = 'test-password'
        user_obj = UserManager(self._session_for_user, user_for_test)
        user_obj.add_user(password_for_test)

        # check that the check_user method confirms user existence in BD
        user_exist = user_obj.check_user()
        self.assertEqual(True, user_exist)
        
        # check that the check_user method confirms the absence of a user that hasn't been added to BD
        sql = "SELECT * FROM users WHERE user = ?"
        self._cursor_sqlite.execute(sql, (['non-existent-user']))
        result = self._cursor_sqlite.fetchall()
        self.assertEqual([], result)  # user 'non-existent-user' isn't exists in BD
        
        user_exist = user_obj.check_user('non-existent-user')
        self.assertEqual(False, user_exist)
        
    def test_check_user_password(self):
        """
        check for check_user_password
        """
        # add user to BD
        user_for_test = 'test-user'
        password_for_test = 'test-password'
        user_obj = UserManager(self._session_for_user, user_for_test)
        user_obj.add_user(password_for_test)

        # check that the check_user_password method confirms the correct password
        pass_is_correct = user_obj.check_user_password(password_for_test)
        self.assertEqual(True, pass_is_correct)
        # check that the check_user_password method doesn't confirm incorrect password
        pass_is_correct = user_obj.check_user_password('some-incorrect-password')
        self.assertEqual(False, pass_is_correct)
        
    def test_del_user(self):
        """
        check for del_user
        """
        # add user to BD
        user_for_test = 'test-user'
        password_for_test = 'test-password'
        user_obj = UserManager(self._session_for_user, user_for_test)
        user_obj.add_user(password_for_test)

        # delete user from BD, than check that it isn't exists in BD
        user_obj.del_user()
        user_exist = user_obj.check_user()
        self.assertEqual(False, user_exist)

    def test_all_users(self):
        """
        check for all_users
        """
        # create a sorted list of users with adding them to BD
        users_list = []
        for i in '654321':
            user_for_test = 'test-user-' + i
            password_for_test = 'test-password-' + i
            user_obj = UserManager(self._session_for_user, user_for_test)
            user_obj.add_user(password_for_test)
            users_list.append(user_for_test)
        users_list.sort()

        # check the equivalence of the list of users with the data from the all_users method
        users_list_from_BD = user_obj.all_users()
        self.assertEqual(users_list, users_list_from_BD)
        

if __name__ == '__main__':
    unittest.main()
