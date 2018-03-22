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
import json

def main(request):
    if is_competition_active():
        context_dict = {"word": get_current_word().text}
        images = Image.objects.filter(related_word=get_current_word().text)
        context_dict["images"] = images
        time_left = Competition.objects.get(word = get_current_word()).end_date.replace(tzinfo=pytz.UTC) - datetime.datetime.now().replace(tzinfo=pytz.UTC)
        context_dict["hours_left"] = time_left.seconds//3600
        context_dict["minutes_left"] = (time_left.seconds//60)%60
    else:
        context_dict = {"word": "No competition at the moment!"}
        context_dict["images"] = None
        context_dict["hours_left"] = None
        context_dict["minutes_left"] = None
    response = render(request, 'WordHuntApp/main.html', context_dict)
    return response
    
def about(request):
    response = render(request, 'WordHuntApp/about.html')
    return response
    
def past(request):
    competition = Competition.objects.all()
    context_dict = {'competitions': competition}
    response = render(request, 'WordHuntApp/pastWords.html',context_dict)
    return response
    
def leaderboard(request):
    users = UserProfile.objects.all()
    response = render(request, 'WordHuntApp/leaderboards.html',{'users': users, 'images': images})
    return response
    
def search(request):
    context_dict = {}

    if request.method == 'POST':
        query = request.POST.get("query")
        users = search_for_users(query)
        n_images = get_number_of_user_images(users)
        results = list(zip(users, n_images))

        for result in results:
            print(result)

        context_dict["query"] = query
        context_dict["results"] = results

        return render(request, 'WordHuntApp/search.html', context_dict)

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
    
def current(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('current', user.username)
        else:
            print(form.errors)

    return render(request, 'WordHuntApp/userCurrent.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form})

def settings(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('settings', user.username)
        else:
            print(form.errors)

    return render(request, 'WordHuntApp/userSettings.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form})
    
def uploads(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('uploads', user.username)
        else:
            print(form.errors)

    return render(request, 'WordHuntApp/userAllPictures.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form})
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
