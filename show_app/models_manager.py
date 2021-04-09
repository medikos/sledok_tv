import datetime

from django.db import models
from django.db.models import Q
from django.core.cache import cache


class ShowManager(models.Manager):

    def shows_for_display(self, type_show=None):
        Q1 = Q(raiting_average=None)
        Q2 = Q(rus_fields=None)
        Q3 = Q(premired=None)
        Q4 = Q(image_medium_url=None)
        Q5 = Q(image_original_url=None)

        shows = self.exclude(Q2 | Q3).order_by('-premired').exclude(Q4 & Q5)
        if type_show == 'anime':
            shows = shows.filter(genres=14)
        elif type_show == 'shows':
            shows = shows.filter(type_show='Scripted')

        elif type_show == 'cartoons':
            shows = shows.filter(type_show='Animation').exclude(genres=14)
        rus_objects = cache.get('rus_objects')
        return shows.filter(rus_fields__in=cache.get('rus_objects'))

    def search_form(self, value):
        Q1 = Q(name__icontains=value)

        shows = self.filter(Q1)[:10]
        if not shows:
            return shows
        dict_shows = list()

        for data in shows:
            try:

                dict_shows.append([data.name, data.rus_fields.name, data.premired, data.image_original_url,
                                   data.get_absolute_url()])

            except ValueError:
                continue
        print(dict_shows)
        return dict_shows


class RusFeldsManager(models.Manager):

    def search_form(self, value):
        Q1 = Q(name__icontains=value)

        shows_rus = self.filter(Q1)[:10]
        if not shows_rus:
            return shows_rus
        dict_shows = list()

        for data in shows_rus:
            try:
                data.show
                dict_shows.append([data.name, data.show.name, data.show.premired, data.show.image_original_url,
                                   data.show.get_absolute_url()])
            except:
                continue
        print(dict_shows)
        return dict_shows

    def search_rus_names(self):
        return self.filter(name__regex='[а-яА-Я]')


class EpisodeManager(models.Manager):

    def filter_episodes(self):
        print('Hello')

        return self.filter(airdate__gt=datetime.datetime.now()).order_by('airdate')[:20]
