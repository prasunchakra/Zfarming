"""
Context processors for the core app.
"""
from django.conf import settings


def site_context(request):
    """
    Add site-wide context variables.
    """
    return {
        'site_name': 'ZFarming',
        'site_description': 'Your Personal Urban Garden Assistant',
        'debug': settings.DEBUG,
    }
