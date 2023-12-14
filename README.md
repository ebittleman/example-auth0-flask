# Auth0 Flask

Quick example application that uses server side authorization code OAuth2 grant. It also has a small extension to the `authlib` to support Auth0's usage of the `audience` argument on the Authorization URL

## Instructions

**Install** python 3.8 or greater

**Copy** `.env.example` to `.env` and fill out the configuration

**Run**

```shell
pip install poetry
poetry install
poetry run python -m auth0_flask
```

**Visit** http://localhost:8080/home

**Login**
