import os.path
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
