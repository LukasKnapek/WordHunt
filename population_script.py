import os, sys, datetime, pytz
import django


# Add the the main project folder to Python path
work_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(work_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WordHunt.settings')


# Get this script's folder
django.setup()

from WordHuntApp.models import *
from django.contrib.auth.models import User
from WordHuntApp.utils import *

def populate():
    # Create the word and the competition related to that word
    word = Word.objects.get_or_create(text="Flag")[0]
    cmp = Competition.objects.get_or_create(word=word,
                                            start_date=datetime.datetime.now(pytz.utc),
                                            end_date=datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=23),
                                            points_to_award=120)

    users = [
        {"username": "XxX_HunTer123",
         "password": "wordhunt",
         "email": "hunter123@email.com",
         "total_points": 564,
         "rank": 1,
         "currently_participates": True,
         "competition_rank": 0,
         "competitions_won": 0},

        {"username": "1337Commander",
         "password": "wordhunt",
         "email": "commando@email.com",
         "total_points": 470,
         "rank": 2,
         "currently_participates": False,
         "competition_rank": None,
         "competitions_won": 0},

        {"username": "Ch0mp",
         "password": "wordhunt",
         "email": "blabla@10minutemail.com",
         "total_points": 254,
         "rank": 3,
         "currently_participates": True,
         "competition_rank": 0,
         "competitions_won": 0},

        {"username": "BTW",
         "password": "wordhunt",
         "email": "ferr@oomla.com",
         "total_points": 90,
         "rank": 4,
         "currently_participates": True,
         "competition_rank": 0,
         "competitions_won": 0},

        {"username": "KillerLady",
         "password": "wordhunt",
         "email": "angel@email.com",
         "total_points": 0,
         "rank": 5,
         "currently_participates": True,
         "competition_rank": 0,
         "competitions_won": 0},
    ]

    for u in users:
        add_user(u["username"], u["password"], u["email"],
                 u["total_points"], u["rank"], u["currently_participates"],
                 u["competition_rank"], u["competitions_won"])
        print("Added %s" % u["username"])

    images = [
        {"word" : Word.objects.get(text="Flag"),
         "user": User.objects.get(username="XxX_HunTer123"),
         "avg_rating": 0,
         "uploaded_image": "flag_entry_1.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "user": User.objects.get(username="BTW"),
         "avg_rating": 0,
         "uploaded_image": "flag_entry_2.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "user": User.objects.get(username="KillerLady"),
         "avg_rating": 0,
         "uploaded_image": "flag_entry_3.jpeg"},

        {"word" : Word.objects.get(text="Flag"),
         "user": User.objects.get(username="Ch0mp"),
         "avg_rating": 0,
         "uploaded_image": "flag_entry_4.jpeg"}
    ]

    for i in images:
        add_image(i["word"], i["user"], i["avg_rating"], i["uploaded_image"])
        print("Added a new image for user %s" % i["user"])

    ratings = [
        {"user" : User.objects.get(username="XxX_HunTer123"),
         "image" : Image.objects.get(user=User.objects.get(username="BTW")),
         "rating" : 5},

        {"user": User.objects.get(username="Ch0mp"),
         "image": Image.objects.get(user=User.objects.get(username="BTW")),
         "rating": 2},

        {"user": User.objects.get(username="BTW"),
         "image": Image.objects.get(user=User.objects.get(username="KillerLady")),
         "rating": 3}
    ]

    comments = [
        {"user": User.objects.get(username="XxX_HunTer123"),
         "image": Image.objects.get(user=User.objects.get(username="BTW")),
         "creation_date": datetime.datetime(2018,2,12,16,30,00,00, pytz.utc),
         "text": "Do you really have to apply filters to EVERY image?"},

        {"user": User.objects.get(username="BTW"),
         "image": Image.objects.get(user=User.objects.get(username="Ch0mp")),
         "creation_date": datetime.datetime(2018,2,12,16,30,00,00, pytz.utc),
         "text": "Very nice!"},

        {"user": User.objects.get(username="XxX_HunTer123"),
         "image": Image.objects.get(user=User.objects.get(username="KillerLady")),
         "creation_date": datetime.datetime(2018,2,12,16,30,00,00, pytz.utc),
         "text": "This feels like such a cliche, you could have put more creativity into it."},
    ]

    for r in ratings:
        add_rating(r["user"], r["image"], r["rating"])
        print("Added a new rating for image '%s' from user '%s'" % (r["image"], r["user"]))

    for c in comments:
        add_comment(c["user"], c["image"], c["creation_date"], c["text"])
        print("Added a new comment for image '%s' from user '%s'" % (r["image"], r["user"]))


def add_user(username, password, email, total_points, rank, currently_participates, comp_rank, comps_won):
    u = User.objects.get_or_create(username=username,
                                   password=password,
                                   email=email)[0]

    profile = UserProfile.objects.get_or_create(user=u,
                                   total_points=total_points,
                                   rank=rank,
                                   currently_participates=currently_participates,
                                   competition_rank=comp_rank,
                                   competitions_won=comps_won)[0]
    print(u, profile)
    return u

def add_image(related_word, user, avg_rating, image):
    i = Image.objects.get_or_create(related_word=related_word,
                                    user=user,
                                    avg_rating=avg_rating,
                                    uploaded_image=image)[0]
    i.save()
    return i

def add_rating(user, image, rating):
    r = Rating.objects.get_or_create(user=user,
                                     image=image,
                                     rating=rating)[0]
    r.save()
    calculate_new_average_rating(image)
    return r

def add_comment(user, image, creation_date, text):
    c = Comment.objects.get_or_create(user=user,
                                      image=image,
                                      creation_date=creation_date,
                                      text=text)[0]
    c.save()
    return c

if __name__ == '__main__':
    print("Starting population script")
    populate()
    update_competition_ranks()
