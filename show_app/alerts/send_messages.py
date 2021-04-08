from show_app.models import Episode
import datetime
from collections import namedtuple
from show_app.alerts.messages import alert_release_date
from tv_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

import requests


def after_day(date, days):
    day = datetime.timedelta(days=days)
    return date + day


def get_episodes(date):
    episodes = Episode.objects.filter(airdate=date)
    list_episodes = [episode for episode in episodes
                     if episode.show.siteusermodel_set.all().count() > 0]
    return list_episodes


def get_show_name(show):
    rus = show.rus_fields
    if rus is None:
        return show.name
    else:
        return rus.name


def list_messages(episodes, days):
    days = 'Завтра' if days == 1 else 'Через неделю'
    alert_list = list()
    Alert = namedtuple('Alert', ['message', 'email', 'telegram'])
    for episode in episodes:
        airdate = episode.airdate.strftime('%d-%m-%y')
        for site_users in episode.show.siteusermodel_set.all():
            username = site_users.user.username
            show_name = get_show_name(episode.show)
            email = site_users.user.email
            telegram = None
            if site_users.sender.name == 'telegram':
                telegram = site_users.telegram.chat_id
                email = None
            alert = Alert(
                message=alert_release_date.format(username=username, show_name=show_name, day=days,
                                                  airdate=airdate), email=email, telegram=telegram)
            alert_list.append(alert)

    return alert_list


def create_messages(days) -> namedtuple:
    today = datetime.datetime.now().date()
    date = after_day(today, days=days)
    episodes = get_episodes(date)
    alerts_list = list()
    if episodes:
        alerts_list = list_messages(episodes,days)

    return alerts_list


def send_alerts(days):
    if days != 1 and days != 7:
        raise Exception
    alerts_list = create_messages(days)
    for alert in alerts_list:
        if alert.telegram:
            send_telegram(alert)
        else:
            send_email(alert)
    return


def send_email(alert: namedtuple):
    list_email = list()
    subject = 'Оповещение'
    from_ = EMAIL_HOST_USER
    too = alert.email
    list_email.append(too)
    send_mail(subject, alert.message, from_, list_email)
    return 'Ok'


def send_telegram(alert: namedtuple):
    my_chat_id = 1651198085
    TOKEN = '1685201828:AAEEpPTyerjCY4VUGkPnwycFnE3rNeBtMY4'
    url = 'https://api.telegram.org/bot{}/sendMessage?'
    payload = {'chat_id': alert.telegram, 'text': alert.message}
    res = requests.get(url.format(TOKEN), params=payload)
    return res.status_code
