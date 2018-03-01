import os, sys, datetime
print(os.curdir)

# Add the the main project folder to Python path
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WordHunt.settings')

import django
django.setup()
from WordHuntApp.models import *

def populate():

    # Create the word and the competition related to that word
    w = Word.objects.get_or_create(text="Flag")
    cmp = Competition.objects.get_or_create(word=Word.objects.get(text="Flag"),
                                            start_date=datetime.datetime(2018,2,12,10,0,0),
                                            end_date=datetime.datetime(2018,2,12,20,0,0),
                                            points_to_award=120)

    users = [
        {"username": "XxX_HunTer123",
         "password": "iwannabetheverybest",
         "email": "hunter123@email.com",
         "total_points": 564,
         "rank": 1,
         "currently_participates": True},

        {"username": "1337Commander",
         "password": "1337Lyfe",
         "email": "commando@email.com",
         "total_points": 470,
         "rank": 2,
         "currently_participates": False},

        {"username": "Ch0mp",
         "password": "chompchomp",
         "email": "blabla@10minutemail.com",
         "total_points": 254,
         "rank": 3,
         "currently_participates": True},

        {"username": "BTW",
         "password": "9999999",
         "email": "ferr@oomla.com",
         "total_points": 90,
         "rank": 4,
         "currently_participates": True},

        {"username": "KillerLady",
         "password": "toor",
         "email": "angel@email.com",
         "total_points": 0,
         "rank": 5,
         "currently_participates": True}
    ]

    for u in users:
        add_user(u["username"], u["password"], u["email"],
                 u["total_points"], u["rank"], u["currently_participates"])
        print("Added %s" % u["username"])

    images = [
        {"word" : Word.objects.get(text="Flag"),
         "username": User.objects.get(username="XxX_HunTer123"),
         "avg_rating": 4,
         "uploaded_image": "flag_entry_1.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "username": User.objects.get(username="BTW"),
         "avg_rating": 3.2,
         "uploaded_image": "flag_entry_2.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "username": User.objects.get(username="KillerLady"),
         "avg_rating": 4.5,
         "uploaded_image": "flag_entry_3.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "username": User.objects.get(username="Ch0mp"),
         "avg_rating": 2.4,
         "uploaded_image": "flag_entry_4.jpeg"}
    ]

    for i in images:
        add_image(i["word"], i["username"], i["avg_rating"], i["uploaded_image"])
        print("Added a new image for user %s" % i["username"])

    ratings = [
        {"username" : User.objects.get(username="XxX_HunTer123"),
         "image" : Image.objects.get(username="BTW"),
         "rating" : 5},

        {"username": User.objects.get(username="XxX_HunTer123"),
         "image": Image.objects.get(username="KillerLady"),
         "rating": 2},

        {"username": User.objects.get(username="BTW"),
         "image": Image.objects.get(username="Ch0mp"),
         "rating": 3}
    ]

    comments = [
        {"username": User.objects.get(username="XxX_HunTer123"),
         "image": Image.objects.get(username="BTW"),
         "creation_date": datetime.datetime(2018,2,12,16,30,00),
         "text": "Do you really have to apply filters to EVERY image?"},

        {"username": User.objects.get(username="BTW"),
         "image": Image.objects.get(username="Ch0mp"),
         "creation_date": datetime.datetime(2018,2,12,16,30,00),
         "text": "Very nice!"},

        {"username": User.objects.get(username="XxX_HunTer123"),
         "image": Image.objects.get(username="KillerLady"),
         "creation_date": datetime.datetime(2018,2,12,16,30,00),
         "text": "This feels like such a cliche, you could have put more creativity into it."},
    ]

    for r in ratings:
        add_rating(r["username"], r["image"], r["rating"])
        print("Added a new rating for image '%s' from user '%s'" % (r["image"], r["username"]))

    for c in comments:
        add_comment(c["username"], c["image"], c["creation_date"], c["text"])
        print("Added a new comment for image '%s' from user '%s'" % (r["image"], r["username"]))


def add_user(username, password, email, total_points, rank, currently_participates):
    u = User.objects.get_or_create(username=username,
                                   password=password,
                                   email=email,
                                   total_points=total_points,
                                   rank=rank,
                                   currently_participates=currently_participates)[0]
    u.save()
    return u

def add_image(related_word, username, avg_rating, image):
    i = Image.objects.get_or_create(related_word=related_word,
                                    username=username,
                                    avg_rating=avg_rating,
                                    uploaded_image=image)[0]
    i.save()
    return i

def add_rating(username, image, rating):
    r = Rating.objects.get_or_create(username=username,
                                     image=image,
                                     rating=rating)[0]
    r.save()
    return r

def add_comment(username, image, creation_date, text):
    c = Comment.objects.get_or_create(username=username,
                                      image=image,
                                      creation_date=creation_date,
                                      text=text)[0]
    c.save()
    return c

if __name__ == '__main__':
    print("Starting population script")
    populate()