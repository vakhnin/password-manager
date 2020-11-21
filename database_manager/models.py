from sqlalchemy import (Column, ForeignKey, Integer, String, PrimaryKeyConstraint,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from main import get_hash

FILE_DB = 'db.sqlite'

Base = declarative_base()


class User(Base):
    """Определение таблицы users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, unique=True,
                  sqlite_on_conflict_unique='FAIL')
    password = Column(String, nullable=False)
    logins = relationship("Unit",
                          back_populates="user",
                          cascade="all, delete-orphan")

    def __init__(self, user, password):
        self.user = user
        self.password = password


class Unit(Base):
    """Определение таблицы units"""
    __tablename__ = 'units'
    user_id = Column(Integer,
                     ForeignKey('users.id',
                                ondelete="CASCADE"),
                     nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    PrimaryKeyConstraint(user_id, login)
    user = relationship("User", back_populates="logins")


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
        user = self._session.query(User).filter(User.user == self._user).first()
        for unit in user.logins:
            logins_list.append(unit.login)
        return logins_list

    def check_login(self, login):
        """Проверка существования логина"""
        return login in self.all_logins()

    def add_unit(self, login, password_for_login):
        """Добавление unit"""
        user = self._session.query(User).filter(User.user == self._user).first()
        user.logins.append(Unit(login=login, password=password_for_login))
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
        user = self._session.query(User).filter(User.user == self._user).first()
        for unit in user.logins:
            if unit.login == login:
                user.logins.remove(unit)
                self._session.commit()
                return


class SQLAlchemyManager:
    """Менеджер управления БД, предположительно будет отвечать за установление
    коннектов с базой, CRUD(Create, Read, Update, Delete) по хранящимся юнитам"""
    _file_db = ''
    _user = None
    _session = None
    unit_obj = None

    @property
    def user(self):
        return self._user

    @property
    def file_db(self):
        return self._file_db

    @property
    def session(self):
        return self._session

    def __init__(self, file_db=FILE_DB, user=None):
        """Инициализация класса при вызове с поднятием текущей сессии"""
        self._user = user
        self._file_db = file_db

        engine = create_engine(f'sqlite:///{self.file_db}', echo=False)

        # Создание файла БД, если его нет, обновление таблиц, при изменении
        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

        self.unit_obj = UnitManager(self._session, self.user)

    def check_user(self):
        """
        check user existence in BD
        """
        if self.session.query(User).filter(User.user == self.user).first():
            return True
        return False

    def check_user_password(self, password):
        """
        check user and password in BD
        """
        pass_hash = get_hash((self.user + password).encode("utf-8"))
        if self.session.query(User).filter(User.user == self.user)\
                .filter(User.password == pass_hash).first():
            return True
        return False

    def add_user(self, password):
        """
        add user to BD
        """
        pass_hash = get_hash((self.user + password).encode("utf-8"))
        user_for_add = User(self.user, pass_hash)
        self.session.add(user_for_add)
        self.session.commit()

    def del_user(self):
        """
        delete user from BD
        """
        self.session.query(User)\
            .filter(User.user == self.user).first().logins = []
        self.session.query(User) \
            .filter(User.user == self.user).delete()
        self.session.commit()
