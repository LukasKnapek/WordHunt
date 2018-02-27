# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=64, unique=True, primary_key=True)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    total_points = models.IntegerField()
    rank = models.IntegerField()
    currently_participates = models.BooleanField()

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username


class Image(models.Model):
    username = models.ForeignKey(User)
    avg_rating = models.FloatField()
    uploaded_image = models.ImageField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class Comment(models.Model):
    username = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280)

    class Meta:
        unique_together = ('username', 'image', 'creation_date')

class Rating(models.Model):
    username = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('username', 'image')

class Word(models.Model):
    image = models.ForeignKey(Image)
    text = models.CharField(max_length=50, unique=True, primary_key=True)

class Competition(models.Model):
    word = models.OneToOneField(Word)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    points_to_award = models.IntegerField()

