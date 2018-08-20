#Custom context processors

from django.conf import settings


def site(request):
    return {
        'SITE_BASE_URL': settings.SITE_BASE_URL,
        'IDP_NAME': settings.IDP_NAME,
        'IDP_LOGO': settings.IDP_LOGO,
        'SERVICE_PROVIDER': settings.SERVICE_PROVIDER,
        'SERVICE_PROVIDER_URL': settings.SERVICE_PROVIDER_URL
    }