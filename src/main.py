import tornado.ioloop, tornado.web, json, JWTManager, MyRadioClient, Event

with open('/etc/jars/config.json', 'r') as f:
    config = json.load(f)

class GetTokenHandler(tornado.web.RequestHandler):
    def post(self):
        # Probably needs to do a bit more...
        # Like validate the credentials...
        # Not make everyone an admin...
        # Respond in JSON, not raw text...
        # That kind of thing, really.
        jwt = JWTManager.JWTManager(config)
        token = jwt.generate_jwt(self.get_argument('user'), MyRadioClient.ACCESS_ADMIN)
        self.write(token)

class ConnectHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            jwt = JWTManager.JWTManager(config)
            event = Event.Event(config)
            claim = jwt.decode_and_validate(self.get_argument('auth'))
            event.connect_to_event(claim, self.get_argument('mount'))
            self.finish('OK')
        except Exception as e:
            self.set_status(500)
            self.finish(type(e).__name__)

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
            self.finish(event_uuid)
        except Exception as e:
            self.set_status(500)
            self.finish(type(e).__name__)

application = tornado.web.Application([
    ('/jars/token', GetTokenHandler),
    ('/jars/connect', ConnectHandler)
    ('/jars/create', CreateHandler)
])

application.listen(8888)

tornado.ioloop.IOLoop.instance().start()
