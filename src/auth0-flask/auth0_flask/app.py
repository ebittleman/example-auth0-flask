import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_client.apps import FlaskOAuth2App
from authlib.integrations.requests_client.oauth2_session import (
    OAuth2Session as _OAuth2Session,
)
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Initialize Flask
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Extend `authlib` to support `audience`
## START


class Auth0Session(_OAuth2Session):
    EXTRA_AUTHORIZE_PARAMS = ("response_mode", "nonce", "prompt", "login_hint", "audience")


class Auth0App(FlaskOAuth2App):
    client_cls = Auth0Session


class Auth0OAuth(OAuth):
    oauth2_client_cls = Auth0App


## END

# Initialize OAuth2 integration
oauth = Auth0OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email offline_access",
        "audience": env.get("AUTH0_AUDIENCE"),
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Add routes


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@app.route("/", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/home")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/home")
def home():
    return render_template(
        "home.html", session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4)
    )
