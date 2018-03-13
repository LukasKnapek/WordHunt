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

# Create your views here.

def main(request):
	response = render(request, 'WordHuntApp/main.html')
	return response
	
def about(request):
	response = render(request, 'WordHuntApp/about.html')
	return response
	
def past(request):
	response = render(request, 'WordHuntApp/pastWords.html')
	return response
	
def leaderboard(request):
	response = render(request, 'WordHuntApp/leaderboards.html')
	return response
	
def search(request):
	response = render(request, 'WordHuntApp/search.html')
	return response
	
def register(request):
	response = render(request, 'WordHuntApp/register.html')
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
	
