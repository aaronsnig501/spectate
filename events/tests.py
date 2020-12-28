from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .models import Event
from .fixtures.events import EVENT_TO_BE_CREATED, EVENT_TO_UPDATE
from sports.models import Sport


class EventTestCase(APITestCase):
    fixtures = ["events.json"]

    def test_get_match_by_id(self):
        """GET match by ID

        A status of 200 is returned when an ID is provided is to the matches endpoint,
        as well as the correct event
        """
        url = reverse("match", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["id"]), 1)

    def test_get_all_matches(self):
        """GET all matches

        A status of 200 is returned when the matches endpoint is called without
        parameters, and the correct number of events are returned
        """
        url = reverse("matches")
        response = self.client.get(url)

        events_count = Event.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), events_count)

    def test_post_creates_new_event(self):
        """POST new event

        A status of 201 is returned when an event is posted with a message of `NewEvent`
        and the new event is also returned
        """
        url = reverse("matches")
        response = self.client.post(url, EVENT_TO_BE_CREATED, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data["id"]), EVENT_TO_BE_CREATED["id"])

    def test_post_doesnt_create_duplicate_events(self):
        """POST doesn't create duplicate events

        A status of 400 is returned when trying to create an event that already exists
        with an appropriate error message
        """
        url = reverse("matches")
        response = self.client.post(url, EVENT_TO_BE_CREATED, format="json")
        second_response = self.client.post(url, EVENT_TO_BE_CREATED, format="json")
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            second_response.data["message"][0],
            "Event with ID 994839351740 already exists. Try updating the odds",
        )
