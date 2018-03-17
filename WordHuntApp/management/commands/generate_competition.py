import random, os, datetime, pytz
from WordHuntApp.models import Word, Competition
from django.core.management.base import BaseCommand, CommandError
from WordHuntApp.utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):

        competition_duration = datetime.timedelta(hours=23, minutes=50)

#        if is_competition_active():
#            self.stdout.write("Cannot generate a new competition, another competition is still active")
#            return

        # Get this script's folder
        work_dir = os.path.dirname(__file__)
        input_file = os.path.join(work_dir, "nounlist.txt")

        with open(input_file) as inp:
            nouns = inp.read().split(",")
        chosen_word = random.choice(nouns)

        # Remove the chosen word from all nouns and resave
        nouns.remove(chosen_word)
        with open(input_file, "w") as out:
            out.writelines(",".join(nouns))

        # Create a new Word object and an associated Competition
        word = Word.objects.get_or_create(text=chosen_word.capitalize())[0]
        comp = Competition.objects.get_or_create(word=word,
                                                 start_date=datetime.datetime.now(pytz.utc),
                                                 end_date=datetime.datetime.now(pytz.utc)
                                                          + competition_duration,
                                                 points_to_award=random.randint(2, 6) * 10)[0]

        word.save()
        comp.save()

        self.stdout.write("New competition generated:")
        self.stdout.write("Word: '%s'" % comp.word)
        self.stdout.write("Start date: '%s'" % comp.start_date)
        self.stdout.write("End date: '%s'" % comp.end_date)
        self.stdout.write("Points: '%s'" % comp.points_to_award)