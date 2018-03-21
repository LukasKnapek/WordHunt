import random, os, datetime, pytz
from WordHuntApp.models import *
from django.core.management.base import BaseCommand
from WordHuntApp.utils import *

class Command(BaseCommand):

    BASE_POINTS = 5
    COMPETITION_DURATION = datetime.timedelta(days=1)

    def handle(self, *args, **options):
        self.close_competition()
        self.generate_new_competition()

    def close_competition(self):
        # If there is no active competition, get the most recent one (if it hasn't been evaluated yet)
        if not is_competition_active():
            self.stdout.write("There is no currently active competition")
            self.stdout.write("Checking whether the latest closed competition has been evaluated yet")

            last_comp = Competition.objects.latest('end_date')

            if last_comp.evaluated:
                self.stdout.write("The latest closed competition has already been evaluated")
                self.stdout.write("Skipping evaluation...")
                return
            else:
                self.stdout.write("The latest closed competition has not been evaluated yet")

        # Otherwise, just get the current active competition
        else:
            last_comp = Competition.objects.latest('start_date')

        # Close the competition, if it is active
        if is_competition_active():
            last_comp.end_date = datetime.datetime.now(pytz.utc)

        # Evaluate the competition
        self.evaluate_competition(last_comp)

    def generate_new_competition(self):
        # Get this script's folder
        work_dir = os.path.dirname(__file__)
        input_file = os.path.join(work_dir, "nounlist.txt")

        # Choose a random noun
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
                                                          + Command.COMPETITION_DURATION,
                                                 points_to_award=random.randint(2, 6) * 10)[0]
        word.save()
        comp.save()

        self.stdout.write("\nNew competition generated:")
        self.stdout.write("Word: '%s'" % comp.word)
        self.stdout.write("Start date: '%s'" % comp.start_date)
        self.stdout.write("End date: '%s'" % comp.end_date)
        self.stdout.write("Points: '%s'" % comp.points_to_award)

    def evaluate_competition(self, last_comp):
        word = last_comp.word
        awarded_points = last_comp.points_to_award
        participants = UserProfile.objects.filter(currently_participates=True)

        # Awards base amount of points to all users who have participated
        self.stdout.write("Distributing participation points")
        for user in participants:
            user.total_points += Command.BASE_POINTS
            self.stdout.write("Awarding '%s' %s points for participation" % (user, Command.BASE_POINTS))
            user.currently_participates = False
            user.save(update_fields=["total_points", "currently_participates"])

        # Calculate how many people will be awarded with bonus points
        awarded_positions = 1 + len(participants) // 5
        self.stdout.write(
            "%s participants, awarding participants in first %s place(s)" % (len(participants), awarded_positions))

        # Calculate how many points each winner will get
        points_per_winner = awarded_points // awarded_positions
        self.stdout.write("Each winner will get %s points" % points_per_winner)

        # Get the winning entries and fetch the corresponding users
        winning_entries = Image.objects.filter(related_word=word).order_by("-avg_rating")[:awarded_positions]
        for position, entry in enumerate(winning_entries, 1):
            winner = UserProfile.objects.get(user=entry.user)
            winner.total_points += points_per_winner;
            winner.competitions_won += 1
            winner.save(update_fields=["total_points", "competitions_won"])
            self.stdout.write("'%s' is in %s. place! (avg. image rating %s) -> +%s points" %
                              (winner, position, entry.avg_rating, points_per_winner))

        # Update user ranks
        self.stdout.write("")
        self.stdout.write("New rankings:")
        for new_rank, user in enumerate(UserProfile.objects.all().order_by("-total_points"), 1):
            user.rank = new_rank
            user.save(update_fields=["rank"])
            self.stdout.write("%s - %s points, %s. place" % (user, user.total_points, user.rank))

        # Mark competition as evaluated
        last_comp.evaluated = True
        last_comp.save()
