from show_app.models import Episode
from show_app.alerts import models
from collections import defaultdict, namedtuple
from django.contrib.auth.models import User
from show_app.alerts.messages_1 import alert_release_date
from tv_project.settings import EMAIL_HOST_USER
import requests
from django.core.mail import send_mail
from show_app.telegram_app import TOKEN


class SendAlerts:
    for_day = models.ForDayWeek('for_day')
    for_week = models.ForDayWeek('for_week')

    def episodes_list(self):
        '''Возвращает все эпизоды которые у который значение даты равно self.date и у которых есть подписчики'''
        episodes = Episode.objects.filter(airdate=self.data)
        list_episodes = [ep for ep in episodes if ep.show.siteusermodel_set.all().count() > 0]
        return list_episodes

    def users_dict(self) -> defaultdict:
        """Возвращяет словарь с пользователями и шоу на которые они подписаны вызывает внутри себя episodes_list"""
        dict_users = defaultdict(list)
        for episode in self.episodes_list():
            show_name = episode.show.name
            for site_user in episode.show.siteusermodel_set.all():
                if self.day_or_week == 'Завтра' and site_user.time_1 is False:
                    continue
                if self.day_or_week == 'Через неделю' and site_user.time_2 is False:
                    continue
                dict_users[site_user.user.username].append(show_name)
        return dict_users

    def create_messages(self) -> list:
        """Создает список сообшений для отправки пользователям"""
        Alert = namedtuple('Alert', ['message', 'email', 'telegram', 'username'])
        list_messages = list()
        dict_users = self.users_dict()
        if not dict_users:
            return False
        for username, list_show in dict_users.items():
            user = User.objects.get(username=username)
            message = self.get_message(list_show, username)
            email = user.email
            telegram = None
            if user.siteusermodel.sender.name == 'telegram':
                telegram = user.siteusermodel.telegram.chat_id
                email = None
            username = user.username
            alert = Alert(message=message, email=email, telegram=telegram, username=username)
            list_messages.append(alert)
        return list_messages

    def send_alerts(self):
        list_messages = self.create_messages()
        for alert in list_messages:
            if alert.telegram:
                res = self.send_telegram(alert)
            else:
                res = self.send_email(alert)
        return res

    def send_telegram(self, alert: namedtuple):
       
        url = 'https://api.telegram.org/bot{}/sendMessage?'
        payload = {'chat_id': alert.telegram, 'text': alert.message}
        print(url, payload)
        res = requests.get(url.format(TOKEN), params=payload)
        return res.status_code

    def send_email(self, alert: namedtuple):
        list_email = list()
        subject = 'Оповещение'
        from_ = EMAIL_HOST_USER
        too = alert.email
        list_email.append(too)
        send_mail(subject, alert.message, from_, list_email)
        return 'Ok'

    def get_message(self, list_show, username):
        one_or_many = 'несколько' if len(list_show) > 1 else "одно"


        message = alert_release_date.format(username=username, day_or_week=self.day_or_week, one_or_many=one_or_many)
        print(message)
        for show_name in list_show:
            message = message + f'Название шоу: {show_name}\n'
        message += f'У всех шоу дата выхода {self.data}'
        return message
