import datetime
import os
import json
from tv_project.settings import BASE_DIR
import datetime


path = os.path.join(BASE_DIR, 'show_app/manage_db/json_files_update/')


def _get_db_data() -> dict:
    from show_app.models import Show
    return {str(i['id_tvmaze']): i['updated'] for i in Show.objects.all().values('id_tvmaze', 'updated')}


def _get_site_data(file_=False):
    date = datetime.datetime.now().date()
    if file_:
        with open(f'{path}{file_}') as fp:
            return json.load(fp)
    url = 'https://api.tvmaze.com/updates/shows'
    try:
        with open(f'{path}updated_{date}.json', 'r') as fp:
            data_site = json.load(fp)
    except FileNotFoundError:
        import requests
        res = requests.get(url)
        data_site = res.json()
        with open(f'{path}updated_{date}.json', 'w') as fp:
            json.dump(data_site, fp, indent=2)
    return data_site


def get_show_updates():
    """ Проверяет обновление шоу которые уже есть в базе"""
    data_site = _get_site_data()
    data_db = _get_db_data()
    data_for_update = dict(data_db.items() - (data_site.items() & data_db.items()))
    return list(map(int, data_for_update.keys()))


def get_site_updates():
    """проверяет сайт на наличие новых шоу"""
    files = os.listdir(path)
    files.sort()

    new_file = files[-1]
    old_file = files[-2]

    old_data, new_data = _get_site_data(file_=old_file), _get_site_data(file_=new_file)
    data = new_data.keys() - old_data.keys()
    return list(map(int, data))
