from django import template
from WordHuntApp.models import UserProfile

register = template.Library()

@register.inclusion_tag('WordHuntApp/topUsers.html')
def get_user_list():
    user_list = UserProfile.objects.order_by('rank')[:5]
    dict = {'users':user_list}
    return dict
