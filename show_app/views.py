import logging

from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

# from show_app.forms import FormUser

from show_app.models import Show, Episode, Telegram, SiteUserModel,RusFields
from django.core.mail import send_mail
from show_app.forms import RegisterUserForm, LoginForm
from django.contrib.auth.models import User

# from .tasks import send_me_ip_user, update_db

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)
def sitemap(request):
    return render(request, 'show_app/sitemap.xml')


def create_user(user: User, password: str):
    telegram_user = Telegram.objects.create()
    SiteUserModel.objects.create(user=user, telegram=telegram_user)
    user.set_password(password)
    user.save()

    return user


@require_http_methods(['GET', 'POST'])
def form_register_view(request):
    if request.method == 'POST':
        form_user = RegisterUserForm(request.POST)
        if form_user.is_valid():
            user = form_user.save()
            password = form_user.cleaned_data['password_1']
            user = create_user(user, password)

            return redirect('login')
        else:
            context = {'form': form_user}
            return render(request, 'registration/registration.html', context)

    else:
        form_user = RegisterUserForm()
        context = {'form': form_user}
        return render(request, 'registration/registration.html', context)


def telegram_view(request):
    fields_user = request.GET
    user = fields_user['username']
    try:
        user = User.objects.get(username=user)
        if user.siteusermodel.telegram.code == fields_user['password']:
            user.siteusermodel.telegram.user_name = fields_user['telegram_username']
            user.siteusermodel.telegram.chat_id = fields_user['chat_id']
            user.siteusermodel.telegram.save()
        else:
            raise User.DoesNotExist
    except User.DoesNotExist:
        return HttpResponse('NO')

    else:
        return HttpResponse('OK')


# Create your views here.
class MyAppLogoutView(LogoutView):
    next_page = 'index'


class MyAppLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = LoginForm
    


def detail_show(request, pk):
    types = {'Scripted':'сериала', 'Animation':'мультфильма'}
    show = Show.objects.get(pk=pk)
    if show.original_image.name == '':
        return HttpResponseNotFound('<h1>Такой страницы нет ошибка 404</h1>')

    if show.genres.all().filter(pk=14):
        type_ = 'аниме'
    else:
        type_ = types[show.type_show]
    description_words = 'Смотрите дату выхода серий, описание, оценку {} (2021). Более чем 27000 сериалов. Возможность настроить оповещение выхода сериала через почту или телеграмм.'.format(type_)


    return render(request, 'show_app/show.html', {'show': show, 'type':type_, 'description_words':description_words})

def about_view(request):
    description_words = 'СЛЕДОК TV - это сайт созданный для того чтобы вы никогда не пропустили и всегда были в курсе о выходе сезонов и серий ваших любимых сериалов. Более 27000 сериалов. '
    title_words = 'О Сайте и Инструкция | СЛЕДОК TV (2021)'
    return render(request, 'show_app/about.html', {'title_words': title_words, 'description_words':description_words} )


def index(request):
    # usr = request.META['HTTP_X_REAL_IP']
    base = False
    episodes = cache.get('episodes')

    if not episodes or cache.get('rus_objects') is None:
        cache.set('episodes', Episode.objects.filter_episodes(), timeout=20000)
        episodes = cache.get('episodes')
        cache.set('rus_objects', RusFields.objects.search_rus_names())

    if request.path == '/anime/':
        context = Show.objects.shows_for_display(type_show='anime')
        
        title_words = 'Дата выхода новых серий аниме (2021) | Следок TV'
        description_words = 'Дата выхода новых сезонов и серий аниме. Более 10000 аниме. Напоминание о выходе новых серий и сезонов аниме через почту и телеграм.'


    elif request.path == '/shows/':
        context = Show.objects.shows_for_display(type_show='shows')
        
        title_words = 'Дата выхода сериалов (2021) | Следок TV'
        description_words = 'Дата выхода новых сериалов. График выхода серий. Более 15000 сериалов.Настройте оповещение дата выхода сериалов, через почту или телеграмм.'
                                                                                                

    elif request.path == '/cartoons/':
        context = Show.objects.shows_for_display(type_show='cartoons')

        
        title_words = 'Дата выхода мультсериалов(2021) | Следок TV'
        description_words = 'График выхода новых сезонов и серий мультисериелов. Более 10000 мультисериалов. Настроить оповещение через почту или телеграмм, чтобы не пропустить свои любимые мультисериалы. '


    else:
        logging.info('hello')
        context = Show.objects.shows_for_display()
        base = True
        title_words = 'Дата выхода сериалы, аниме (2021) | СЛЕДОК TV'
        description_words = 'Дата выхода сериалы, аниме (2021). Более 15000 сериалов,12000 аниме. Возможность настроить оповещение о дате выхода сериала , аниме, через почту или телеграмм.'

    logging.info(request.user.pk)
    paginator = Paginator(context, 18)
    page = paginator.get_page(request.GET.get('page', None))

    return render(request, 'show_app/main.html', {'shows': context, 'page': page, 'episodes': episodes,
     'base': base, 'title_words':title_words, 'description_words':description_words})
