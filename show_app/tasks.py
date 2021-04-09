from tv_project import celery_app
from django.core.mail import send_mail
from celery import shared_task
from django.contrib.auth.models import User
from show_app.alerts.messages_1 import instructions_email as email_inst, instructions_telegram as telegram_inst


@celery_app.task
def send_instructions(username: str, code: str, email: str, sender: str):
    

    subject = 'Инструкция'
    message = email_inst
    if sender == 'telegram':
        message = telegram_inst.format(name= username, code=code)
    from_ = 'medik@sledoktv.ru'
    list_email = list()
    list_email.append(email)
    return send_mail(subject, message, from_, list_email)

@celery_app.task
def send_messages():
    from show_app.alerts.send_messages_1 import SendAlerts
    sender = SendAlerts()
    sender.for_day
    sender.send_alerts()
    sender1= SendAlerts()
    sender1.for_week
    sender1.send_alerts()



@celery_app.task
def update_db():
    from show_app.manage_db.get_updated import get_show_updates, get_site_updates
    from show_app.manage_db import CreateShow, UpdateShow
    db_for_updated = get_show_updates()
    update_obj = UpdateShow()
    db_for_created = get_site_updates()
    send_mail('Updated id_tvmaze', str(db_for_updated), 'medik@sledoktv.ru', ['medikos007@yandex.ru'])
    send_mail('Created id_tvmaze', str(db_for_created), 'medik@sledoktv.ru', ['medikos007@yandex.ru'])
    try:
        for i in db_for_updated:
            update_obj.update_show(i)
        create_obj = CreateShow()
        from django.db.utils import IntegrityError
        for i in db_for_created:
            try:
                create_obj.create_show(i)
            except IntegrityError:
                continue
    except Exception as exc:
        send_mail('Error', f'need check db\nException: {exc.args}', 'medik@sledoktv.ru', ['medikos007@yandex.ru'])
        raise exc
    return None
