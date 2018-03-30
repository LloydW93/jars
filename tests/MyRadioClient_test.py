import unittest, json, MyRadioClient
from unittest.mock import patch
from collections import namedtuple

class MyRadioClientTest(unittest.TestCase):

    CONFIG = {
            "myradio": {
                "api_url": "http://localhost/api/v2",
                "api_key": "q1w2e3r4t5",
                "standard_user_permission": -1,
                "super_user_permission": -2
            }
        }

    def configure_json_return_value(self, mock, resource):
        with open("tests/resources/" + resource, "r") as f:
            return_json = json.load(f)
        mock.return_value = namedtuple("Response", ["status_code", "json"])
        mock.return_value.status_code = 200
        mock.return_value.json = lambda: return_json

    @patch('MyRadioClient.requests.post')
    def test_login_invalid_fails(self, mock_post):
        self.configure_json_return_value(mock_post, "testcredentials_notexists.json")

        under_test = MyRadioClient.MyRadioClient(self.CONFIG)

        with self.assertRaises(MyRadioClient.NoUserException):
            under_test.get_user_id_if_exists("user", "pass")

        mock_post.assert_called_with("http://localhost/api/v2/auth/testcredentials", data={
                "user": "user",
                "pass": "pass",
                "api_key": self.CONFIG["myradio"]["api_key"],
            }, headers={"User-Agent": "JARS/0.1"})

    @patch('MyRadioClient.requests.post')
    def test_login_valid_succeeds(self, mock_post):
        self.configure_json_return_value(mock_post, "testcredentials_exists.json")

        under_test = MyRadioClient.MyRadioClient(self.CONFIG)

        self.assertEqual(under_test.get_user_id_if_exists("user", "pass"), 123)

        mock_post.assert_called_with("http://localhost/api/v2/auth/testcredentials", data={
                "user": "user",
                "pass": "pass",
                "api_key": self.CONFIG["myradio"]["api_key"]
            }, headers={"User-Agent": "JARS/0.1"})

    @patch('MyRadioClient.requests.get')
    def test_permissions_none(self, mock_get):
        self.configure_json_return_value(mock_get, "getpermissions_none.json")

        under_test = MyRadioClient.MyRadioClient(self.CONFIG)

        with self.assertRaises(MyRadioClient.NoUserPermissionException):
            under_test.get_user_access_level(123)

        mock_get.assert_called_with("http://localhost/api/v2/user/123/permissions", data={
                "api_key": self.CONFIG["myradio"]["api_key"]
            }, headers={"User-Agent": "JARS/0.1"})

    @patch('MyRadioClient.requests.get')
    def test_permissions_user(self, mock_get):
        self.configure_json_return_value(mock_get, "getpermissions_user.json")

        under_test = MyRadioClient.MyRadioClient(self.CONFIG)

        self.assertEqual(under_test.get_user_access_level(123), MyRadioClient.ACCESS_USER)

        mock_get.assert_called_with("http://localhost/api/v2/user/123/permissions", data={
                "api_key": self.CONFIG["myradio"]["api_key"]
            }, headers={"User-Agent": "JARS/0.1"})

    @patch('MyRadioClient.requests.get')
    def test_permissions_admin(self, mock_get):
        self.configure_json_return_value(mock_get, "getpermissions_admin.json")

        under_test = MyRadioClient.MyRadioClient(self.CONFIG)

        self.assertEqual(under_test.get_user_access_level(123), MyRadioClient.ACCESS_ADMIN)

        mock_get.assert_called_with("http://localhost/api/v2/user/123/permissions", data={
                "api_key": self.CONFIG["myradio"]["api_key"]
            }, headers={"User-Agent": "JARS/0.1"})
