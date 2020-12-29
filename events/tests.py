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
        url = reverse("match", kwargs={"pk": 8661032232038284220})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["id"]), 8661032232038284220)

    def test_get_match_by_invalid_id(self):
        """GET match by nonexistent ID

        A status of 400 is returned when an invalid ID is provided is to the matches
        endpoint, as well as the appropriate error message
        """
        url = reverse("match", kwargs={"pk": 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Event with ID of 2 not found")

    def test_get_all_matches(self):
        """GET all matches

        A status of 200 is returned when the matches endpoint is called without
        parameters, and the correct number of events are returned
        """
        response = self.client.get(self.url)

        events_count = Event.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), events_count)

    def test_get_events_filtered_by_name(self):
        """GET event filtered by event name

        A status of 200 is returned when the endpoint is called with a name parameter
        that finds a match in the database and returns the correct amount of events
        """
        response = self.client.get(self.url, {"name": "Barcelona vs Real Madrid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_events_filtered_by_invalid_name(self):
        """GET event filtered by event name

        A status of 200 is returned when the endpoint is called with a name parameter
        that doesn't find an event
        """
        response = self.client.get(self.url, {"name": "Barcelona vs Real Mrid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_events_filtered_by_sport_name(self):
        """GET event filtered by sport name

        A status of 200 is returned when the endpoint is called with a sport name parameter
        that finds a match in the database and returns the correct amount of events
        """
        response = self.client.get(self.url, {"sport": "Football"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_events_filtered_by_invalid_sport_name(self):
        """GET event filtered by sport name

        A status of 200 is returned when the endpoint is called with a sport name parameter
        that doesn't find an event
        """
        response = self.client.get(self.url, {"sport": "Ftball"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_post_creates_new_event(self):
        """POST new event

        A status of 201 is returned when an event is posted with a message of `NewEvent`
        and the new event is also returned
        """
        response = self.client.post(self.url, EVENT_TO_BE_CREATED, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(response.data["id"]), EVENT_TO_BE_CREATED["id"])

    def test_post_doesnt_create_a_new_event_if_message_isnt_present(self):
        """POST new event isn't created without a message field

        A status of 400 is return when attempting POST without providing a `message`
        field along with the appropriate error message
        """
        response = self.client.post(self.url, EVENT_WITH_NO_MESSAGE, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message_type"][0], "This field is required.")
        self.assertRaises(
            Event.DoesNotExist, Event.objects.get, id=EVENT_WITH_NO_MESSAGE["id"]
        )

    def test_post_doesnt_create_a_new_event_if_message_unknown(self):
        """POST new event isn't created if the message field has an unknown value

        A status of 400 is return when attempting POST without providing a valid
        `message` field along with the appropriate error message
        """
        response = self.client.post(self.url, EVENT_WITH_UNKNOWN_MESSAGE, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"][0],
            "Unknown message_type. Try again with either `NewEvent` or `UpdateOdds`",
        )
        self.assertRaises(
            Event.DoesNotExist, Event.objects.get, id=EVENT_WITH_UNKNOWN_MESSAGE["id"]
        )

    def test_post_doesnt_create_duplicate_events(self):
        """POST doesn't create duplicate events

        A status of 400 is returned when trying to create an event that already exists
        with an appropriate error message
        """
        response = self.client.post(self.url, EVENT_TO_BE_CREATED, format="json")
        second_response = self.client.post(self.url, DUPLICATE_EVENT, format="json")
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            second_response.data["message"][0],
            f"Event with ID {DUPLICATE_EVENT['id']} already exists. Try updating the odds",
        )

    def test_update_odds(self):
        """POST updates odds with a message of `UpdateOdds`

        A status of 200 is returned when trying to edit the odds of an event that exists
        and the updated object
        """
        response = self.client.post(self.url, EVENT_TO_BE_CREATED, format="json")
        update_response = self.client.post(self.url, EVENT_TO_UPDATE, format="json")

        updated_event = Event.objects.get(id=int(EVENT_TO_UPDATE["id"]))

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            float(update_response.data["markets"][1]["selections"][-2]["odds"]), 10.00
        )
        self.assertEqual(
            float(update_response.data["markets"][1]["selections"][-1]["odds"]), 5.55
        )
