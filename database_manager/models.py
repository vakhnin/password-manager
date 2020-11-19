from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, PrimaryKeyConstraint,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main import get_hash

FILE_DB = 'db.sqlite'

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, unique=True,
                  sqlite_on_conflict_unique='FAIL')
    password = Column(String, nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def __repr__(self):
        return f'<User({self.user}, {self.password})>'


class Unit(Base):
    __tablename__ = 'units'
    user_id = Column(Integer,
                     ForeignKey('users.id',
                                ondelete="CASCADE"),
                     nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    PrimaryKeyConstraint(user_id, login)

    def __init__(self, user_id, login, password_for_login):
        self.user_id = user_id
        self.login = login
        self.password = password_for_login


class UnitManager:
    _session = None
    _user_id = None

    def __init__(self, session, user_id):
        self._session = session
        self._user_id = user_id

    def add_item(self, login, password_for_login):
        print(11111)
        unit_for_add = Unit(self._user_id, login, password_for_login)
        self._session.add(unit_for_add)
        self._session.commit()


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

    def _get_id_by_user(self, user):
        """Получаем id по имени пользоваетля"""
        result = self.session.query(User).filter(User.user == self.user).first()
        if result:
            return result.id
        return None

    def __init__(self, file_db=FILE_DB, user=None):
        """Инициализация класса при вызове с поднятием текущей сессии"""
        self._user = user
        self._file_db = file_db

        engine = create_engine(f'sqlite:///{self.file_db}', echo=False)

        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

        self.unit_obj = UnitManager(self._session,
                                    self._get_id_by_user(user))

    def check_user(self):
        """
        check user existence in BD
        """
        if len(self.session.query(User).filter(User.user == self.user).all()):
            return True
        return False

    def check_user_password(self, password):
        """
        check user and password in BD
        """
        pass_hash = get_hash((self.user + password).encode("utf-8"))
        if len(self.session.query(User).filter(User.user == self.user)
                       .filter(User.password == pass_hash).all()):
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
        self.session.query(User).filter(User.user == self.user).delete()
        self.session.commit()
