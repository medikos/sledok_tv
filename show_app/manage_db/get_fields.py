from show_app.models import WebChannel
class GetShowFields:

    @staticmethod
    def get_updated(show):
        resp = show.get('updated', None)
        return resp

    @staticmethod
    def get_idtvmaze(show):
        resp = show.get('id', None)
        return resp

    @staticmethod
    def get_idtvrage(show):

        resp = show.get('externals', None)

        if not resp is None:
            resp = resp.get('tvrage')
        return resp

    @staticmethod
    def get_idthetvdb(show):
        resp = show.get('externals', None)
        if not resp is None:
            resp = resp.get('thetvdb')

        return resp

    @staticmethod
    def get_idimdb(show):
        resp = show.get('externals', None)
        if not resp is None:
            resp = resp.get('imdb')

        return resp

    @staticmethod
    def get_name(show):
        resp = show.get('name', None)

        return resp

    @staticmethod
    def get_urltvmze(show):
        resp = show.get('url', None)

        return resp

    @staticmethod
    def get_typeshow(show):
        resp = show.get('type', None)
        return resp

    @staticmethod
    def get_language(show):
        resp = show.get('language', None)

        return resp

    @staticmethod
    def get_status(show):
        resp = show.get('status', None)
        return resp

    @staticmethod
    def get_premiered(show):
        resp = show.get('premiered', None)
        return resp

    @staticmethod
    def get_officialSite(show):
        resp = show.get('officialSite', None)
        return resp

    @staticmethod
    def get_raiting(show):
        resp = show.get('rating', None)
        if not resp is None:
            resp = resp.get('average', None)
        return resp

    @staticmethod
    def get_raitingaverage(show):
        resp = show.get('rating', None)
        if not resp is None:
            resp = resp.get('average', None)
        return resp

    @staticmethod
    def get_weight(show):
        resp = show.get('weight', None)
        return resp

    @staticmethod
    def get_webchannel(show):
        resp = show.get('network', None)
        if not resp is None:
            resp = resp.get('name', None)

        if resp:
            try:
                web_channel = WebChannel.objects.get(name=resp)
            except WebChannel.DoesNotExist:
                web_channel = WebChannel.objects.create(name=resp)

        else:
            web_channel = None
        return web_channel

    @staticmethod
    def get_originalimage(show):

        return ''

    @staticmethod
    def get_summary(show):
        resp = show.get('summary', None)

        return resp

    @staticmethod
    def get_imagemediumurl(show):
        resp = show.get('image', None)
        if not resp is None:
            resp = resp.get('medium', None)
        return resp

    @staticmethod
    def get_imageoriginalurl(show):
        resp = show.get('image', None)
        if not resp is None:
            resp = resp.get('original', None)
        return resp

    @staticmethod
    def get_rusfields(show):
        return None

    @staticmethod
    def get_genres(show):
        resp = show.get('genres', None)

        return resp

    @staticmethod
    def get_actors(show):
        return []


class GetEpisodesFields:

    @staticmethod
    def get_idtvmaze(episode):
        resp = episode.get('id', None)
        return resp

    @staticmethod
    def get_urltvmaze(episode):
        resp = episode.get('url', None)
        return resp

    @staticmethod
    def get_name(episode):
        resp = episode.get('name', None)
        return resp

    @staticmethod
    def get_season(episode):
        resp = episode.get('season', None)
        return resp

    @staticmethod
    def get_number(episode):
        resp = episode.get('number', None)
        return resp

    @staticmethod
    def get_airdate(episode):
        resp = episode.get('airdate', None)
        return resp

    @staticmethod
    def get_airtime(episode):
        resp = episode.get('airtime', None)
        return resp

    @staticmethod
    def get_url_image_original(episode):
        resp = episode.get('image', None)
        if not resp is None:
            resp = resp.get('original', None)
        return resp

    @staticmethod
    def get_summary(episode):
        resp = episode.get('summary', None)
        return resp
