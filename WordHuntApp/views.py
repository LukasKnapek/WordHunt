# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from WordHuntApp.models import UserProfile
from WordHuntApp.models import Word
from WordHuntApp.models import Competition
from WordHuntApp.models import Image
from WordHuntApp.models import Comment
from WordHuntApp.models import Rating
from WordHuntApp.forms import ImageUploadForm, UserProfileForm
from WordHuntApp.utils import *

def user_list_def():
    user_list = UserProfile.objects.order_by('rank')[:5]
    dict = {'users':user_list}
    return dict

def main(request):
    context_dict = user_list_def()
    if is_competition_active():
        context_dict["word"] = get_current_word().text
        images = Image.objects.filter(related_word=get_current_word().text)
        context_dict["images"] = images
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
def stats(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
    
    try:
        images_number = len(Image.objects.filter(user=user))
    except Image.DoesNotExist:
        images_number = 0

    try:
        rated = len(Rating.objects.filter(user=user))
    except Rating.DoesNotExist:
        rated = 0

    try:
        commented = len(Comment.objects.filter(user=user))
    except Comment.DoesNotExist:
        commented = 0

    total_rating = 0
    best_rating = 0
    best_picture = None
    for image in Image.objects.filter(user=user):
        total_rating = total_rating + image.avg_rating
        if image.avg_rating > best_rating:
            best_rating = image.avg_rating
            best_picture = image.uploaded_image
        
    try:
        average = total_rating/images_number
    except ZeroDivisionError:
        average = 0

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('stats', user.username)
        else:
            print(form.errors)

    return render(request, 'WordHuntApp/userMain.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form,
         'images_number': images_number, 'rated': rated, 'commented': commented,
         'average': average, 'best_rating': best_rating, 'best_picture': best_picture})
    
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
