import requests

ACCESS_USER = "STANDARD_USER";
ACCESS_ADMIN = "ADMIN_USER";

class MyRadioClient:

    def __init__(self, config):
        self.config = config

    def get_user_id_if_exists(self, user, password):
        api_request_url = self.config["myradio"]["api_url"] + "/auth/testcredentials"
        api_request_data = {
            "user": user,
            "pass": password
        }
        api_request_params = {
            "api_key": self.config["myradio"]["api_key"]
        }
        result = requests.post(
            api_request_url,
            data=api_request_data,
            params=api_request_params,
            headers={"User-Agent": "JARS/0.1"})

        if result.status_code != 200:
            raise MyRadioServiceFailureException(result.text if result.text else result)

        data = result.json()

        if not data["payload"]:
            raise NoUserException(data)

        return data["payload"]["memberid"]

    def get_user_access_level(self, memberid):
        api_request_url = self.config["myradio"]["api_url"] + "/user/" + str(memberid) + "/permissions"
        api_request_params = {
            "api_key": self.config["myradio"]["api_key"]
        }
        result = requests.get(api_request_url, params=api_request_params, headers={"User-Agent": "JARS/0.1"})

        if result.status_code != 200:
            raise MyRadioServiceFailureException(result.text if result.text else result)

        data = result.json()

        if self.config["myradio"]["super_user_permission"] in data["payload"]:
            return ACCESS_ADMIN

        if self.config["myradio"]["standard_user_permission"] in data["payload"]:
            return ACCESS_USER

        raise NoUserPermissionException(data)


class NoUserException(Exception):
    pass

class NoUserPermissionException(Exception):
    pass

class MyRadioServiceFailureException(Exception):
    pass
