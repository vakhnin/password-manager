import unittest

from click.testing import CliRunner

from cli import cli


class TestCli(unittest.TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

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
