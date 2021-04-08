from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from show_app.models import Sender
from show_app.models import Show
from show_app.tasks import send_instructions


def alert_setting(data, pk) -> User:
    user = User.objects.get(pk=pk)
    user.siteusermodel.sender = Sender.objects.get(name=data['send'])
    time_1 = data['time_1']
    time_2 = data['time_2']
    user.siteusermodel.send = True
    if time_1:
        user.siteusermodel.time_1 = True
    if time_2:
        user.siteusermodel.time_2 = True
    user.siteusermodel.save()
    return user


@login_required()
def account_view(request, pk):
    if request.method == 'POST':
        data = request.POST
        user = alert_setting(data, pk)
        sender = user.siteusermodel.sender.name
        code = user.siteusermodel.telegram.code
        username = user.username
        email = user.email
        send_instructions.delay(username=username, code=code, email=email, sender=sender)
        return render(request, 'users/succes_sender.html', context={'sender': sender})

    else:
        user = request.user
        shows_user = user.siteusermodel.shows.all()

        return render(request, 'users/cabinet.html', {'shows_user': shows_user})


@login_required()
def ajax_delete_show(request, pk: int) -> JsonResponse:
    if request.is_ajax():
        data = request.GET
        user = User.objects.get(pk=pk)
        show = data['show_pk']
        show = Show.objects.get(pk=int(show))
        user.siteusermodel.shows.remove(show)
        user.siteusermodel.trash.add(show)
        return JsonResponse({'data': 'ok'})


def trash_view(request, pk: int) -> render:
    user = User.objects.get(pk=pk)
    shows = user.siteusermodel.trash.all()
    return render(request, 'users/trash.html', {'shows': shows})


def trash_clear(request, pk: int) -> render:
    user = User.objects.get(pk=pk)
    user.siteusermodel.trash.clear()
    return redirect('users:account', pk=pk)
