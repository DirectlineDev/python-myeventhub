# -*- coding: utf-8 -*-

import json
import math
from socket import timeout
from urllib import parse, request
from urllib.error import URLError, HTTPError

from myeventhub.exceptions import *
from myeventhub import options
from myeventhub.api_models import *


class Client(object):
    """ Клиент MyEventHub.ru API
    """
    partner_id = 0
    partner_key = ''

    def __init__(self, partner_id, partner_key, timeout=0):
        self.partner_id = partner_id
        self.partner_key = partner_key
        self.timeout = timeout or options.DEFAULT_TIMEOUT

    def _call(self, method, **kwargs):
        """ Вызов метода API
        """
        kwargs.update(dict(
            partnerid=self.partner_id,
            partnerkey=self.partner_key,
            method=method,
        ))

        url = options.ENDPOINT_URL + '?' + parse.urlencode(kwargs)
        try:
            raw_json = request.urlopen(url, timeout=self.timeout).read().decode('utf-8')
            res = json.loads(raw_json)
            if 'code' in res:
                if res['code'] == 4:
                    raise InvalidCredentialsException(res['msg'])
        except (HTTPError, URLError, timeout) as e:  # ошибка запроса
            raise APIRequestException(e.__class__.__name__, e)
        except (ValueError, ) as e:  # ошибка в данных
            raise APIDataException(e.__class__.__name__, e)
        return res, raw_json

    def get_count_action(self):
        """ Получение общего количества событий
        """
        res, _ = self._call('getcountaction')
        return int(res)

    def get_action_list(self, page=1):
        """ Получение списка событий
        :param page: (опционально) номер страницы, начинается с 1
        :param filter: todo
        :return:
        """
        kw = {}
        if page:
            kw['inum'] = page
        actions, _ = self._call('getactionlist', **kw)
        result_list = []
        for action in actions:
            result_list.append(ActionInList.object_from_api(action))
        return result_list

    def get_action_by_id(self, action_id):
        """ Получение детального описания события
        """
        parsed_json, raw_json = self._call('getactionbyid', element_id=action_id)
        action = Action.object_from_api(parsed_json, raw_json)
        return action

    def all_actions(self):
        """ Генератор, возвращающий все события
        """
        count = self.get_count_action()
        page = 1
        while True:  # не цикл for, потому как не уверен, что всё норм будет с API
            actions = self.get_action_list(page=page)
            for action in actions:
                yield action
            page += 1
            if len(actions) < options.ACTIONS_ON_PAGE or page > math.ceil(count / options.ACTIONS_ON_PAGE):
                break
