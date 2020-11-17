from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


def create_session():
    engine = create_engine('sqlite:///db.sqlite', echo=False)
    Session = sessionmaker(bind=engine)
    return Session(), engine


engine = create_engine('sqlite:///db.sqlite', echo=False)

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


# Base.metadata.create_all(engine)
