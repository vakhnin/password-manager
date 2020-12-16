import os
import unittest
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.models import Base, UserManager, UnitManager
from encryption_manager.models import get_secret_obj


class TestUserManager(unittest.TestCase):
    _session_for_user = None
    _session_for_unit = None
    _conn_sqlite = None
    _cursor_sqlite = None
    dir_path = 'tests' + os.sep + 'test_databases'
    file_path = dir_path + os.sep + 'users.sqlite'
    user_for_test = 'test-user'
    password_for_test = 'test-password'
    dir_units_path = ''.join([dir_path, os.sep, 'test_units'])
    file_units_path = ''.join([dir_units_path, os.sep, user_for_test, '.sqlite'])  

    def setUp(self) -> None:
        """Настройка окружения"""

        # Инициализация User
        # БД в памяти, без файла
        engine = create_engine(f'sqlite:///{self.file_path}', echo=False)

        # Создание файла БД, если его нет
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)
        Base.metadata.create_all(engine,
                                 tables=[Base.metadata.tables['users']])

        self._session_for_user = sessionmaker(bind=engine)()
        
        # Добавление тестового пользователя
        user_obj = UserManager(self._session_for_user, self.user_for_test)
        user_obj.add_user(self.password_for_test)
        
        # Инициализация Units
        engine = create_engine(f'sqlite:///{self.file_units_path}', echo=False)

        # Создание файла БД, если его нет
        if not os.path.isdir(self.dir_units_path):
            os.makedirs(self.dir_units_path)
        Base.metadata.create_all(engine,
                                 tables=[
                                     Base.metadata.tables["units"],
                                     Base.metadata.tables["categories"]
                                 ])

        self._session_for_unit = sessionmaker(bind=engine)()

        # Инициализация sqlite3
        self._conn_sqlite = sqlite3.connect(self.file_units_path)
        self._cursor_sqlite = self._conn_sqlite.cursor()

    def tearDown(self) -> None:
        """Чистка, после завершения тестов"""
        self._session_for_unit.close()
        self._conn_sqlite.close()
        # Если для того, чтобы посмотреть, что в БД,
        # комментируем строку ниже. Не забываем удалить
        # файл БД вручную, перед следующим прогоном
        os.remove(self.file_path)
        os.remove(self.file_units_path)
        #os.rmdir
        

    def test_add_unit(self):
        """
        check for add_unit
        """
        login_for_test = 'test-login'
        passlogin_for_test = 'test-passlogin'
        unit_obj = UnitManager(self._session_for_unit)

        unit_obj.add_unit(self.user_for_test, self.password_for_test, login_for_test, passlogin_for_test)

        sql = "SELECT login, password FROM units WHERE login = ? and alias = ?"
        self._cursor_sqlite.execute(sql, ([login_for_test, 'default']))
        result = self._cursor_sqlite.fetchall()
        
        # check that the result is only one line
        self.assertEqual(1, len(result))
        
        # check that 'login' field is correct
        self.assertEqual(login_for_test, result[0][0])
        
        # check that encrypted passlogin_for_test is written correctly
        secret_obj = get_secret_obj(self.user_for_test, self.password_for_test)
        encrypted_pass = secret_obj.encrypt(passlogin_for_test)
        self.assertEqual(secret_obj.decrypt(encrypted_pass), secret_obj.decrypt(result[0][1]))
        
        # сheck that exeption is occur when adding a unit that already exists
        exception_occur = False
        try:
            unit_obj.add_unit(self.user_for_test, self.password_for_test, login_for_test, passlogin_for_test)
        except Exception:
            exception_occur = True
        self.assertEqual(True, exception_occur)

    
if __name__ == '__main__':
    unittest.main()
