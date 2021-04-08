from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from show_app.models_manager import ShowManager, EpisodeManager, RusFeldsManager
import random


def gen_code():
    list_code = list()
    for i in range(4):
        list_code.append(str(random.randint(0, 9)))
    return ''.join(list_code)


class Telegram(models.Model):
    user_name = models.CharField(max_length=200, blank=True)
    chat_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(default=gen_code, max_length=4)


class SiteUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    shows = models.ManyToManyField('Show', blank=True)
    send = models.BooleanField(default=False)
    sender = models.ForeignKey('Sender', on_delete=models.SET_NULL, null=True, blank=True)
    time_1 = models.BooleanField(default=False)
    time_2 = models.BooleanField(default=False)
    telegram = models.OneToOneField(Telegram, on_delete=models.CASCADE, blank=True, null=True)
    trash = models.ManyToManyField('Show', blank=True, related_name='trash')


class Sender(models.Model):
    name = models.CharField(max_length=250, unique=True)


class Show(models.Model):
    KINDS = (
        ('unknown', ''),
        ('Scripted', 'Сериал'),
        ('Animation', 'Анимация'),
    )
    STATUS = (
        ('unknown', ''),
        ('Running', 'Продолжается'),
        ('Ended', 'Закончился'),
        ('To Be Determined', 'Приостановленный'),
        ('In Development', 'В разработке')

    )

    id_tvmaze = models.IntegerField(unique=True)
    id_tvrage = models.IntegerField(blank=True, null=True)
    id_thetvdb = models.IntegerField(blank=True, null=True)
    id_imdb = models.CharField(blank=True, null=True, max_length=150)
    name = models.CharField(verbose_name='Название шоу', max_length=400)
    url_tvmze = models.URLField(blank=True)
    type_show = models.CharField(choices=KINDS, max_length=200, blank=True, default='unknown')
    language = models.CharField(max_length=100, blank=True, null=True)
    genres = models.ManyToManyField('Genres', blank=True)
    status = models.CharField(max_length=200, choices=STATUS, blank=True, null=True)
    premired = models.DateField(blank=True, default='1945-05-09', null=True)
    officialSite = models.URLField(blank=True, null=True, max_length=500)
    raiting = models.IntegerField(blank=True, null=True)
    raiting_average = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    web_channel = models.ForeignKey('WebChannel', on_delete=models.SET_NULL, blank=True, null=True)
    original_image = models.ImageField(upload_to='original_media/', blank=True, null=True)
    updated = models.IntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    actors = models.ManyToManyField('Actors', blank=True)
    image_medium_url = models.URLField(blank=True, null=True)
    image_original_url = models.URLField(blank=True, null=True)
    rus_fields = models.OneToOneField('RusFields', on_delete=models.CASCADE, null=True)
    original_image1 = models.ImageField(blank=True, null=True)
    objects = ShowManager()
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("show", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'TV Shows'
        verbose_name = 'TV Show'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class RusFields(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    objects = RusFeldsManager()


class Genres(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр', db_index=True)
    name_rus = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


DAYS = (
    ('Sunday', 'Воскресенье'),
    ('Monday', 'Понедельник'),
    ('Tuesday', 'Четверг'),
    ('Wednesday', 'Среда'),
    ('Thursday', 'Четверг'),
    ('Friday', 'Пятница'),
    ('Saturday', 'Суббота'),
)


class WebChannel(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Episode(models.Model):
    id_tvmaze = models.IntegerField()
    url_tvmaze = models.URLField(blank=True, null=True, max_length=500)
    name = models.CharField(max_length=1000, blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    airdate = models.DateField(blank=True, null=True)
    airtime = models.TimeField(blank=True, null=True)
    url_image_original = models.URLField(blank=True, null=True, max_length=500)
    summary = models.TextField(blank=True, null=True, max_length=1000)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='Episodes', related_query_name='entry',
                             max_length=500)
    objects = EpisodeManager()
    date_created = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-airdate']
        verbose_name_plural = 'Episodes'
        verbose_name = 'Episode'

    def save(self, *args, **kwargs):

        try:
            super().save(*args, **kwargs)
        except ValidationError:
            self.airtime = None
            try:
                super().save(*args, **kwargs)
            except ValidationError:
                self.airdate = None
                super().save(*args, **kwargs)


class Actors(models.Model):
    id_tvmaze = models.IntegerField(unique=True)
    url_tvmaze = models.URLField(blank=True)
    name = models.CharField(max_length=150, blank=True)
    image_url_medium = models.URLField(blank=True)
    image_url_original = models.URLField(blank=True)
    country = models.CharField(max_length=400, blank=True, default='')
    birthday = models.DateField(blank=True)
    deathday = models.DateField(blank=True)
    gender = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
