from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_manager.models import Base, Unit, User
from utils.crypt import get_hash, get_secret_obj
from utils.settings import FILE_DB
from utils.show import UnitData


class UserManager:
    """Класс работы с user"""
    _session = None
    _user = None

    def __init__(self, session, user):
        self._session = session
        self._user = user

    def check_user(self, user=None):
        """
        check user existence in BD
        """
        user_tmp = self._user
        if user:
            user_tmp = user

        if self._session.query(User).filter(User.user == user_tmp).first():
            self._session.close()
            return True
        return False

    def check_user_password(self, password):
        """
        check user password in BD
        """
        pass_hash = get_hash((self._user + password).encode("utf-8"))
        if self._session.query(User).filter(User.user == self._user) \
                .filter(User.password == pass_hash).first():
            self._session.close()
            return True
        return False

    def add_user(self, password):
        """
        add user to BD
        """
        pass_hash = get_hash((self._user + password).encode("utf-8"))
        user_for_add = User(self._user, pass_hash)
        self._session.add(user_for_add)
        self._session.commit()
        self._session.close()

    def update_user(self, db, password, new_user, new_password=None):
        """
        update username (and password) in BD
        """
        if not new_password:
            new_password = password

        manager_obj = SQLAlchemyManager(db, self._user)
        for unit in manager_obj.unit_obj.get_logins():
            password_for_login = \
                manager_obj.unit_obj.get_password(
                    self._user, password, unit.login, unit.name)
            manager_obj.unit_obj \
                .update_unit(new_user, new_password, unit.login,
                             password_for_login=password_for_login, name=unit.name)

        if new_password:
            secret_password = new_user + new_password
        else:
            secret_password = new_user + password
        pass_hash = get_hash(secret_password.encode("utf-8"))
        self._session.query(User) \
            .filter(User.user == self._user) \
            .update({"user": new_user, "password": pass_hash})

        self._session.commit()

    def del_user(self):
        """
        delete user from BD
        """
        self._session.query(Unit) \
            .filter(Unit.user.has(User.user == self._user)) \
            .delete(synchronize_session='fetch')
        self._session.query(User) \
            .filter(User.user == self._user).delete()
        self._session.commit()

    def all_users(self):
        """
        list of users
        """
        users_list = []
        users = self._session.query(User).all()
        for user in users:
            users_list.append(user.user)
        users_list.sort()
        return users_list


class UnitManager:
    """Класс работы с unit"""
    _session = None
    _user = None

    def __init__(self, session, user):
        self._session = session
        self._user = user

    def get_logins(self, category=None):
        """Выдача units"""

        def make_logins_obj(units_list):
            """Выдача логинов, из списка"""
            units_obj = []

            if units_list:
                for unit in units_list:
                    units_obj.append(UnitData(
                        unit.login,
                        unit.name,
                        unit.category,
                        unit.url if unit.url else '',
                    ))
            return units_obj

        if category:
            units = self._session.query(Unit) \
                .filter(Unit.user.has(User.user == self._user)
                        & (Unit.category == category)).all()
            return make_logins_obj(units)
        else:
            units = self._session.query(Unit) \
                .filter(Unit.user.has(User.user == self._user)).all()
            return make_logins_obj(units)

    def check_login(self, login, name):
        """Проверка существования логина"""
        return self._session.query(Unit) \
            .filter(Unit.user.has(User.user == self._user) & (Unit.login == login)
                    & (Unit.name == name)).all()

    def get_category(self, category):
        """Выдаем категорию, если есть, иначе создаем"""
        return self._session.query(Unit) \
            .filter(Unit.category == category).first()

    def get_user(self):
        """Выдаем пользователя"""
        return self._session.query(User).filter(User.user == self._user).first()

    def add_unit(self, user, password, login, password_for_login, name='default',
                 category='default', url=None):
        """Добавление unit"""
        secret_obj = get_secret_obj(user, password)
        unit_for_add = Unit(login,
                            secret_obj.encrypt(password_for_login), url, name, category)
        self._session.add(unit_for_add)
        unit_for_add.user = self.get_user()
        self._session.commit()

    def get_password(self, user, password, login, name):
        """Получение пароля"""
        secret_obj = get_secret_obj(user, password)
        unit_obj = self._session.query(Unit) \
            .filter(Unit.user.has(User.user == self._user) &
                    (Unit.login == login) & (Unit.name == name)).first()
        return secret_obj.decrypt(unit_obj.password)

    def update_unit(self, user, password, login, name, new_login=None, password_for_login=None,
                    new_category=None, url=None, new_name=None):
        """Обновление unit"""
        update_dict = {'login': login}
        if new_login:
            update_dict['login'] = new_login
        if password_for_login:
            secret_obj = get_secret_obj(user, password)
            update_dict['password'] = secret_obj.encrypt(password_for_login)
        if url:
            update_dict['url'] = url
        if new_name:
            update_dict['name'] = new_name
        if new_category:
            update_dict['category'] = new_category

        self._session.query(Unit) \
            .filter(Unit.user.has(User.user == self._user)
                    & (Unit.login == login) & (Unit.name == name)) \
            .update(update_dict, synchronize_session='fetch')
        self._session.commit()

    def delete_unit(self, login, name):
        """Удаление unit"""
        self._session.query(Unit) \
            .filter(Unit.user.has(User.user == self._user)
                    & (Unit.login == login) & (Unit.name == name)) \
            .delete(synchronize_session='fetch')
        self._session.commit()


class SQLAlchemyManager:
    """Менеджер управления БД, предположительно будет отвечать за установление
    коннектов с базой, CRUD(Create, Read, Update, Delete) по хранящимся юнитам"""
    _file_user_db = ''
    _session_for_user = None
    _session_for_unit = None

    _user = None

    user_obj = None
    unit_obj = None

    @property
    def file_user_db(self):
        return self._file_user_db

    @property
    def session_for_user(self):
        return self._session_for_user

    @property
    def session_for_unit(self):
        return self._session_for_unit

    @property
    def user(self):
        return self._user

    def __init__(self, file_db=FILE_DB, user=None):
        """Инициализация класса при вызове с поднятием текущей сессии"""
        self._user = user
        self._file_user_db = file_db

        # Инициализация User
        engine = create_engine(f'sqlite:///{self.file_user_db}', echo=False)

        # Создание файла БД, если его нет
        Base.metadata.create_all(engine)

        self._session_for_user = sessionmaker(bind=engine)()

        self.user_obj = UserManager(self.session_for_user, self.user)
        self.unit_obj = UnitManager(self.session_for_user, self.user)
