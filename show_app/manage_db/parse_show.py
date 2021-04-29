import datetime
import json
from collections import namedtuple
from time import sleep

import requests

from show_app.manage_db.get_fields import GetShowFields, GetEpisodesFields
from show_app.models import Show
from tv_project import settings
import re
import environ
env = environ.Env()


class BaseRequests:
    def __init__(self):
        self.errors = dict()

    def _get(self, url):
        count = 0
        while count < 100:
            try:
                resp = requests.get(url)
            except Exception as exc:
                print(exc)
                raise Exception
            if resp.status_code == 200:
                return resp
            if resp.status_code == 404:
                return False
            if resp.status_code == 429:
                sleep(0.1)
                count += 1
                continue
        else:
            raise Exception('too many requests')


class RusFieldsParse:
    def __init__(self, type_bd: str, id_bd: int):
        self.key = env('KEY_TOKEN')
        self.url = env('URL_PARSE')
        self.requests = BaseRequests()

    def _get_rus_fields(self, data: dict) -> dict:
        data = data.get('tv_results', None)

        if data:
            name, description = data[0].get('name', None), data[0].get('overview', None)
            return {'name': name, 'description': description}
        else:
            return dict()

    def has_cyrillic(self, text):
        return bool(re.search('[а-яА-Я]', text))

    def check_rus(self, fields: dict) -> dict:
        name = fields.get('name', None)
        if name:
            if self.has_cyrillic(name):
                return fields
            else:
                return dict()
        else:
            return dict()

    def rus_fields(self):
        res = self.requests._get(self.url)
        fields = self._get_rus_fields(res.json())
        if fields:
            fields = self.check_rus(fields)
        return fields


class TvMazeParse(BaseRequests):

    def __init__(self, pk: int):
        """
        Инициализирует urls для парсинга шоу по pk, и создает
        экземпляр обьекта GetShowFields для получения отдельных значений полей
        """
        self.pk = pk
        self._url_show_main = 'http://{}/shows/{}'.format(env('SITE_PARSE'),pk)
        self._get_show_fields = GetShowFields()
        self._get_episodes_fields = GetEpisodesFields()
        self._url_show_episodes_list = 'http://api.tvmaze.com/shows/{}/episodes'.format(pk)
        self.request = requests

    def check_response(self, resp) -> bool:
        if resp is False:
            return True
        else:
            return False

    def check_show(self, show) -> bool:
        if show is None or (show['type'] != 'Scripted' and show['type'] != 'Animation'):
            return True

    def _get_show_main(self) -> dict or bool:
        """
        Использует url_show_main для парсинга шоу возвращяет
        словарь с атрибудами для создания в модели Show
        """

        response = self._get(self._url_show_main)

        if self.check_response(response):
            return False
        show = response.json()
        if self.check_show(show):
            return False

        show_obj = dict(
            updated=self._get_show_fields.get_updated(show),
            id_tvmaze=self._get_show_fields.get_idtvmaze(show),
            id_tvrage=self._get_show_fields.get_idtvrage(show),
            id_thetvdb=self._get_show_fields.get_idthetvdb(show),
            id_imdb=self._get_show_fields.get_idimdb(show),
            name=self._get_show_fields.get_name(show),
            url_tvmze=self._get_show_fields.get_urltvmze(show),
            type_show=self._get_show_fields.get_typeshow(show),
            language=self._get_show_fields.get_language(show),
            status=self._get_show_fields.get_status(show),
            premired=self._get_show_fields.get_premiered(show),
            officialSite=self._get_show_fields.get_officialSite(show),
            raiting=self._get_show_fields.get_raiting(show),
            raiting_average=self._get_show_fields.get_raitingaverage(show),
            weight=self._get_show_fields.get_weight(show),
            web_channel=self._get_show_fields.get_webchannel(show),
            original_image=self._get_show_fields.get_originalimage(show),
            summary=self._get_show_fields.get_summary(show),
            image_medium_url=self._get_show_fields.get_imagemediumurl(show),
            image_original_url=self._get_show_fields.get_imageoriginalurl(show),
            rus_fields=self._get_show_fields.get_rusfields(show),
            genres=self._get_show_fields.get_genres(show),
            actors=self._get_show_fields.get_actors(show),

        )
        return show_obj

    def get_show(self) -> namedtuple:
        """
        Метод пользователя возвращяющий шоу
        """
        show = namedtuple('SHOW', ['show'])
        return show(show=self._get_show_main())

    def get_episodes(self) -> namedtuple:
        """
        Метод пользователя возвращяющий список епизодов шоу
        """
        episodes = namedtuple('Episodes', ['episodes'])

        return episodes(episodes=self._get_eposodes_main())

    def get_show_episodes(self) -> dict:
        """
        Метод пользователя возвращяющий и список епизодов и шоу
        """
        return {'show': self._get_show_main, 'episodes': self._get_eposodes_main()}

    def _get_eposodes_main(self) -> list or bool:
        # парсит сайт и возвращяет список епизодов

        response = self._get(self._url_show_episodes_list)
        if self.check_response(response):
            return False
        episodes = response.json()
        return list(map(self._parse_episode, episodes))

    def _parse_episode(self, episode: dict) -> dict:
        # парсит данные из полученного словаря
        dict_data = {}
        dict_data.update(
            id_tvmaze=self._get_episodes_fields.get_idtvmaze(episode),
            url_tvmaze=self._get_episodes_fields.get_urltvmaze(episode),
            name=self._get_episodes_fields.get_name(episode),
            season=self._get_episodes_fields.get_season(episode),
            number=self._get_episodes_fields.get_number(episode),
            airdate=self._get_episodes_fields.get_airdate(episode),
            airtime=self._get_episodes_fields.get_airtime(episode),
            url_image_original=self._get_episodes_fields.get_url_image_original(episode),
            summary=self._get_episodes_fields.get_summary(episode),
            show=self.pk,

        )
        return dict_data
