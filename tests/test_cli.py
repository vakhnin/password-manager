import unittest
import pathlib
from click.testing import CliRunner
from cli import cli
import database_manager.models as models_db


class TestCli(unittest.TestCase):
    _login_user = 'temp'
    _password_user = 'temp1234!@#$'
    _path_project = pathlib.Path.cwd() / 'tests'

    @classmethod
    def setUpClass(cls):
        """Инициация тестовой базы данных"""
        if not pathlib.Path.exists(cls._path_project):
            pathlib.Path.mkdir(cls._path_project)
        if not pathlib.Path.exists(cls._path_project / 'units'):
            pathlib.Path.mkdir(cls._path_project / 'units')    
        _file_db = cls._path_project / 'test_users.sqlite'
        _dir_units_dbs = cls._path_project / 'units'
        cls._test_BD = models_db.SQLAlchemyManager(
            file_db=_file_db, user=cls._login_user,
            dir_units_dbs=_dir_units_dbs
        )
        cls._test_BD.user_obj.add_user(cls._password_user)

    @classmethod
    def tearDownClass(cls):
        """Очистка сгенерированных тестовых данных"""
        pathlib.Path.unlink(cls._path_project / 'test_users.sqlite')
        pathlib.Path.unlink(cls._path_project / 'units' / f'{cls._login_user}.sqlite')
        pathlib.Path.rmdir(cls._path_project / 'units')
        

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_user_add(self):
        user_for_test = 'test_user1'
        password_for_test = 'test_password'
        with self.runner.isolated_filesystem() as tmpdir:
            pass
        import time
        time.sleep(5)
    
    def test_uadd(self):
        """
        Test uadd command
        """

        """
        Окружение не настроено. При запуске в корне, пишет в рабочую БД.
        После настройки нужно удалить return ниже
        """
        return

        # Данные для теста
        user_for_test = 'test_user1'
        password_for_test = 'test_password'

        with self.runner.isolated_filesystem():
            # Вызываем cli
            result = self.runner.invoke(cli,
                                        [
                                            'uadd',  # Команда
                                            '-u', user_for_test,  # Первая опция
                                            '-p', password_for_test  # Вторая опция
                                            ])

            self.assertEqual(result.exit_code, 0)  # Проверяем код возврата
            self.assertEqual(result.output, f'User named "{user_for_test}" created\n')  # Проверяем сообщение
            # об успешности создания пользователя

            # Проверяем cli при вводе с подсказками (можно посмотреть, как ниже  print(result.output) )
            result = self.runner.invoke(cli, input=f'{user_for_test}\n{password_for_test}\n',  # Опции. Построчно
                                        args=['uadd'])  # Команда

            self.assertNotEqual(result.exit_code, 0)  # Пользователь уже есть, поэтому код возврата не 0
            # Нужно всем неуспешным завершениям проставить exit(-1), как в этом коммите
            res_str = result.output.split('\n')  # Делим вывод построчно
            self.assertEqual(res_str[-2], f'Error: User named "{user_for_test}" already exists') # Проверяем нижнюю
            # строку на соответсвии тексту ошибки

            print(result.exit_code)  # Вывод кода возврата (помошь при написании тестов,
            # в рабочем варианте нужно удалить
            print(result.output)  # Вывод всего вывода утилиты


if __name__ == '__main__':
    unittest.main()
