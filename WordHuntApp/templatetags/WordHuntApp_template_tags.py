from django import template
from WordHuntApp.models import UserProfile

register = template.Library()

@register.inclusion_tag('WordHuntApp/topUsers.html')
def get_user_list():
    user_list = UserProfile.objects.order_by('rank')[:10]
    dict = {'users':user_list}
    return dict

# Check whether the given user participates and return the corresponding text to be shown
@register.simple_tag(takes_context=True)
def participation_text(context):
    user = context["user"]
    participates = UserProfile.objects.get(user=user).currently_participates
    if participates: return 'Entry Submitted'
    else: return 'Entry NOT Submitted'

# Check whether the given user participates and return the corresponding color to be shown
@register.simple_tag(takes_context=True)
def participation_color(context):
    user = context["user"]
    participates = UserProfile.objects.get(user=user).currently_participates
    if participates: return '#5cb85c'
    else: return '#d9534f'


