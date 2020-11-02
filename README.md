# RUCS (R)emote (U)ser (C)ontrol (S)ervice

## exercise: control home automation JSON file

**current status**

- while the http api is functional with curl or postman,
browser based web clients do not fetch data because of
http headers requirements (todo: set header values in server
response)

- while the uwsgi server process loads the service
successfully when loaded manually from its container, this
doesn't work when loaded from the Dockerfile.

- while logging / debugging data appears in the terminals -
mongodb and docker to the tty to which docker-compose
is attached, and the Python and uwsgi to the tty where
the container of the rucs_api docker service is attached -
however, logging support needs to be added

- testing - unit and endpoint tests to be created

- to add swagger documentation


### to start

- the app bind to port 8080, if that is busy, to
change it in _docker-compose.yml_

- `RUCS_DEMO=on docker-compose up`

- (after a fix, it would be possib to remove this step)
enter the container `docker-compose exec rucs_api /bin/bash`,
load the web service `./uwsgi-ini`

- in a web browser with JavaScript, to go to the
path _/rucs/_ (for eg. _localhost:8080/rucs/_)

### description of the remote user control service

http api:

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

### non technical summary

exercise in web development: the state of a house
includes the on/off state of some lighting units and a
thermostat. The exercise is to build the web
service that communicates with the remote user.
A sepparate web service (not built here),
would control the house (for ex. "internet of
things" protocols).

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
the use case, but even for a demo app, demo user
authentication
should be used. But the most critical, common part
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
can be unset if a new use case (non demo) is to
be developed.
