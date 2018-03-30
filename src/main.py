import tornado.ioloop, tornado.web, json, JWTManager, MyRadioClient, Event, traceback

with open('/etc/jars/config.json', 'r') as f:
    config = json.load(f)

def handle_exception(exception, req):
    traceback.print_exc()
    # Todo: Map failures to their fault and our fault (4xx vs 5xx)
    req.set_status(500)
    response = {
        "error": type(exception).__name__
    }
    req.finish(json.dumps(response) + "\n")

class GetTokenHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            myradio = MyRadioClient.MyRadioClient(config)
            member_id = myradio.get_user_id_if_exists(self.get_argument('user'), self.get_argument('password'))
            jwt = JWTManager.JWTManager(config)
            token = jwt.generate_jwt(member_id, myradio.get_user_access_level(member_id))
            response = {
                "token": token.decode('ascii')
            }
            self.finish(json.dumps(response) + "\n")
        except Exception as e:
            handle_exception(e, self)

class ConnectHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            jwt = JWTManager.JWTManager(config)
            event = Event.Event(config)
            claim = jwt.decode_and_validate(self.get_argument('auth'))
            event.connect_to_event(claim, self.get_argument('mount'))
            self.set_status(202)
            self.finish()
        except Exception as e:
            handle_exception(e, self)

class CreateHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            title = self.get_argument('title')
            description = self.get_argument('description')
            private = self.get_argument('private')

            jwt = JWTManager.JWTManager(config)
            event = Event.Event(config)
            claim = jwt.decode_and_validate(self.get_argument('auth'))
            event_uuid = event.create_event(claim, title, description, private)
            response = {
                "event_id": event_uuid
            }
            self.set_status(201)
            self.finish(json.dumps(response) + "\n")
        except Exception as e:
            handle_exception(e, self)

class KeyHandler(tornado.web.RequestHandler):
    def get(self):
        jwt = JWTManager.JWTManager(config)
        self.finish(jwt.get_public_key())

application = tornado.web.Application([
    ('/jars/token', GetTokenHandler),
    ('/jars/connect', ConnectHandler),
    ('/jars/create', CreateHandler),
    ('/jars/pubkey', KeyHandler)
])

application.listen(8888)

tornado.ioloop.IOLoop.instance().start()
