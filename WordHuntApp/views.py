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

def main(request):
    response = render(request, 'WordHuntApp/main.html')
    return response
    
def about(request):
    response = render(request, 'WordHuntApp/about.html')
    return response
    
def past(request):
    #words = Competition.objects.get()
    response = render(request, 'WordHuntApp/pastWords.html')
    return response
    
def leaderboard(request):
    response = render(request, 'WordHuntApp/leaderboards.html')
    return response
    
def search(request):
    if request.method == 'POST':
        input = request.POST.get()
    response = render(request, 'WordHuntApp/search.html')
    return response
    
def register(request):
    registered = False
    response = render(request, 'WordHuntApp/register.html')
    return response
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user: 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main'))
            else:
                return HttpResponse("Invalid account")
        else:
             return HttpResponse("Wrong username or password")
    else:
        return null
        
def image(request):
    response = render(request, 'WordHuntApp/viewImage.html')
    return response
    
@login_required
def stats(request):
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