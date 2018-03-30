Just Another Radio Station
==========================

Getting started:
- Create an /etc/jars/config.json with example config
- Create an /etc/jars/service.pem, service.key, with generated values
- pip3 install pipenv (or pip install pipenv if you're on a 3 native system)
- pipenv install
- pipenv run python src/main.py

API
---

### GET /jars/pubkey

Returns the public part of the keypair used for signing JWT claims.

```
$ curl -v http://localhost:8888/jars/pubkey
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> GET /jars/pubkey HTTP/1.1
> Host: localhost:8888
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Fri, 30 Mar 2018 12:36:25 GMT
< Etag: "ca4d786c9f32e8861bc4f9de0acbe83d9be9465a"
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Content-Length: 451
<
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm2CecPMulYLZeW7+Brf2
pVb14PWwgbv1ZnQjmp/RsFeu/dYbvR3XBIl4ozcH15LRE8g7ZTzhPYm4tQjYQn9u
NAELGjlU9It9VCSX7STdH+r3xTO5pQtBobWaXs8pv/Di3og2p4oGEWsxKxci2J08
NoUlKFL+x2LZ7Z+vc6h6QMdegOPht3kWZ/YrhDdvZT7jENo0fi7xRUiOl6FZi4gk
wBAR9gAG782jx0ZI4HargxETy1KwVl6BuFjFUQfu9kkDZxeq4j7+ID30lhqGhoxt
Ujz/YKP5Z9sGXB+Wk2UxA2vnbs9WAoVpgmIjjE+fRQC0MpSGRowPn/EkV/gCXFhS
MQIDAQAB
-----END PUBLIC KEY-----
* Connection #0 to host localhost left intact
```

### POST /jars/token
Required: user, password

Validate the given credentials against MyRadio, and if valid, returns a JWT claim
valid for the next 24 hours (default, configurable)

```
$ curl -vd"user=lpw503&password=my_password" http://localhost:8888/jars/token
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/token HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 31
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 32 out of 32 bytes
< HTTP/1.1 200 OK
< Date: Fri, 30 Mar 2018 12:34:51 GMT
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Content-Length: 510
<
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1MjI0OTk2OTIsInN1YiI6NzQ0OSwiYWNjZXNzX2xldmVsIjoiQURNSU5fVVNFUiIsImlhdCI6MTUyMjQxMzI5MiwiaXNzIjoiamFycyJ9.I5iPwJrPJ4mw-p0WBZxBxPFy4_U_LP0LTKZ9I_zXK7ygDhM30Ob3vIHLcQRzHkc-QoUsbIMr8o-V81s8QsdfN0VKqvEaaLQY67UlEpdTqlIEWYwjlvQFaCP6mgyVIxRXl0DUXu38XnKD54uGiqDBTs27Zg8AZJoPHJFyGg4DN20x4RYtzq02ssXeN21rJrwl6ApgRGaalYomx3fNUZuNEh0Me5oN7k0gGkkVIcKGgmW5Pml1uloN0nuSNCwek-Nd1AuwuMCrpx5S6YqZlROGqTIttwadV4LLU684I32V55tYZBhEQ9zUML68bcRKLtGq7-UlvnggXwf7QO_3_xSsbA"}
* Connection #0 to host localhost left intact
```

### POST /jars/create
Required: auth, title, description, private

Create a new Event endpoint that can be connected to by Webcaster clients

```
$ curl -vd"auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1MjI0OTk2OTIsInN1YiI6NzQ0OSwiYWNjZXNzX2xldmVsIjoiQURNSU5fVVNFUiIsImlhdCI6MTUyMjQxMzI5MiwiaXNzIjoiamFycyJ9.I5iPwJrPJ4mw-p0WBZxBxPFy4_U_LP0LTKZ9I_zXK7ygDhM30Ob3vIHLcQRzHkc-QoUsbIMr8o-V81s8QsdfN0VKqvEaaLQY67UlEpdTqlIEWYwjlvQFaCP6mgyVIxRXl0DUXu38XnKD54uGiqDBTs27Zg8AZJoPHJFyGg4DN20x4RYtzq02ssXeN21rJrwl6ApgRGaalYomx3fNUZuNEh0Me5oN7k0gGkkVIcKGgmW5Pml1uloN0nuSNCwek-Nd1AuwuMCrpx5S6YqZlROGqTIttwadV4LLU684I32V55tYZBhEQ9zUML68bcRKLtGq7-UlvnggXwf7QO_3_xSsbA&title=MyEventTitle&description=MyEventDescription&private=true" http://localhost:8888/jars/create
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/create HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 564
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 564 out of 564 bytes
< HTTP/1.1 201 Created
< Date: Fri, 30 Mar 2018 12:35:59 GMT
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Content-Length: 53
<
{"event_id": "5e0b9230-086c-406f-a26c-13ff3a8d3880"}
* Connection #0 to host localhost left intact
```


### POST /jars/connect
Required: auth, mount

Validates the given auth is allowed to connect to this mount point. Users are
able to connect to mounts they created, Admins can connect to any mount point.

If successful, marks the connection as connected and logs last connected user.

```
$ curl -vd"auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1MjI0OTk2OTIsInN1YiI6NzQ0OSwiYWNjZXNzX2xldmVsIjoiQURNSU5fVVNFUiIsImlhdCI6MTUyMjQxMzI5MiwiaXNzIjoiamFycyJ9.I5iPwJrPJ4mw-p0WBZxBxPFy4_U_LP0LTKZ9I_zXK7ygDhM30Ob3
vIHLcQRzHkc-QoUsbIMr8o-V81s8QsdfN0VKqvEaaLQY67UlEpdTqlIEWYwjlvQFaCP6mgyVIxRXl0DUXu38XnKD54uGiqDBTs27Zg8AZJoPHJFyGg4DN20x4RYtzq02ssXeN21rJrwl6ApgRGaalYomx3fNUZuNEh0Me5oN7k0gGkkVIcKGgmW5Pml1uloN0nuSNCwek-Nd1AuwuMCrpx5S6YqZlROGqTIttwadV4LLU
684I32V55tYZBhEQ9zUML68bcRKLtGq7-UlvnggXwf7QO_3_xSsbA&mount=5e0b9230-086c-406f-a26c-13ff3a8d3880" http://localhost:8888/jars/connect
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/connect HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 544
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 544 out of 544 bytes
< HTTP/1.1 202 Accepted
< Date: Fri, 30 Mar 2018 12:39:37 GMT
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Content-Length: 0
<
* Connection #0 to host localhost left intact
```

Possible error responses
------------------------
Note that current jars returns a 500 for all failure modes, even ones where the
client is at fault.


### NoUserException
The user credentials provided do not correspond to an account in MyRadio.

```
$ curl -vd"user=lpw503&password=not_my_password" http://localhost:8888/jars/token
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/token HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 36
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 36 out of 36 bytes
< HTTP/1.1 500 Internal Server Error
< Date: Fri, 30 Mar 2018 12:41:23 GMT
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Content-Length: 29
<
{"error": "NoUserException"}
* Connection #0 to host localhost left intact
```

### NoUserPermissionException
User has neither of the 'OB User' or 'OB Admin' permissions in MyRadio.

```
$ curl -vd"user=lpw503&password=my_password" http://localhost:8888/jars/token
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/token HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 31
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 32 out of 32 bytes
< HTTP/1.1 500 Internal Server Error
< Server: TornadoServer/5.0.1
< Date: Fri, 30 Mar 2018 12:45:36 GMT
< Content-Type: text/html; charset=UTF-8
< Content-Length: 39
<
{"error": "NoUserPermissionException"}
* Connection #0 to host localhost left intact
```

### MyRadioServiceFailureException
MyRadio is sad today, or jars is misconfigured.

```
$ curl -vd"user=lpw503&password=my_password" http://localhost:8888/jars/token
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/token HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 32
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 32 out of 32 bytes
< HTTP/1.1 500 Internal Server Error
< Server: TornadoServer/5.0.1
< Content-Type: text/html; charset=UTF-8
< Date: Fri, 30 Mar 2018 12:44:36 GMT
< Content-Length: 44
<
{"error": "MyRadioServiceFailureException"}
* Connection #0 to host localhost left intact
```

### InvalidIdentifierException
The event_id provided is not a v4 UUID.

```
$ curl -vd"auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1MjI0OTk2OTIsInN1YiI6NzQ0OSwiYWNjZXNzX2xldmVsIjoiQURNSU5fVVNFUiIsImlhdCI6MTUyMjQxMzI5MiwiaXNzIjoiamFycyJ9.I5iPwJrPJ4mw-p0WBZxBxPFy4_U_LP0LTKZ9I_zXK7ygDhM30Ob3vIHLcQRzHkc-QoUsbIMr8o-V81s8QsdfN0VKqvEaaLQY67UlEpdTqlIEWYwjlvQFaCP6mgyVIxRXl0DUXu38XnKD54uGiqDBTs27Zg8AZJoPHJFyGg4DN20x4RYtzq02ssXeN21rJrwl6ApgRGaalYomx3fNUZuNEh0Me5oN7k0gGkkVIcKGgmW5Pml1uloN0nuSNCwek-Nd1AuwuMCrpx5S6YqZlROGqTIttwadV4LLU684I32V55tYZBhEQ9zUML68bcRKLtGq7-UlvnggXwf7QO_3_xSsbA&mount=i-love-lamp" http://localhost:8888/jars/connect
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/connect HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 519
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 519 out of 519 bytes
< HTTP/1.1 500 Internal Server Error
< Server: TornadoServer/5.0.1
< Date: Fri, 30 Mar 2018 12:47:38 GMT
< Content-Type: text/html; charset=UTF-8
< Content-Length: 40
<
{"error": "InvalidIdentifierException"}
* Connection #0 to host localhost left intact
```

### NonExistentOrExpiredEventException
The event_id is of a valid format, but the event either does not exist, or has
expired. Events by default last for 10 days before expiring.

```
$ curl -vd"auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1MjI0OTk2OTIsInN1YiI6NzQ0OSwiYWNjZXNzX2xldmVsIjoiQURNSU5fVVNFUiIsImlhdCI6MTUyMjQxMzI5MiwiaXNzIjoiamFycyJ9.I5iPwJrPJ4mw-p0WBZxBxPFy4_U_LP0LTKZ9I_zXK7ygDhM30Ob3vIHLcQRzHkc-QoUsbIMr8o-V81s8QsdfN0VKqvEaaLQY67UlEpdTqlIEWYwjlvQFaCP6mgyVIxRXl0DUXu38XnKD54uGiqDBTs27Zg8AZJoPHJFyGg4DN20x4RYtzq02ssXeN21rJrwl6ApgRGaalYomx3fNUZuNEh0Me5oN7k0gGkkVIcKGgmW5Pml1uloN0nuSNCwek-Nd1AuwuMCrpx5S6YqZlROGqTIttwadV4LLU684I32V55tYZBhEQ9zUML68bcRKLtGq7-UlvnggXwf7QO_3_xSsbA&mount=5e0b9230-086c-406f-a26c-13ff3a8d3881" http://localhost:8888/jars/connect
*   Trying ::1...
* Connected to localhost (::1) port 8888 (#0)
> POST /jars/connect HTTP/1.1
> Host: localhost:8888
> Accept: */*
> Content-Length: 544
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 544 out of 544 bytes
< HTTP/1.1 500 Internal Server Error
< Server: TornadoServer/5.0.1
< Date: Fri, 30 Mar 2018 12:48:48 GMT
< Content-Type: text/html; charset=UTF-8
< Content-Length: 48
<
{"error": "NonExistentOrExpiredEventException"}
* Connection #0 to host localhost left intact
```

### UnauthorizedConnectionException
The event exists, but this user is not authorised to connect to it.

### Others
Various built-in exceptions may also be issued. The response will always be of
the form {"error": "ExceptionName"}. For example, a JWT library is used which
automatically validates JWTs. If these are invalid, or are expired etc, then
this will surface as an exception such as jwt.exceptions.ExpiredSignatureError.

Webcaster Endpoints
-------------------
Actual webcasting is out of the scope of this project. However, there is a
companion to this, webcaster-relay, which implements the webccast protocol,
validates the connection against a jars service, then relays the stream to
an icecast server.

TODOs
-----
- API endpoint to list all/running events
- Return better status codes (4xx for invalid events/credentials etc)
