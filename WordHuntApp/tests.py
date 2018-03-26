# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders


# Create your tests here.

class GeneralTesting (TestCase):
    def test_basic_addition(self):

        # Test to establish that tests are working

        self.assertEqual(2 + 2, 4)

    def test_static_files(self):
        
        # If using static media correctly the result is not NONE
        
        result = finders.find('img/logo.jpg')
        self.assertIsNotNone(result)

    def main_competition_entry(self):
        
        # Tests if responds and if navbar displays entry not submitted for non-members
        
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response, "Entry NOT Submitted")

class TestAboutPage(TestCase):
    def test_about_response(self):

        # Tests whether the about page url responds

        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_text_appears(self):

        # Tests if about page contains appropriate text

        response = self.client.get(reverse('about'))
        self.assertIn(b'The goal of this game is to find the word randomly generated', response.content)

    def test_about_using_about_template(self):

        # Test template used to render about page

        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'WordHuntApp/about.html')

    def test_about_using_base_template(self):

        # Test template used to render about page

        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'WordHuntApp/base.html')

class TestPastWordsPage(TestCase):
    def test_past_words(self):

        # Tests whether past page responds
        
        response = self.client.get(reverse('past'))
        self.assertEqual(response.status_code, 200)

    def test_past_words_using_template(self):

        # Tests if about page contains appropriate text

        response = self.client.get(reverse('past'))
        self.assertTemplateUsed(response, 'WordHuntApp/pastWords.html')

class TestLeaderBoardsPage(TestCase):
    def test_leaderboard_response(self):
        
        # Tests if leaderboard contains the user
        
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)

