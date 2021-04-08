from django.http import JsonResponse, HttpResponseNotFound
from django.http import HttpRequest
from show_app.models import Show, SiteUserModel, RusFields
from django.core.exceptions import ObjectDoesNotExist
import re

def has_cyrillic( text):
        return bool(re.search('[а-яА-Я]', text))

def search_view(request, pk=None, show_type=None):
    if not request.is_ajax():
        return HttpResponseNotFound(content='Не сужествующяя страница', status=404)
    data = request.GET
    value = data.get('value', None)
    show_object = RusFields
    if not has_cyrillic(value):
        show_object = Show

    return JsonResponse(show_object.objects.search_form(value), safe=False)


def subscribe_view(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'key': False})
    else:
        show = Show.objects.get(pk=pk)
        try:
            request.user.siteusermodel.shows.add(show)
        except ObjectDoesNotExist:
            user = SiteUserModel.objects.create(user=request.user)
            user.shows.add(show)

        return JsonResponse({'key': True, 'show_rus': show.rus_fields.name, 'show_en': show.name})
