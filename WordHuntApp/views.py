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

#Main Page
def main(request):
	#for an active competition give the images uploaded and the time left
    if is_competition_active():
        context_dict = {"word": get_current_word().text}
        images = Image.objects.filter(related_word=get_current_word().text)
        time_left = Competition.objects.get(word = get_current_word()).end_date.replace(tzinfo=pytz.UTC) - datetime.datetime.now().replace(tzinfo=pytz.UTC)
        context_dict["hours_left"] = time_left.seconds//3600
        context_dict["minutes_left"] = (time_left.seconds//60)%60

		#to make the pictures appear in the correct layout:
        image_rows = []
        for i in range(0, len(images), 3):
            image_rows.append(images[i:i+3])

        context_dict["image_rows"] = image_rows
	#if there is no active competition give an appropriate message and show no photos
    else:
        context_dict = {"word": "No competition at the moment!"}
        context_dict["images"] = None
        context_dict["hours_left"] = None
        context_dict["minutes_left"] = None
    response = render(request, 'WordHuntApp/main.html', context_dict)
    return response

#About Page   
def about(request):
    response = render(request, 'WordHuntApp/about.html')
    return response
    
#Past Word Page
def past(request):
	#show all of the past competitions
    competition = Competition.objects.all()
	#display the number of pictures submitted for each competition
    pictures_number = []
    for competitions in competition:
        pictures_number.append(len(Image.objects.filter(related_word=competitions.word)))
    var = list(zip(competition,pictures_number))
    context_dict = {'competitions': var}
    print(var)
    response = render(request, 'WordHuntApp/pastWords.html',context_dict)
    return response

#All Pictures of a Word Page
def all(request, word):
	#show all the pictures and the users that uploaded them for a certain competition
    context_dict = {}
    word = Word.objects.get(text=word)
    context_dict["word"] = word
    w = Competition.objects.get(word=word)
    context_dict["competition"] = w
    image = Image.objects.filter(related_word=word)
	#to make the pictures appear in the correct layout:
    image_rows = []
    for i in range(0, len(image), 3):
        image_rows.append(image[i:i+3])
    context_dict["image_rows"] = image_rows
    response = render(request, 'WordHuntApp/all.html',context_dict)
    return response
    
#All Time Leaderboards Page
def leaderboard(request):
	#show all of the users ordered by their rank
    users = UserProfile.objects.all()
    users = users.order_by('rank')
    numbers = get_number_of_user_images(users)
    results = list(zip(users, numbers))
    for result in results:
         print(result)
    response = render(request, 'WordHuntApp/leaderboards.html',{'users': users, 'results': results})
    return response

#Current Competition Leaderboards Page
def current_leaderboard(request):
	#show only the users that are taking part in the current competition, in the order of their pictures ratings
	if is_competition_active():
		word = get_current_word().text
		images = Image.objects.filter(related_word = get_current_word().text)
		images = images.order_by('avg_rating')
		images = images[::-1]
	else:
		word = "No competition at the moment!"
		images = None
	response = render(request, 'WordHuntApp/current_leaderboards.html',{'images': images, 'word':word})
	return response

#User Search Page	
def search(request):
    context_dict = {}
	#show all of the users matching the entered string
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

#Word Search Page
def words_search(request):
    context_dict = {}
	#show all of the words matching the entered string
    if request.method == 'POST':
        query = request.POST.get("query")
        words = search_for_words(query)
        enddate = []
        n_images = []
        for word in words:
            enddate.append(Competition.objects.get(word=word).end_date)
            n_images.append(len(Image.objects.filter(related_word=word)))
		
        results = list(zip(words, enddate, n_images))
        for result in results:
            print(result)
		
        context_dict["query"] = query
        context_dict["results"] = results

        return render(request, 'WordHuntApp/words_search.html', context_dict)

    response = render(request, 'WordHuntApp/words_search.html')
    return response
   
#Registration Page
def register(request):
    registered = False
    response = render(request, 'WordHuntApp/register.html')
    return response
    
#Login Page
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


#Individual Pictures Page
def word(request, username, word):
    context_dict = {}
	#for the pictures show the user, comments, rating and location if applicable
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

	#only allow logged in user to rate and comment
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

#Main User Page - Stats   
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
	#get the info about the best picture based on their ratings
	#if the user has no uploaded pictures, present an appropriate message
    for image in Image.objects.filter(user=user):
        total_rating = total_rating + image.avg_rating
        if image.avg_rating >= best_rating:
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
         'average': "{0:.2f}".format(average), 'best_rating': "{0:.2f}".format(best_rating), 'best_picture': best_picture})

#Current Competition Picture - User Page
def current(request, username):
	#show the current picture
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
        context_dict["avg_rating"] = "{0:.2f}".format(existing_image.avg_rating)
    except Image.DoesNotExist:
        pass

    userprofile = UserProfile.objects.get(user=user)
    word = get_current_word()
    form = ImageUploadForm()

    context_dict["userprofile"] = userprofile
    context_dict["selecteduser"] = user
    context_dict["word"] = word.text
	#if the user viewing this tab is also the owner of the account them to 
	#upload for the first time, change or delete the picture
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
                    update_competition_ranks()
            else:
                context_dict["status"] = "Invalid submission"

    context_dict["form"] = form

    return render(request, 'WordHuntApp/userCurrent.html', context_dict)


#User Settings Page
def settings(request, username):
	#TAB ONLY VISIBLE ON USERS OWN ACCOUNT
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
    
#All User Uploads Page
def uploads(request, username):
	#shows all pictures and word associated with them
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

    images = Image.objects.filter(user = userprofile.user)

    return render(request, 'WordHuntApp/userAllPictures.html',
        {'userprofile': userprofile, 'selecteduser': user, 'form': form, 'images': images})
    
#Logout Page
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))
