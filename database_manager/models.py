from sqlalchemy import (Column, ForeignKey, Integer,
                        String, create_engine, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from encryption_manager.models import get_hash, get_secret_obj
from settings import DIR_UNITS_DBS, FILE_USERS_DB

Base = declarative_base()


class User(Base):
    """Определение таблицы users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, unique=True,
                  sqlite_on_conflict_unique='FAIL')
    password = Column(String, nullable=False)

    def __init__(self, user, password):
        self.user = user
        self.password = password


class Unit(Base):
    """Определение таблицы units"""
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    url = Column(String)
    alias = Column(String)
    category_id = Column(ForeignKey('categories.id', ondelete="CASCADE"))
    password = Column(String, nullable=False)
    login_alias = UniqueConstraint(login, alias)
    category = relationship("Category", back_populates="units")

    def __init__(self, login, password, url=None, alias=None):
        self.login = login
        self.password = password
        self.url = url
        self.alias = alias


class Category(Base):
    """Определение таблицы units"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String, unique=True, nullable=True)
    units = relationship("Unit",
                         back_populates="category",
                         cascade="all, delete-orphan")

    def __init__(self, category):
        self.category = category


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

    def update_user(self, password, newuser, newpassword=None):
        """
        update username (and password) in BD
        """
        if newpassword is not None:
            password = newpassword
        pass_hash = get_hash((newuser + password).encode("utf-8"))
        self._session.query(User) \
            .filter(User.user == self._user).update({"user": newuser, "password": pass_hash})
        self._session.commit()

    def del_user(self):
        """
        delete user from BD
        """
        self._session.query(User) \
            .filter(User.user == self._user).delete()
        if (DIR_UNITS_DBS / (self._user + ".sqlite")).exists():
            (DIR_UNITS_DBS / (self._user + ".sqlite")).unlink()
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

    def __init__(self, session):
        self._session = session

    def get_logins(self, category):
        """Выдача units"""

        def make_logins_obj(units_list):
            """Выдача логинов, из списка"""
            units_obj = {
                "logins": [],
                "category": [],
                "url": [],
                "alias": []
            }

            if units_list:
                for unit_ in units_list:
                    units_obj['logins'].append(unit_.login)
                    units_obj['category']\
                        .append(unit_.category.category if unit_.category.category else 'default')
                    units_obj['url']\
                        .append(unit_.url if unit_.url else '')
                    units_obj['alias']\
                        .append(unit_.alias if unit_.alias else '')
            return units_obj

        if category == 'default':
            category = self._session.query(Category)\
                .filter(Category.category == None).first()
            return make_logins_obj(category.units)
        elif category:
            category = self._session.query(Category)\
                .filter(Category.category == category).first()
            return make_logins_obj(category.units)
        else:
            units = self._session.query(Unit).all()
            return make_logins_obj(units)

    def check_login(self, login, alias):
        """Проверка существования логина"""
        return self._session.query(Unit)\
            .filter((Unit.login == login) & (Unit.alias == alias)).all()

    def get_category(self, category):
        """Выдаем категорию, если есть, иначе создаем"""
        category_obj = self._session.query(Category)\
            .filter(Category.category == category).first()
        if category_obj:
            return category_obj
        else:
            return Category(category=category)

    def add_unit(self, user, password, login, password_for_login, category=None, url=None, alias=None):
        """Добавление unit"""
        secret_obj = get_secret_obj(user, password)
        unit_for_add = Unit(login, secret_obj.encrypt(password_for_login), url, alias)
        self._session.add(unit_for_add)
        unit_for_add.category = self.get_category(category)
        self._session.commit()

    def get_password(self, user, password, login):
        """Получение пароля"""
        secret_obj = get_secret_obj(user, password)
        unit_obj = self._session.query(Unit).filter(Unit.login == login).first()
        return secret_obj.decrypt(unit_obj.password)

    def update_unit(self, user, password, login, new_login=None, password_for_login=None,
                    category=None, url=None, alias=None):
        """Обновление unit"""
        update_dict = {'login': login}
        if new_login:
            update_dict['login'] = new_login
        if password_for_login and password_for_login != 'old-password':
            secret_obj = get_secret_obj(user, password)
            update_dict['password'] = secret_obj.encrypt(password_for_login)
        if url:
            update_dict['url'] = url
        if alias:
            update_dict['alias'] = alias

        self._session.query(Unit).filter(Unit.login == login)\
            .first().category = self.get_category(category)
        self._session.query(Unit).filter(Unit.login == login)\
            .update(update_dict)
        self._session.commit()

    def delete_unit(self, login):
        """Удаление unit"""
        self._session.query(Unit) \
            .filter(Unit.login == login).delete()
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

        # Если пользователя еще не существует, не создаем файл с его БД
        if not self.user_obj.check_user():
            return

        # Инициализация Items
        engine = create_engine(
            f'sqlite:///{DIR_UNITS_DBS / (user + ".sqlite")}',
            echo=False)

        # Создание файла БД, если его нет, обновление таблиц, при изменении
        Base.metadata.create_all(engine,
                                 tables=[
                                     Base.metadata.tables["units"],
                                     Base.metadata.tables["categories"]
                                 ])

        self._session_for_unit = sessionmaker(bind=engine)()

        self.unit_obj = UnitManager(self.session_for_unit)
