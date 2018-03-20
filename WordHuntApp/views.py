# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from WordHuntApp.models import UserProfile
from WordHuntApp.models import Word
from WordHuntApp.models import Competition
from WordHuntApp.models import Image
from WordHuntApp.models import Comment
from WordHuntApp.models import Rating
from WordHuntApp.forms import ImageUploadForm
from WordHuntApp.utils import *

def user_list_def():
    user_list = UserProfile.objects.order_by('rank')[:5]
    dict = {'users':user_list}
    return dict

def main(request):
    context_dict = user_list_def()
    if is_competition_active():
        context_dict["word"] = get_current_word().text
    else:
        context_dict["word"] = "No competition at the moment!"
    response = render(request, 'WordHuntApp/main.html', context_dict)
    return response
    
def about(request):
    context_dict = user_list_def()
    response = render(request, 'WordHuntApp/about.html',context_dict)
    return response
    
def past(request):
    context_dict = user_list_def()
    competition = Competition.objects.all()
    context_dict['competitions'] = competition
    response = render(request, 'WordHuntApp/pastWords.html',context_dict)
    return response
    
def leaderboard(request):
    context_dict = user_list_def()
    response = render(request, 'WordHuntApp/leaderboards.html',context_dict)
    return response
    
def search(request):
    if request.method == 'POST':
        input = request.POST.get()
    response = render(request, 'WordHuntApp/search.html')
    return response
    
def register(request):
    context_dict = user_list_def()
    registered = False
    response = render(request, 'WordHuntApp/register.html',context_dict)
    return response
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'WordHuntApp/main.html', {})


def word(request):
    response = render(request, 'WordHuntApp/viewImage.html')
    return response
    
@login_required
def stats(request,user):
    try:
        u = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        u = None
    response = render(request, 'WordHuntApp/userMain.html')
    return response
    
def current(request):
    response = render(request, 'WordHuntApp/userCurrent.html')
    return response

def settings(request):
    response = render(request, 'WordHuntApp/userSettings.html')
    return response
    
def uploads(request):
    response = render(request, 'WordHuntApp/userAllPictures.html')
    return response
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
