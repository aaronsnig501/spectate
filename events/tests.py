from datetime import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import Event
from .fixtures.events import (
    EVENT_TO_BE_CREATED,
    EVENT_TO_UPDATE,
    DUPLICATE_EVENT,
    EVENT_WITH_NO_MESSAGE,
    EVENT_WITH_UNKNOWN_MESSAGE,
)
from sports.models import Sport


class EventTestCase(APITestCase):
    fixtures = ["events.json"]
    url = reverse("matches")

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
        response = self.client.get(self.url)

        events_count = Event.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), events_count)

    def test_post_creates_new_event(self):
        """POST new event

        A status of 201 is returned when an event is posted with a message of `NewEvent`
        and the new event is also returned
        """
        url = reverse("matches")
        response = self.client.post(self.url, EVENT_TO_BE_CREATED, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data["id"]), EVENT_TO_BE_CREATED["id"])

        # Clean up to ensure that this error doesn't fire sporatically
        Event.objects.get(id=EVENT_TO_BE_CREATED["id"]).delete()

    def test_post_doesnt_create_a_new_event_if_message_isnt_present(self):
        """POST new event isn't created without a message field

        A status of 400 is return when attempting POST without providing a `message`
        field along with the appropriate error message
        """
        url = reverse("matches")
        response = self.client.post(self.url, EVENT_WITH_NO_MESSAGE, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"][0], "This field is required.")
        self.assertRaises(
            Event.DoesNotExist, Event.objects.get, id=EVENT_WITH_NO_MESSAGE["id"]
        )

    def test_post_doesnt_create_a_new_event_if_message_isnt_present(self):
        """POST new event isn't created without a message field

        A status of 400 is return when attempting POST without providing a `message` field
        along with the appropriate error message
        """
        url = reverse("matches")
        response = self.client.post(self.url, EVENT_WITH_UNKNOWN_MESSAGE, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            "Unknown message. Try again with either `NewEvent` or `UpdateOdds`",
        )
        self.assertRaises(
            Event.DoesNotExist, Event.objects.get, id=EVENT_WITH_UNKNOWN_MESSAGE["id"]
        )

    def test_post_doesnt_create_duplicate_events(self):
        """POST doesn't create duplicate events

        A status of 400 is returned when trying to create an event that already exists
        with an appropriate error message
        """
        url = reverse("matches")
        response = self.client.post(self.url, EVENT_TO_BE_CREATED, format="json")
        second_response = self.client.post(url, DUPLICATE_EVENT, format="json")
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            second_response.data["message"][0],
            "Event with ID 994839351740 already exists. Try updating the odds",
        )
