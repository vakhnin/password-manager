import os.path

from sqlalchemy import (Column, ForeignKey, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main import get_hash


class SQLAlchemyManager:
    """Менеджер управления БД, предположительно будет отвечать за установление
    коннектов с базой, CRUD(Create, Read, Update, Delete) по хранящимся юнитам"""
    pass


# либо пока пишите функциями всё что относится к работе с БД сюда
# когда будет работать начнём рефакторить
FILE_DB = 'db.sqlite'


def create_session():
    """
    Создание сессии
    """
    file_db_exists = False
    if os.path.isfile(FILE_DB):
        file_db_exists = True

    engine = create_engine(f'sqlite:///{FILE_DB}', echo=False)

    if not file_db_exists:
        Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)()


def check_user(session, user):
    """
    check user existence in BD
    """
    if len(session.query(User).filter(User.user == user).all()):
        return True
    return False


def check_user_password(session, user, password):
    """
    check user and password in BD
    """
    pass_hash = get_hash((user + password).encode("utf-8"))
    if len(session.query(User).filter(User.user == user)
                   .filter(User.password == pass_hash).all()):
        return True
    return False


def add_user(session, user, password):
    """
    add user to BD
    """
    pass_hash = get_hash((user + password).encode("utf-8"))
    user_for_add = User(user, pass_hash)
    session.add(user_for_add)
    session.commit()


def del_user(session, user):
    """
    delete user from BD
    """
    session.query(User).filter(User.user == user).delete()
    session.commit()


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
