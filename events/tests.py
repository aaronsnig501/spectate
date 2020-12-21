from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .models import Event
from sports.models import Sport


class EventTestCase(APITestCase):
    def setUp(self):
        """Create a new match event"""
        sport = Sport(name="Football")
        sport.save()

        event = Event(
            name="Real Madrid vs Barcelona", start_time=datetime.now(), sport=sport
        )
        event.save()

    def test_get_match_by_id(self):
        """Test get match by ID

        A status of 200 is returned when an ID is provided is to the matches endpoint
        """
        url = reverse("match", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
