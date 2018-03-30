import unittest, json, JWTManager, MyRadioClient, jwt
from unittest.mock import patch
from datetime import datetime

class JWTManagerTest(unittest.TestCase):

    # Manually created on jwt.io
    VALID_CLAIM = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqYXJzIiwiZXhwIjoxNTIyNDM2NjAxLCJpYXQiOjE1MjIzNTAyMDEsImFjY2Vzc19sZXZlbCI6IkFETUlOX1VTRVIiLCJzdWIiOiIxMjMifQ.Vk2aBuP9BCX1H-TdnR9oZ0r9z_1wsN_NwvSuMBozp0jcATY1n6lo9mFgKp_dGtM-WGgsBpF6EhMOCefOava8kk0scyWf5vofsNq3Gazrxeb9x1uRREo0fnt_dlfkuciUP9glTCqbpVDjeU67BdNApNyst_uqRb3nRAQUnyX1A0wyjNmksONv53QEIaT4HKQjm3ko9N6ueaN1M6Pnzd74EnnmFdjRXmTqk91xrWLT61fzhMmebn8XKO94r6oJPFW8ANk-9LhtniZL5hIkEnH63ZDmnD-IxcKP9lFY3QRl56e11HzyYNm0oNQEw1Zgigvvs_wXZlaTNBvkOas-k_-vjQ"

    CONFIG = {
            "jwt": {
                "private_key": "resources/sample_service.key",
                "public_key": "resources/sample_service.pem",
                "token_lifetime": 86400
            }
        }

    @patch('JWTManager.datetime')
    def test_generate_standard_jwt(self, mock_today):
        # 2099 as JWT handles expiry for you
        mock_today.today.return_value = datetime(2099, 1, 2, 3, 4, 5)
        expected_expires_datetime = datetime(2099, 1, 3, 3, 4, 5)

        under_test = JWTManager.JWTManager(self.CONFIG)

        generated_jwt = under_test.generate_jwt(123, MyRadioClient.ACCESS_USER)

        with open(self.CONFIG["jwt"]["public_key"], "r") as f:
            public_key = f.read()

        decoded_claim = jwt.decode(generated_jwt, public_key, algorithms=["RS256"])

        self.assertEqual(decoded_claim["iat"], int(mock_today.today.return_value.timestamp()))
        self.assertEqual(decoded_claim["exp"], int(expected_expires_datetime.timestamp()))
        self.assertEqual(decoded_claim["access_level"], MyRadioClient.ACCESS_USER)
        self.assertEqual(decoded_claim["sub"], 123)
        self.assertEqual(decoded_claim["iss"], "jars")

    @patch('JWTManager.datetime')
    def test_generate_admin_jwt(self, mock_today):
        # 2099 as JWT handles expiry for you
        mock_today.today.return_value = datetime(2099, 1, 2, 3, 4, 5)
        expected_expires_datetime = datetime(2099, 1, 3, 3, 4, 5)

        under_test = JWTManager.JWTManager(self.CONFIG)

        generated_jwt = under_test.generate_jwt(456, MyRadioClient.ACCESS_ADMIN)

        with open(self.CONFIG["jwt"]["public_key"], "r") as f:
            public_key = f.read()

        decoded_claim = jwt.decode(generated_jwt, public_key, algorithms=["RS256"])

        self.assertEqual(decoded_claim["iat"], int(mock_today.today.return_value.timestamp()))
        self.assertEqual(decoded_claim["exp"], int(expected_expires_datetime.timestamp()))
        self.assertEqual(decoded_claim["access_level"], MyRadioClient.ACCESS_ADMIN)
        self.assertEqual(decoded_claim["sub"], 456)
        self.assertEqual(decoded_claim["iss"], "jars")

    @patch('JWTManager.datetime')
    def test_generate_expired_jwt(self, mock_today):
        # 2099 as JWT handles expiry for you
        mock_today.today.return_value = datetime(1999, 1, 2, 3, 4, 5)
        expected_expires_datetime = datetime(1999, 1, 3, 3, 4, 5)

        under_test = JWTManager.JWTManager(self.CONFIG)

        generated_jwt = under_test.generate_jwt(789, MyRadioClient.ACCESS_ADMIN)

        with open(self.CONFIG["jwt"]["public_key"], "r") as f:
            public_key = f.read()

        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            decoded_claim = jwt.decode(generated_jwt, public_key, algorithms=["RS256"])

    @patch('JWTManager.datetime')
    def test_validating_valid_jwt(self, mock_today):
        mock_today.today.return_value = datetime(2018, 3, 30, 0, 0, 0)

        under_test = JWTManager.JWTManager(self.CONFIG)

        decoded_claim = under_test.decode_and_validate(JWTManagerTest.VALID_CLAIM)

        self.assertEqual(decoded_claim["access_level"], MyRadioClient.ACCESS_ADMIN)
