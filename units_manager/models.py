import datetime as dt
import json
from abc import ABC, abstractmethod, abstractproperty

from settings import TIME_SESSION_CLOSE


class UnitsComposition:
    """Класс компоновки юнитов на выдачу
    
    Пока общими словами описываю данные, т.к. сопоставление точек соприкосновения
    мы ещё не делали

    IN: 
        Получает на вход выгруженные данные из БД
    OUT:
        отдаёт на выходе json, собрав его в зависимости от наших потребностей,
        которые возникнут по коду
    """
    pass


class TimeoutController:
    """Класс проверки истечения времени активной сессии
    
    IN:
        Получаем на вход объект БД с атрибутом времени посещения
    OUT:
        Если delta между текущим временем и полученным в атрибуте БД больше
        _default_time_session, то возвращаем False; если меньше, то возвращаем
        True и запрашиваем обновление времени в БД по этому объекту
    """
    _default_time_session = TIME_SESSION_CLOSE

    def check_time_permission(check_datetime):
        """
        проверка дельты между переданным datetime и текущим,
        возвращаем True, если дельта меньше дефолтного времени, отведённого на длительность сессии, иначе False
        """
        return dt.datetime.today() - check_datetime < dt.timedelta(seconds=_default_time_session)
