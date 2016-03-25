# -*- coding: utf-8 -*-

from six import python_2_unicode_compatible

__all__ = ['ModelProperty', 'Model', 'ActionInList', 'Action', ]


@python_2_unicode_compatible
class ModelProperty:
    """ Свойство модели
    """
    # алиас
    name = ''
    # значение
    value = ''
    # человеко-понятное название
    verbose_name = ''

    def __init__(self, name, value='', verbose_name=''):
        self.name = name
        self.value = value
        self.verbose_name = verbose_name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return '"{}": "{}"{}'.format(
            self.name,
            self.value,
            ' [' + self.verbose_name + ']' if self.verbose_name else '',
        )


@python_2_unicode_compatible
class Model:
    """ Модель API
    - поля
    - свойства
    """
    _meta = None
    properties = None

    def __init__(self):
        self._meta = type('lamdbaobject', (object,), {})()
        self._meta.fields = []
        self._meta.properties = []
        self.properties = type('lamdbaobject', (object,), {})()

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, str(self))

    def __str__(self):
        return 'Instance of {}'.format(self.__class__.__name__)

    def set_field(self, name, value):
        """ Установка значения поля
        """
        if name not in self._meta.fields:
            self._meta.fields.append(name)
        setattr(self, name, value)

    def set_property(self, name, value='', verbose_name=''):
        """ Установка значения свойства
        """
        if getattr(self.properties, name, None) is None:
            setattr(self.properties, name, ModelProperty(name=name, value=value, verbose_name=verbose_name))
            self._meta.properties.append(name)
        else:
            self.properties.name.value = value
            self.properties.name.verbose_name = verbose_name

    def is_any_prop_startedwith_has_value(self, startswith):
        """ Возвращает True, если хоть одно свойство модели, начинающееся со startswith, имеет непустое значение
        Может пригодиться для определения типа события: например, если хоть одно свойство,
        начинающееся со PROP_CHILDREN, имеет значение, значит событие можно отнести к детским
        :param startswith: строка, с которой должно начинаться свойство
        :return: bool
        """
        for prop_name in self.properties.__dir__():
            if str(prop_name).startswith(startswith) and getattr(self.properties, prop_name).value:
                return True
        return False

    @classmethod
    def object_from_api(cls, d, raw_json=None):
        """ Создание объекта модели из json-ответа API
        """
        obj = cls()
        obj.raw_json = raw_json
        for k, v in d.items():
            if k == 'PROPERTIES':  # свойства
                for prop_name, prop_value in v.items():
                    if 'NAME' in prop_value and 'VALUE' in prop_value:  # свойство
                        obj.set_property(prop_name, prop_value['VALUE'], prop_value['NAME'])
                    else:
                        raise ValueError('Invalid property markup: expected NAME and VALUE')
            else:  # поле
                obj.set_field(k, v)
        return obj


@python_2_unicode_compatible
class ActionInList(Model):
    """ Объект события в списке
    """
    def __str__(self):
        return '{}: {}'.format(self.ID, self.NAME)


@python_2_unicode_compatible
class Action(Model):
    """ Объект события
    """
    def __str__(self):
        return '{}: {}'.format(self.ID, self.NAME)
