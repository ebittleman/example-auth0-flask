from os import environ as env

from auth0_flask.app import app

port = env.get("PORT", 8080) or 8080
if not isinstance(port, int):
    port = int(port)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
