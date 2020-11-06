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

**current status: in development**

- next development objectives:

    1. to document demo routes
 
    2. implement unit testing testing and logging.
      - while logging / debugging data appears in the 
      the tty to which docker-compose
      is attached -
      however, it remains to support logging

    3. Swagger documentation


### to start:

- the app bind to port 8080, if that is busy, to
change it in _docker-compose.yml_

- `RUCS_DEMO=on docker-compose up`

- in a web browser with JavaScript, to go to the
path _/rucs/_ (for eg. _localhost:8080/rucs/_)

- _note_: if the domain is not localhost, please set
the constant `domain` in httpd/content/index.js, to the
correct value

### technical description

#### demo endpoints

the purpose of the demo REST endpoints _/rucs/demo/*_ 
is to supply access control sufficient for a production demo -
a 512 bit token that is accessible from the server
(at the current configuration, it's printed to the stdout of the
docker-compose process) - the demo module is controlled
by the _RUCS\_DEMO_ environment variable to _docker\_compose_,
so it can be "unplugged" when multiuser support is developed

- /rucs/demo/set_token

  - request: `{"house_id": TOKEN}`

     the TOKEN accessible from the server

  - response: includes a "set-cookie" header with the token


#### endpoints of the RUCS service

- access control: the access control moduel is a stub, it
  it suitable for a production level demo - a 512 bit key
  accessible in the server, is secure in a SSL encripted
  deployment, it's stored in a cookie with the Http-only flag.

- /rucs/ method: GET

  - request data: none

  - response data: complete house state document

```
    { "thermostat": val, "lighting":

        [{"id": x, "on_state": x, "label": x }]

   }
```

- /rucs/ methods PUSH, PUT, DELETE

  - for now, see descriptions at individual _rucs\_router.py_ sections 

document based (Mongo DB) model:

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
