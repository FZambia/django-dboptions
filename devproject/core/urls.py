from django.conf.urls import patterns, url
from core.views import HelloView


urlpatterns = patterns(
    'core.views',
    url(r'^$', HelloView.as_view(), name="core_hello"),
)