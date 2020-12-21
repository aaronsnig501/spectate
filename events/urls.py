from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import EventsAPI

urlpatterns = [
    path("", EventsAPI.as_view(), name="matches"),
    path("<int:pk>", EventsAPI.as_view(), name="match"),
]

urlpatterns = format_suffix_patterns(urlpatterns)