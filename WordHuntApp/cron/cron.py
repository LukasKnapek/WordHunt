import random, os, datetime, pytz
from WordHuntApp.models import Word, Competition


def generate_competition():
    # Get this script's folder
    work_dir = os.path.dirname(__file__)
    input_file = os.path.join(work_dir, "nounlist.txt")
    competition_duration_hours = 12

    with open(input_file) as inp:
        nouns = inp.readlines()
    chosen_word = random.choice(nouns)

    # Remove the chosen word from all nouns and resave
    nouns.remove(chosen_word)
    with open(input_file, "w") as out:
        out.writelines(nouns)

    # Create a new Word object and an associated Competition
    word = Word.objects.get_or_create(text=chosen_word.capitalize())[0]
    comp = Competition.objects.get_or_create(word=word,
                                             start_date = datetime.datetime.now(pytz.utc),
                                             end_date = datetime.datetime.now(pytz.utc) 
                                                        + datetime.timedelta(hours=competition_duration_hours),
                                             points_to_award=random.randint(2, 6) * 10)[0]