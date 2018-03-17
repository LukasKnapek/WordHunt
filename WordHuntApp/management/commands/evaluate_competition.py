from WordHuntApp.models import *
from django.core.management.base import BaseCommand, CommandError
from WordHuntApp.utils import *

BASE_POINTS = 5


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Cannot evaluate competition that is still going on
        if is_competition_active():
            self.stdout.write("A competition is still active")
            return

        last_comp = Competition.objects.latest('end_date')

        # Don't evaluate closed competition that has already been evaluated
        if last_comp.evaluated:
            self.stdout.write("The latest competition was already evaluated")
            return

        word = last_comp.word
        awarded_points = last_comp.points_to_award
        participants = UserProfile.objects.filter(currently_participates=True)

        # Awards base amount of points to all users who have participated
        self.stdout.write("Distributing participation points")
        for user in participants:
            user.total_points += BASE_POINTS
            self.stdout.write("Awarding '%s' %s points for participation" % (user, BASE_POINTS))
            user.currently_participates = False
            user.save(update_fields=["total_points", "currently_participates"])


        # Calculate how many people will be awarded with bonus points
        awarded_positions = 1 + len(participants) // 5
        self.stdout.write("%s participants, awarding participants in first %s place(s)" % (len(participants), awarded_positions))

        # Calculate how many points each winner will get
        points_per_winner = awarded_points // awarded_positions
        self.stdout.write("Each winner will get %s points" % points_per_winner)

        # Get the winning entries and fetch the corresponding users
        winning_entries = Image.objects.filter(related_word=word).order_by("-avg_rating")[:awarded_positions]
        for position, entry in enumerate(winning_entries, 1):
            winner = UserProfile.objects.get(user=entry.user)
            winner.total_points += points_per_winner;
            winner.save(update_fields=["total_points"])
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