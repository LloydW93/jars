import unittest, Event, MyRadioClient
from unittest.mock import patch
from datetime import datetime

class EventTest(unittest.TestCase):

    TEST_UUID = "cea110a4-8fb8-400e-9952-7e2613e9bdb2"
    TEST_UUID_2 = "cea110a4-8fb8-400e-9952-7e2613e9bdb3"
    TEST_INVALID_UUID = "cea110a4-8fb8-500e-9952-7e2613e9bdb2"

    USER_CLAIM_NORMAL_1 = {
        "sub": 123,
        "access_level": MyRadioClient.ACCESS_USER
    }

    USER_CLAIM_NORMAL_2 = {
        "sub": 456,
        "access_level": MyRadioClient.ACCESS_USER
    }

    USER_CLAIM_ADMIN = {
        "sub": 789,
        "access_level": MyRadioClient.ACCESS_ADMIN
    }

    CONFIG = {
            "db": {
                "host": "banana.fm",
                "port": 5432,
                "user": "jars",
                "password": "jars",
                "dbname": "jars"
            },
            "events": {
                "lifetime": 86400
            }
        }

    @patch('Event.psycopg2.connect')
    @patch('Event.uuid')
    @patch('Event.datetime')
    def test_create_event(self, mock_today, mock_uuid, mock_connect):
        mock_today.today.return_value = datetime(2018, 1, 2, 3, 4, 5)
        expected_expires_datetime = datetime(2018, 1, 3, 3, 4, 5)

        mock_uuid.uuid4.return_value = EventTest.TEST_UUID

        under_test = Event.Event(EventTest.CONFIG)

        uuid = under_test.create_event(EventTest.USER_CLAIM_NORMAL_1, "Title", "Description", False)

        self.assertEqual(uuid, self.TEST_UUID)

        mock_connect.assert_called_with(host="banana.fm", port=5432, user="jars", password="jars", dbname="jars")
        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value

        mock_cur.execute.assert_called_with(
            "INSERT INTO jars.events (event_uuid, created_by, expires_time, title, description, private) VALUES (%s, %s, %s, %s, %s, %s)",
            (EventTest.TEST_UUID, 123, expected_expires_datetime, "Title", "Description", False))

    @patch('Event.psycopg2.connect')
    def test_connect_event_valid(self, mock_connect):
        mock_connect.return_value.cursor.return_value.rowcount = 1
        mock_connect.return_value.cursor.return_value.fetchone.return_value = {
            "created_by": 123
        }

        under_test = Event.Event(EventTest.CONFIG)

        under_test.connect_to_event(EventTest.USER_CLAIM_NORMAL_1, EventTest.TEST_UUID)

    @patch('Event.psycopg2.connect')
    def test_connect_event_uuid_invalid(self, mock_connect):
        under_test = Event.Event(EventTest.CONFIG)

        with self.assertRaises(Event.InvalidIdentifierException):
            under_test.connect_to_event(EventTest.USER_CLAIM_NORMAL_1, EventTest.TEST_INVALID_UUID)

    @patch('Event.psycopg2.connect')
    def test_connect_event_nonexistent(self, mock_connect):
        mock_connect.return_value.cursor.return_value.rowcount = 0

        under_test = Event.Event(EventTest.CONFIG)

        with self.assertRaises(Event.NonExistentOrExpiredEventException):
            under_test.connect_to_event(EventTest.USER_CLAIM_NORMAL_1, EventTest.TEST_UUID_2)

    @patch('Event.psycopg2.connect')
    def test_connect_event_user_not_authorised(self, mock_connect):
        mock_connect.return_value.cursor.return_value.rowcount = 1
        mock_connect.return_value.cursor.return_value.fetchone.return_value = {
            "created_by": 123
        }

        under_test = Event.Event(EventTest.CONFIG)

        with self.assertRaises(Event.UnauthorizedConnectionException):
            under_test.connect_to_event(EventTest.USER_CLAIM_NORMAL_2, EventTest.TEST_UUID)

    @patch('Event.psycopg2.connect')
    def test_connect_event_user_is_admin(self, mock_connect):
        mock_connect.return_value.cursor.return_value.rowcount = 1
        mock_connect.return_value.cursor.return_value.fetchone.return_value = {
            "created_by": 123
        }

        under_test = Event.Event(EventTest.CONFIG)

        under_test.connect_to_event(EventTest.USER_CLAIM_ADMIN, EventTest.TEST_UUID)
