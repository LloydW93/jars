import psycopg2, uuid, re, MyRadioClient, psycopg2.extras
from datetime import datetime, timedelta

class Event:

    CREATE_SQL = "INSERT INTO jars.events (event_uuid, created_by, expires_time, title, description, private) VALUES (%s, %s, %s, %s, %s, %s)"
    FETCH_SQL = "SELECT * FROM jars.events WHERE event_uuid=%s AND expires_time > NOW()"
    CONNECT_SQL = "UPDATE jars.events SET connected=true, connected_by=%s WHERE event_uuid=%s"

    def __init__(self, config):
        self.config = config;
        self.db = psycopg2.connect(
            host=config["db"]["host"],
            port=config["db"]["port"],
            user=config["db"]["user"],
            password=config["db"]["password"],
            dbname=config["db"]["dbname"]
        )

    def create_event(self, claim, title, description, private):
        event_id = str(uuid.uuid4())
        expiry_time = datetime.today() + timedelta(0, self.config["events"]["lifetime"])

        cur = self.db.cursor()
        cur.execute(Event.CREATE_SQL, (event_id, claim["sub"], expiry_time, title, description, private))
        self.db.commit()

        return event_id

    def connect_to_event(self, claim, event_id):
        uuid_pattern = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$")

        if uuid_pattern.match(event_id) == None:
            raise InvalidIdentifierException()

        cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute(Event.FETCH_SQL, (event_id,))

        if cur.rowcount == 0:
            raise NonExistentOrExpiredEventException()

        row = cur.fetchone()

        if claim["access_level"] != MyRadioClient.ACCESS_ADMIN:
            # Admins can always connect, but check normal users
            if claim["sub"] != row["created_by"]:
                raise UnauthorizedConnectionException()

        cur.execute(Event.CONNECT_SQL, (claim["sub"], event_id))

        self.db.commit()


class InvalidIdentifierException(Exception):
    pass

class NonExistentOrExpiredEventException(Exception):
    pass

class UnauthorizedConnectionException(Exception):
    pass
