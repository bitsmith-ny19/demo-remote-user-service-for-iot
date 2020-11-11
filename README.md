# RUCS (R)emote (U)ser (C)ontrol (S)ervice

## exercise: control home automation JSON file

### non technical summary

The state of a house
includes the on/off state of some lighting units and a
thermostat. The exercise is to build the web
service that communicates with the remote user.
A sepparate web service (not built here),
would control the house (for ex. "internet of
things" protocols).

A demo client for html browsers with JavaScript enabled is
included, accessible at the root url.
This is not purposed to demonstrate front-end skill
of the contributors, instead, it is minimal, and the only purpose
is for
convenience of who would like to preview the
functionality in 1 minute, instead of tools such
as curl or postman.

### to start:

1. `RUCS_DEMO=set docker-compose up` (to configure domain or
   port see note bellow)

The RUCS endpoints should now be accessible as documented bellow, and
the openapi spec at the endpoint _/rucs/spec_.

To allow "instant preview" instead of curl or postman requests:

2. in a web browser with a JavaScript interpreter, to go to the
   path _/rucs/_ (for eg. _localhost:8080/rucs/_)

3. the 12 digit access token is printed to the _docker\_compose_
   output in a line that starts in _**** DEMO TOKEN_
   (it's regenerated every time that the container is restarted).

_note_: to modify port or domain -
default domain is localhost, default port is 8080.
These values are configured in the `domain` and `port`
constant in the script _httpd/content/index.js_. The port
would also need to be set in the `services.httpd.ports`
key in the Docker compose file.

### technical description

#### demo endpoint

To enable the demo , set
the _RUCS\_DEMO_ environment variable to the _docker\_compose_ command
to a string that is not null.

- /rucs/demo/set_token

  - description: allows that the server would set the cookie. The
    purpose is to secure the access token in the case that the client
    of the demo service runs in a general use web browser.
    The security level is the
    isolation of the access token from the scope of scripts
    by the http-only flag
    (http-only - issue #2).

  - request: `{"house_id": TOKEN}`

    the access TOKEN is accessible from the server. It is printed in
    the _docker-compose_ tty in a
    line that starts in _**** DEMO TOKEN_

  - response: includes a "set-cookie" header with the token

#### endpoints of the RUCS service

the openapi specification of the service is accessible
at the endpoint _/rucs/spec_ as well as in the docstrings
in the source file _rucs/views.py_.

- access control: the access control module is a stub, it
  it suitable for a production level demo - a 384 bit key
  accessible in the server, would be secured in a SSL encripted
  deployment, it's required in all RUCS service endpoints in the
  cookie header with the Http-only flag set
  (http-only: issue #2).

- /rucs/ method: GET

  - request data: none

  - response data: complete house state document

```
    { "thermostat": val, "lighting":

        [{"id": x, "on_state": x, "label": x }]

   }
```

- /rucs/ methods PUSH, PUT, DELETE

  - see the openapi spec at _/rucs/spec_ or in the docstrings
    in _rucs/views.py_

#### document based (Mongo DB) model:

- house collection:

  - id: Mongo object id field

  - thermostat: Float field

  - lighting: list field of type lighting embedded document

- lighting embedded document:

  - id: Integer

  - label: String field

  - is_on: boolean field

### non technical design reasoning

As suggested in the description of the exercise
(not included in this repository), the interface between the
remote user control service
and the house control is a JSON file,
in this implementation, this is extended to a
Mongo document.

The demo web service includes a demo web page
and a demo house state. The infrastructure is
scalable - it includes a Docker
network with Mongo, Python Flask and Nginx
http server containers that could be used
by devops with Docker Swarm or other distributed
system.

As suggested by the guidelines, the demo focuses on
the development as close as possible to production
on the most critical components. Multi user support
and authentication method would depend on
the use case, but even for a demo app, of course
sufficient access control is required.
But the most critical, common part
is the part of the service that reads and controls
the house state (that data would be the interface with
a sepparate web service that controls the house,
as mentioned before). This conclusion was based as well
on the description of the exercise. In that description,
the the concrete specifications are:

- get/post/put support
for house lighting units

- get/put thermostat value

- logging

- web page demo

It should be scalable so that
it can adapt to the usage levels, as well as modular
so that more components such as user model and
appropriate authentication control can be added
without the need to change the existing components
of the service. Not less critical to development
is that it is accessible by documentation and
documentation and includes testing for debugging,
quality control, and programming practices.

Based on the observations above, 
multiuser support is not included in the demo -
the authentication controller uses
a mock token and there is a demo house state that is
initialized. For modularity, the demo configuration
is initialized as an environment variable flag that
can be unset if a new use case is to
be developed.

#### contributors

- _bitsmith-ny19_

- _contributor 2_: contributed the original draft of the
demo client,
using mock data. This contribution consists of the files
_index.html_, _index.js_, _index.css_ as they appear in
commit _beed76f_.

#### general comments

This exercise was an assignment for the candidate application
process to a job opening, but later it was taken as a fieldwork
oportunity to implement a
complete example of an isolated
service within the Flask ecosystem.

-- bitsmith, ecosystems engineer
