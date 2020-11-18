import os.path

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
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
    password = Column(String)

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def __repr__(self):
        return f'<User({self.user}, {self.password})>'


class SQLAlchemyManager:
    """Менеджер управления БД, предположительно будет отвечать за установление
    коннектов с базой, CRUD(Create, Read, Update, Delete) по хранящимся юнитам"""
    _file_db = ''
    _user = None
    _session = None

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
        file_db_exists = False
        if os.path.isfile(self.file_db):
            file_db_exists = True

        engine = create_engine(f'sqlite:///{self.file_db}', echo=False)

        if not file_db_exists:
            Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

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
