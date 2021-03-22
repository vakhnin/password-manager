from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Определение таблицы users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, unique=True,
                  sqlite_on_conflict_unique='FAIL')
    password = Column(String, nullable=False)
    units = relationship("Unit",
                         back_populates="user",
                         cascade="all, delete-orphan")

    def __init__(self, user, password):
        self.user = user
        self.password = password


class Unit(Base):
    """Определение таблицы units"""
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"))
    login = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    url = Column(String)
    description = Column(String)
    password = Column(String, nullable=False)
    login_name = UniqueConstraint(user_id, login, name)
    user = relationship("User", back_populates="units")

    def __init__(self, login, password, url=None, name='default', category='default'):
        self.login = login
        self.password = password
        self.url = url
        self.name = name
        self.category = category
