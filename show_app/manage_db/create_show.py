from django.core.files.base import ContentFile

from show_app.manage_db import TvMazeParse, BaseRequests, RusFieldsParse
from show_app.models import Show, Genres, RusFields


class CreateShow:

    @property
    def rus_field_parse(self):
        return RusFieldsParse

    @property
    def parse_obj(self):
        return TvMazeParse

    @property
    def request_obj(self):
        return BaseRequests()

    def create_episodes(self, show: Show, episodes: list):
        if not episodes:
            return None
        for episode in episodes:
            show.Episodes.create(**episode)

    def add_genres(self, show: Show, genres: list):
        for genre in genres:
            show.genres.add(Genres.objects.get_or_create(name=genre)[0])

    def add_original_image(self, show: Show):
        url = show.image_original_url or show.image_medium_url
        name = f'image_{show.pk}.jpg'
        if url:
            resp = self.request_obj._get(url)
            show.original_image.save(name, ContentFile(resp.content), save=True)
        else:
            return None

    def add_rus_fields(self, show: Show):
        id_imdb = show.id_imdb
        id_tvrage = show.id_tvrage
        id_thetvdb = show.id_thetvdb
        if id_imdb:
            rus_field_parse = self.rus_field_parse(type_bd='imdb_id', id_bd=str(id_imdb))
            data = rus_field_parse.rus_fields()
            if data:
                rus = RusFields.objects.create(**data)
                show.rus_fields = rus
                show.save()

        if id_tvrage and show.rus_fields is None:
            rus_field_parse = self.rus_field_parse(type_bd='tvrage_id', id_bd=id_imdb)
            data = rus_field_parse.rus_fields()
            if data:
                rus = RusFields.objects.create(**data)
                show.rus_fields = rus
                show.save()

        if id_thetvdb and show.rus_fields is None:
            rus_field_parse = self.rus_field_parse(type_bd='thetvdb_id', id_bd=id_imdb)
            data = rus_field_parse.rus_fields()
            if data:
                rus = RusFields.objects.create(**data)
                show.rus_fields = rus
                show.save()

    def adapter_create(self, parce_obj):
        genres = parce_obj.show.pop('genres')
        parce_obj.show.pop('actors')
        return parce_obj.show, genres

    def create_show(self, id_imdb: int):
        parse_obj = self.parse_obj(id_imdb)
        tuple_show = parse_obj.get_show()
        if isinstance(tuple_show.show, bool):
            return False
        show, genres = self.adapter_create(tuple_show)
        episodes = parse_obj.get_episodes()
        show = Show.objects.create(**show)
        self.create_episodes(show, episodes.episodes)
        self.add_genres(show, genres)
        self.add_original_image(show)
        self.add_rus_fields(show)
        return show


class UpdateShow(CreateShow):

    def _update_episodes(self, parser: TvMazeParse, show: Show) -> bool:
        episodes = parser.get_episodes()
        show.Episodes.all().delete()
        self.create_episodes(show, episodes.episodes)
        return True

    def _update_raiting_status(self, parse_obj: TvMazeParse, show: Show):

        show_ = parse_obj
        if show_ is False:
            return True
        raiting = show_.show['raiting'] if show_.show else None
        status = show_.show['status'] if show_.show else None
        show.status = status
        if isinstance(raiting, float) or isinstance(raiting, int):
            show.raiting_average = raiting
            show.save()
            return True

        show.raiting_average = raiting.get('average') if raiting else None
        show.save()
        return True

    def _update_image(self, parse_obj: TvMazeParse, show: Show):
        try:
            show.original_image.url
        except ValueError:
            self.add_original_image(show)
            return True
        else:
            False

    def _update_rus_fields(self, parse_obj: TvMazeParse, show: Show):

        self.add_rus_fields(show)
        return True

    def _update_updated(self, parse_obj: TvMazeParse, show: Show):
        show_ = parse_obj.show
        if show_ is False:
            return True
        show.updated = show_['updated']
        show.save()
        return True

    def parse_obj(self, id_tvmaze):
        return TvMazeParse(id_tvmaze)

    def update_show(self, id_tvmaze):
        show = Show.objects.get(id_tvmaze=id_tvmaze)
        log_info = {'episodes': False, 'image': False, 'rus_fields': False, 'pk': show.pk, 'id_tvmaze': show.id_tvmaze,
                    'raiting_avrerage': False, 'status': False}

        parse_obj = self.parse_obj(id_tvmaze)
        parse_show = parse_obj.get_show()
        log_info['episodes'] = self._update_episodes(parse_obj, show)
        log_info['rating.average'] = self._update_raiting_status(parse_show, show)
        log_info['image'] = self._update_image(parse_obj, show)
        log_info['rus_fields'] = self._update_rus_fields(parse_obj, show)

        self._update_updated(parse_show, show)
        return log_info
