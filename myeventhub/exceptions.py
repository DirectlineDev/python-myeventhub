# -*- coding: utf-8 -*-


class EventHubException(Exception):
    """ Базовый класс исключений для MyEventHub
    """
    pass


class InvalidCredentialsException(EventHubException):
    """ Неверный ID или ключ партнёра для API-запросов
    """
    pass


class APIRequestException(EventHubException):
    """ Ошибка при запросе (http & url errors, timeout, etc.)
    """
    pass


class APIDataException(EventHubException):
    """ Ошибка данных (parse errors, etc.)
    """
    pass
