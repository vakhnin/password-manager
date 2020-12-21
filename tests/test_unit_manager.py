import os
import sqlite3
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.models import Base, UnitManager, UserManager
from encryption_manager.models import get_secret_obj


class TestUnitManager(unittest.TestCase):
    _session_for_user = None
    _session_for_unit = None
    _conn_sqlite = None
    _cursor_sqlite = None
    dir_path = 'tests' + os.sep + 'test_databases'
    file_path = dir_path + os.sep + 'users.sqlite'
    _test_user = 'test-user'
    _test_pwd_user = 'T_u!123'
    dir_units_path = ''.join([dir_path, os.sep, 'test_units'])
    file_units_path = ''.join([dir_units_path, os.sep, _test_user, '.sqlite'])
    _test_login = 'test-login'
    _test_pwd_login = 'T_l!456'
    _test_alias = 'test-alias'

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
        user_obj = UserManager(self._session_for_user, self._test_user)
        user_obj.add_user(self._test_pwd_user)
        
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
        # os.rmdir

    def test_add_unit(self):
        """
        check for add_unit
        """
        # add unit to DB
        unit_obj = UnitManager(self._session_for_unit)
        unit_obj.add_unit(self._test_user, self._test_pwd_user, self._test_login, self._test_pwd_login)

        # checking query
        sql = "SELECT login, password FROM units WHERE login = ? and alias = ?"
        self._cursor_sqlite.execute(sql, ([self._test_login, 'default']))
        result = self._cursor_sqlite.fetchall()
        
        # check that the result is only one line
        self.assertEqual(1, len(result))
        
        # check that 'login' field is correct
        self.assertEqual(self._test_login, result[0][0])
        
        # check that encrypted password for login is written correctly
        secret_obj = get_secret_obj(self._test_user, self._test_pwd_user)
        encrypted_pass = secret_obj.encrypt(self._test_pwd_login)
        self.assertEqual(secret_obj.decrypt(encrypted_pass), secret_obj.decrypt(result[0][1]))
        
        # сheck that exeption is occur when adding a unit that already exists
        exception_occur = False
        try:
            unit_obj.add_unit(self._test_user, self._test_pwd_user, self._test_login, self._test_pwd_login)
        except Exception:
            exception_occur = True
        self.assertEqual(True, exception_occur)

    def test_check_login(self):
        """
        check for check_login
        """
        # add unit to DB
        unit_obj = UnitManager(self._session_for_unit)
        unit_obj.add_unit(self._test_user, self._test_pwd_user, self._test_login, self._test_pwd_login)

        # check that the check_login method confirms unit existence in DB by key login + default alias
        unit_exist = False
        if unit_obj.check_login(self._test_login, alias='default'):
            unit_exist = True
        self.assertEqual(True, unit_exist)

        # check that unit with 'non-existent-login' and default alias doesn't exist in DB
        sql = "SELECT * FROM units WHERE login = ? and alias = ?"
        self._cursor_sqlite.execute(sql, (['non-existent-login', 'default']))
        result = self._cursor_sqlite.fetchall()
        self.assertEqual([], result)

        # check that the check_login method confirms the absence of a unit that hasn't been added to DB
        unit_exist = False
        if unit_obj.check_login('non-existent-login', alias='default'):
            unit_exist = True
        self.assertEqual(False, unit_exist)

    
if __name__ == '__main__':
    unittest.main()
