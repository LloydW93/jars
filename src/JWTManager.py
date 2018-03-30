import jwt
from datetime import datetime, timedelta

class JWTManager:
    
    def __init__(self, config):
        self.config = config

    def generate_jwt(self, memberid, access_level):
        creation_time = datetime.today()
        expiry_time = datetime.today() + timedelta(0, self.config["jwt"]["token_lifetime"])

        payload = {
            "iss": "jars",
            "sub": memberid,
            "iat": int(creation_time.timestamp()),
            "exp": int(expiry_time.timestamp()),
            "access_level": access_level
        }

        # Try and minimise how often/long this is in RAM, if possible...
        with open(self.config["jwt"]["private_key"], "r") as f:
            private_key = f.read()
            return jwt.encode(payload, private_key, algorithm="RS256")

    def decode_and_validate(self, claim):
        with open(self.config["jwt"]["public_key"], "r") as f:
            public_key = f.read()
            return jwt.decode(claim, public_key, algorithms=["RS256"])
