# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(null=True)
    competition_rank = models.IntegerField(default=None, null=True)
    competitions_won = models.IntegerField(default=0, null=True)
    currently_participates = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username


class Word(models.Model):
    text = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text


class Competition(models.Model):
    word = models.OneToOneField(Word)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    points_to_award = models.IntegerField()
    evaluated = models.BooleanField(default=False)

    def __str__(self):
        return "'%s', %s,  %s - %s, awards %d points" % (self.word, self.start_date.strftime("%d/%m/%Y"),
                                                        self.start_date.strftime("%H:%M"),
                                                        self.end_date.strftime("%H:%M"),
                                                        self.points_to_award)

    def __unicode__(self):
        return "'%s', %s,  %s - %s, awards %d points" % (self.word, self.start_date.strftime("%d/%m/%Y"),
                                                        self.start_date.strftime("%H:%M"),
                                                        self.end_date.strftime("%H:%M"),
                                                        self.points_to_award)


class Image(models.Model):
    related_word = models.ForeignKey(Word)
    user = models.ForeignKey(User)
    avg_rating = models.FloatField()
    uploaded_image = models.ImageField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return "Image %s" % self.id

    def __unicode__(self):
        return "Image %s" % self.id


class Comment(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    creation_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280)

    def __str__(self):
        return "Comment %d left by %s for %s" % (self.id, self.user, self.image)

    def __unicode__(self):
        return "Comment %d left by %s for %s" % (self.id, self.user, self.image)


class Rating(models.Model):
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image)
    rating = models.FloatField()

    def __str__(self):
        return "%.1f/5 - left by %s for %s" % (self.rating, self.user, self.image)






