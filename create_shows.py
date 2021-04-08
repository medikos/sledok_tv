import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tv_project.settings'

import django
django.setup()
import logging 
logging.basicConfig(filename='create_shows.log', level=logging.INFO)

from show_app.manage_db import get_updated
from show_app.manage_db import CreateShow
from show_app.models import Show

data_db = get_updated._get_db_data()
import json
with open('show_app/manage_db/json_files_update/updated_2021-03-15.json') as fp:
    data_file = json.load(fp)

data_new = data_file.keys()-data_db.keys()
print(data_new.__len__())
create_obj = CreateShow()
for i in sorted(data_new):
    show = create_obj.create_show(i)
    if show is False:
        logging.info(f'id_tvmaze: {i} not created')
        continue
    logging.info(f'show with pk {show.pk} and id_tvmaze:{show.id_tvmaze} created')




