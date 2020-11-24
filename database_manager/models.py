import os

from sqlalchemy import (Column, ForeignKey, Integer, PrimaryKeyConstraint,
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from main import get_hash

DIR_DB = 'databases'
DIR_UNITS_DBS = DIR_DB + os.sep + 'units'
FILE_USERS_DB = os.path.join(DIR_DB, 'users.sqlite')

if not os.path.exists(DIR_UNITS_DBS):
    os.makedirs(DIR_UNITS_DBS)

Base = declarative_base()


class User(Base):
    """Определение таблицы users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, unique=True,
                  sqlite_on_conflict_unique='FAIL')
    password = Column(String, nullable=False)

    # logins = relationship("Unit",
    #                       back_populates="user",
    #                       cascade="all, delete-orphan")

    def __init__(self, user, password):
        self.user = user
        self.password = password


class Unit(Base):
    """Определение таблицы units"""
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer,
    #                  ForeignKey('users.id',
    #                             ondelete="CASCADE"),
    #                  nullable=False)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # PrimaryKeyConstraint(user_id, login)
    # user = relationship("User", back_populates="logins")

    def __init__(self, login, password):
        self.login = login
        self.password = password


class UserManager:
    """Класс работы с unit"""
    _session = None
    _user = None

    def __init__(self, session, user):
        self._session = session
        self._user = user

    def check_user(self):
        """
        check user existence in BD
        """
        if self._session.query(User).filter(User.user == self._user).first():
            return True
        return False

    def check_user_password(self, password):
        """
        check user and password in BD
        """
        pass_hash = get_hash((self._user + password).encode("utf-8"))
        if self._session.query(User).filter(User.user == self._user) \
                .filter(User.password == pass_hash).first():
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

    def del_user(self):
        """DIR_UNITS_DBS + os.sep + user + ".sqlite"
        delete user from BD
        """
        self._session.query(User) \
            .filter(User.user == self._user).delete()
        os.remove(DIR_UNITS_DBS + os.sep + self._user + ".sqlite")
        self._session.commit()


class UnitManager:
    """Класс работы с unit"""
    _session = None
    _user = None

    def __init__(self, session, user):
        self._session = session
        self._user = user

    def all_logins(self):
        """Отображение всех логинов"""
        logins_list = []
        # user = self._session.query(User).filter(User.user == self._user).first()
        units = self._session.query(Unit).all()
        for unit in units:
            logins_list.append(unit.login)
        return logins_list

    def check_login(self, login):
        """Проверка существования логина"""
        return self._session.query(Unit).filter(Unit.login == login).first()
        # return login in self.all_logins()

    def add_unit(self, login, password_for_login):
        """Добавление unit"""
        unit_for_add = Unit(login, password_for_login)
        self._session.add(unit_for_add)
        # user = self._session.query(User).filter(User.user == self._user).first()
        # user.logins.append(Unit(login=login, password=password_for_login))
        self._session.commit()

    def get_password(self, login):
        """Получение пароля"""
        user = self._session.query(User).filter(User.user == self._user).first()
        for unit in user.logins:
            if unit.login == login:
                return unit.password
        return None

    def delete_unit(self, login):
        """Удаление unit"""
        self._session.query(Unit) \
            .filter(Unit.login == login).delete()
        self._session.commit()
        # user = self._session.query(User).filter(User.user == self._user).first()
        # for unit in user.logins:
        #     if unit.login == login:
        #         user.logins.remove(unit)
        #         self._session.commit()
        #         return


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

    def __init__(self, file_db=FILE_USERS_DB, user=None, password=None):
        """Инициализация класса при вызове с поднятием текущей сессии"""
        self._user = user
        self._file_user_db = file_db

        # Инициализация User
        engine = create_engine(f'sqlite:///{self.file_user_db}', echo=False)

        # Создание файла БД, если его нет, обновление таблиц, при изменении
        Base.metadata.create_all(engine,
                                 tables=[Base.metadata.tables["users"]])

        self._session_for_user = sessionmaker(bind=engine)()

        self.user_obj = UserManager(self.session_for_user, self.user)

        # Инициализация Items
        engine = create_engine(
            f'sqlite:///{DIR_UNITS_DBS + os.sep + user + ".sqlite"}',
            echo=False)

        # Создание файла БД, если его нет, обновление таблиц, при изменении
        Base.metadata.create_all(engine,
                                 tables=[Base.metadata.tables["units"]])

        self._session_for_unit = sessionmaker(bind=engine)()

        self.unit_obj = UnitManager(self.session_for_unit, self.user)
