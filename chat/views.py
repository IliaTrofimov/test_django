import simplejson
from django.conf.urls import url
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message, BannedUser
from .forms import MessageForm, UsernameForm


def index(request):
    banned = False
    failed = False
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                BannedUser.objects.get(ban_creator=user, ban_target=request.user)
                banned = True
            except User.DoesNotExist:
                failed = True
            except BannedUser.DoesNotExist:
                return redirect('chat:dialog', companion_id=user.id)
        else:
            failed = True
    return render(request, 'chat/index.html', {'failed': failed, 'banned': banned, 'form': UsernameForm()})


@login_required
def dialog(request, companion_id):
    companion = get_object_or_404(User, pk=companion_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message(text=form.cleaned_data['text'], from_user=request.user, to_user=companion).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            messages = Message.objects.filter(Q(from_user=request.user, to_user=companion) | Q(from_user=companion, to_user=request.user)).order_by('date')
        except Message.DoesNotExist:
            messages = None

        try:
            BannedUser.objects.get(ban_creator=request.user, ban_target=companion)
            banned = True
            print('banned')
        except BannedUser.DoesNotExist:
            print('not banned')
            banned = False

        return render(request, 'chat/dialog_page.html', {
            'messages': messages,
            'companion': companion,
            'form': MessageForm(),
            'banned': banned
        })


@login_required
def ban(request, creator_id, target_id):
    if request.user.id == creator_id:
        try:
            BannedUser(ban_creator_id=creator_id, ban_target_id=target_id).save()
        except:
            pass
    return redirect('chat:index')


@login_required
def unban(request, creator_id, target_id):
    if request.user.id == creator_id:
        try:
            BannedUser.objects.get(ban_creator_id=creator_id, ban_target_id=target_id).delete()
        except:
            pass
    return redirect('chat:index')


def reload_messages(request, companion_id):
    try:
        message = Message.objects.filter(Q(from_user=request.user, to_user_id=companion_id) |
                                          Q(from_user_id=companion_id, to_user=request.user)).order_by('date')[0]
    except Message.DoesNotExist:
        messages = None
    response = {
        'message': message
    }
    return JsonResponse(response)


def reload_messages(request, companion_id):
    try:
        message = Message.objects.filter(Q(from_user=request.user, to_user_id=companion_id) |
                                     Q(from_user_id=companion_id, to_user=request.user)).order_by('date')[0]
    except Message.DoesNotExist:
        message = None

    return HttpResponse(simplejson.dumps(message), mimetype='application/json')