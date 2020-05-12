import os
basedir = os.path.abspath(os.path.dirname(__file__))

auth0_config = {
    "AUTH0_DOMAIN" : "fishhouse.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "casting"
}