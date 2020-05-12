# Udacity Full Stack Developer Capstone
This is my capstone project for Udacity's Full Stack Nanodegree Program. This project creates the backbone for a casting agency's application. In it, employees - depending on their role - can view, add, update or delete and actor from the database.
https://central-casting.herokuapp.com

## Tech Stack
This API covers the topics:
* Data modeling with Postgres and SQLAlchemy
* Crud operation with Flask
* Authentication with Auth0
* Testing with Unittest and Postman
* Deployment on Heroku

## Models
### Movies
* __id:__ an auto-incrementing integer
* __title:__ string
* __genre:__ string
* __release_date:__ string

### Actors
* __id:__ an auto-incrementing integer
* __name:__ string
* __gender:__ string
* __birthdate:__ string

## API
In order to use the API users need to be authenticated. 
### Roles (per project rubric)
* __Cassting Assistant:__
    * Can view actors and movies.
* __Casting Director:__
    * All permissions a Casting Assistant has and…
    * Add or delete an actor from the database
    * Modify actors or movies.
* __Executive Producer:__
    * All permissions a Casting Director has and…
    * Add or delete a movie from the database.

## Setting Up Authorization
For Authentication, users must sign in with Auth0. To run this application, create an account with Auth0 (https://auth0.com).
In Auth0, create a new web application. Copy your domain into AUTH0_DOMAIN in config.py.
Create a new API. Copy the identifier into API_AUDIENCE in config.py.
Enable RBAC and Add permissions in the access token and save settings.
Still in API, go to permissions and create these permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
Go to Users and Roles and create roles for Producer, Director and Assistant.
For each of these roles, add permissions as follows:
    - Casting Assistant
        - can   - `get:actors`
                - `get:movies`
    - Casting Director
        - can   - `get:actors`
                - `post:actors`
                - `patch:actors`
                - `delete:actors`
                - `get:movies`
                - `patch:movies`
    - Executive Producer
        - can   - `get:actors`
                - `get:movies`
                - `post:movies`
                - `delete:movies`
Register three users and assign them each a role.
Your users can sign in using a url like this:
```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```
After the user is logged in, you can get the acces token from the callback url between '#access_token=' and '&expires_in'

When testing locally, you'll need the set the bearer tokens as environment variables by running:
```
export ASSISTANT="Bearer <INSERT_YOUR_TOKEN>"
export DIRECTOR="Bearer <INSERT_YOUR_TOKEN>"
export PRODUCER="Bearer <INSERT_YOUR_TOKEN>"
```
Alternatively, you can use Postman (https://www.postman.com/).

### Endpoints
__Get__`/movies`
Retreives an array of current movies in the database.
__Get__`/actors`
Retreives an array of current actors in the database.
```
curl -X GET https://central-casting.herokuapp.com/movies \
-H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```
__Post__`/movies`
Adds a movie to the database.
__Post__`/actors`
Adds an actor to the database.

```
curl -X POST https://central-casting.herokuapp.com/actors \
-H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Jane Doe",
    "gender": "Female",
    "birthdate": "2002/04/27"
}'
```
__Patch__`/movies`
Updates a movie in the database.
__Patch__`/actors`
Udates an actor in the database.

```
curl -X PATCH https://central-casting.herokuapp.com/actors/1 \
-H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Jane Q Public",
}'
```
__Delete__`/movies`
Deletes a movie from the database.
__Delet__`/actors`
Deletes an actor from the database.

```
curl -X Patch https://central-casting.herokuapp.com/actors/1 \
-H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

## Installation
This section explains how to run the project locally.

### Python 3.7.6
This project requires Python3.7.6. 

### Virtual Environment
Using a virtual environment is recommended. See the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for instructions on setting up a virtual environment on your platform.

### Intall Dependancies
Once your virtual environemt is running, install the dependancies by navigating to the project directory and running:
```bash
pip install -r requirements.txt
```

### Create the Database
With postgres running, create the database
```
createdb casting
```
### Run the server
To run the server, open app.py and execute:
``` 
python app.py
```
### Testing
You can test the live endpoints with the included postman collection.
To run testing locally, first create a test database 
With postgres running, create the database
```
createdb casting_test
```
