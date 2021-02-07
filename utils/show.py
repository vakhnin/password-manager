from typing import List


class UnitData:
    login: str
    name: str
    category: str
    url: str

    def __init__(self, login='', name='', category='', url=''):
        self.login = login
        self.name = name
        self.category = category
        self.url = url

    def set(self, key, value):
        self.__setattr__(key, value)

    def __str__(self):
        return self.__dict__

    def __eq__(self, other):
        if isinstance(other, UnitData):
            return (self.login == other.login and
                    self.name == other.name and
                    self.category == other.category and
                    self.url == other.url)
        return NotImplemented


class ShowUtils:
    """
    Обработка юнитов
    """
    @staticmethod
    def extend_fields(units_list: List[UnitData]):
        """Подготовка списка юнитов"""
        max_len_fields = UnitData().__dict__
        for key in max_len_fields.keys():
            max_len_fields[key] = len(key)

        for unit in units_list:
            for key, value in unit.__dict__.items():
                if len(value) > max_len_fields[key]:
                    max_len_fields[key] = len(value)

        for i, unit in enumerate(units_list):
            for key, value in unit.__dict__.items():
                units_list[i].set(
                    key, value.ljust(max_len_fields[key] + 1))

        return units_list

    @staticmethod
    def make_str_units(units_list: List[UnitData], flags):
        """Печатем логины с флагами"""
        if len(units_list) < 1:
            return ''

        res_str = ''
        is_first_line = True
        delimiter_str = ''

        title = UnitData()
        for key, value in units_list[0].__dict__.items():
            title.set(key, key.ljust(len(value)))
            delimiter_str += '+-' + '-' * len(value)
        units_list.insert(0, title)
        delimiter_str += '+'

        for unit in units_list:
            str_for_print = ''
            for key, value in unit.__dict__.items():
                if key in flags.keys() and flags[key]:
                    str_for_print += '| ' + value
            res_str += str_for_print + '|\n'
            if is_first_line:
                res_str += delimiter_str + '\n'
                is_first_line = False

        return res_str.strip()
