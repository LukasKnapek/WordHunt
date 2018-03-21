import datetime, pytz, exifread
from WordHuntApp.models import *


def get_current_word():
    competition = Competition.objects.latest('start_date')
    word = competition.word

    return word


def is_competition_active():
    competition = Competition.objects.latest('start_date')
    now = datetime.datetime.now(pytz.utc)

    return competition.start_date < now < competition.end_date


# Convert the GPS coordinates from DMS (degrees, minutes, deconds) format
# to DD (degrees, degrees) format, which is more useful
def _convert_from_dms_to_dd(coords):
    # Convert one operand to float so we get float division
    degrees = float(coords.values[0].num) / coords.values[0].den
    minutes = float(coords.values[1].num) / coords.values[1].den
    seconds = float(coords.values[2].num) / coords.values[2].den

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def get_image_coordinates(path):
    image = open(path, 'rb')
    exif_tags = exifread.process_file(image, details=False)
    try:
        latitude_ref = exif_tags["GPS GPSLatitudeRef"]
        longitude_ref = exif_tags["GPS GPSLongitudeRef"]
        latitude = exif_tags["GPS GPSLatitude"]
        longitude = exif_tags["GPS GPSLongitude"]
    except KeyError:
        return False

    # If we don't have all the data, we cannot parse the coordinates
    if not (latitude and latitude_ref and longitude and longitude_ref):
        return False

    lat_dd = _convert_from_dms_to_dd(latitude)
    long_dd = _convert_from_dms_to_dd(longitude)
    if latitude_ref.values == 'S':
        lat_dd = -lat_dd
    if longitude_ref.values == 'W':
        long_dd = -long_dd

    return lat_dd, long_dd

def calculate_new_average_rating(image):
    image_ratings = Rating.objects.filter(image=image)
    image.avg_rating = sum(r.rating for r in image_ratings) / len(image_ratings)
    image.save()

