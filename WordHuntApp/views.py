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
        time_left = Competition.objects.get(word = get_current_word()).end_date.replace(tzinfo=pytz.UTC) - datetime.datetime.now().replace(tzinfo=pytz.UTC)
        context_dict["hours_left"] = time_left.seconds//3600
        context_dict["minutes_left"] = (time_left.seconds//60)%60

        image_rows = []
        for i in range(0, len(images), 3):
            image_rows.append(images[i:i+3])

        context_dict["image_rows"] = image_rows
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
    pictures_number = []
    for competitions in competition:
        pictures_number.append(len(Image.objects.filter(related_word=competitions.word)))
    var = list(zip(competition,pictures_number))
    context_dict = {'competitions': var}
    print(var)
    response = render(request, 'WordHuntApp/pastWords.html',context_dict)
    return response
    
def leaderboard(request):
    users = UserProfile.objects.all()
    numbers = get_number_of_user_images(users)
    results = list(zip(users, numbers))
    for result in results:
         print(result)
    response = render(request, 'WordHuntApp/leaderboards.html',{'users': users, 'results': results})
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



def word(request, username, word):
    context_dict = {}

    profile_user = User.objects.get(username=username)
    user = request.user
    image = Image.objects.get(user=profile_user, related_word=word)
    comments = Comment.objects.filter(image=image)

    context_dict["profile_user"] = profile_user
    context_dict["image"] = image
    context_dict["comments"] = comments
    context_dict["word"] = word
    context_dict["avg_rating"] = "{0:.2f}".format(image.avg_rating)
    context_dict["rating_readonly"] = "false"

    if user.is_authenticated():
        if (image.user == user):
            context_dict["rating_readonly"] = "true"

        if request.is_ajax():
            image_id = request.GET.get("image_id")
            image = Image.objects.get(id=image_id)
            rating_value = request.GET.get("rating")

            # If the user has already rated the image, just change the value
            try:
                r = Rating.objects.get(image=image, user=user)
                r.rating = rating_value
                r.save()
            except Rating.DoesNotExist:
                r = Rating.objects.create(image=image, user=user, rating=rating_value)
            calculate_new_average_rating(image)

            return HttpResponse(json.dumps({"avg_rating": image.avg_rating}), content_type="application/json")

        try:
            user_rating = Rating.objects.get(image=image, user=user)
            context_dict["user_rating"] = user_rating.rating
            print(user_rating.rating)
        except Rating.DoesNotExist:
            user_rating = None

        if request.method == "POST":
            comment_text = request.POST.get("comment")

            c = Comment.objects.create(user=user,
                                       image=image,
                                       creation_date=datetime.datetime.now(pytz.utc),
                                       text = comment_text)

    else:
        context_dict["rating_readonly"] = "true"


    if image.latitude and image.longitude:
        context_dict["latitude"] = image.latitude
        context_dict["longitude"] = image.longitude
    
    return render(request, 'WordHuntApp/viewImage.html', context_dict)

    
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
    context_dict = {}
    context_dict["currently_participates"] = False

    get_last_rank()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
        
    if(user != request.user):
        auth = False
    else:
        auth = True
		
    context_dict["auth"] = auth
    existing_image = None
    try:
        existing_image = Image.objects.get(user=user)
        context_dict["existing_image"] = existing_image
        context_dict["currently_participates"] = True
    except Image.DoesNotExist:
        pass

    userprofile = UserProfile.objects.get(user=user)
    word = get_current_word()
    form = ImageUploadForm()

    context_dict["userprofile"] = userprofile
    context_dict["selecteduser"] = user
    context_dict["word"] = word.text

    if request.method == 'POST':
        if request.POST.get("delete") == "true":
            existing_image.delete()
            userprofile.currently_participates = False
            userprofile.save()
        else:
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                if is_competition_active():
                    image = form.save(commit=False)
                    image.user = request.user
                    image.related_word = get_current_word()
                    image.avg_rating = 0.0

                    # If the user has a previously uploaded image, get rid of it first
                    if existing_image:
                        existing_image.delete()

                    userprofile.currently_participates = True
                    userprofile.save()
                    image.save()

                    if "checkbox_scrap_gps" in request.POST:
                        latitude, longitude = get_image_coordinates(image.uploaded_image.path)
                        if latitude and longitude:
                            image.latitude = latitude
                            image.longitude = longitude
                            image.save()

                    context_dict["existing_image"] = image
            else:
                context_dict["status"] = "Invalid submission"

    context_dict["form"] = form

    return render(request, 'WordHuntApp/userCurrent.html', context_dict)


def settings(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('main')
    if(user != request.user):
        auth = False
    else:
        auth = True
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
        {'userprofile': userprofile, 'selecteduser': user, 'form': form, 'auth':auth})
    
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
