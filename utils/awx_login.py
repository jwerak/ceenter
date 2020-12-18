#!/usr/bin/python3

import sys, json
import base64
import urllib.parse
import urllib.request


def print_help():
    print(
        """
This is simple tool to generate envs for Tower/AWX login.
It expects exactly 3 arguments and prints connection envs to the stdout.
Output can be saved to file and sourced later, e.g. source ~/.awx_conf.env

usage:
awx_login.py <TOWER_HOST> <TOWER_USER> <TOWER_PASSWORD>

awx_login.py <TOWER_HOST> <TOWER_USER> <TOWER_PASSWORD> > ~/.awx_conf.env
"""
    )


def auth(host, username, password):
    request = urllib.request.Request(f"{host}/api/v2/tokens/", method="POST")
    base64_auth = base64.b64encode(f"{username}:{password}".encode())
    base64_string = base64_auth.decode()

    request.add_header(f"Authorization", f"Basic {base64_string}")

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP Error {e.code}: {e.read()}")
    except urllib.error.URLError as e:
        sys.exit(f"URL Error: {e.reason}")

    response_body = response.read()

    try:
        tokens = json.loads(response_body.decode())
    except json.JSONDecodeError as e:
        sys.exit(f"Failed to parse returned json {e.msg}")

    return tokens.get("token", None)


if len(sys.argv) != 4:
    print_help()
    sys.exit(f"Expecting 3 argument, but {len(sys.argv) - 1} were given!")

# Save arguments
awx_host = sys.argv[1]
awx_username = sys.argv[2]
awx_password = sys.argv[3]

awx_token = auth(awx_host, awx_username, awx_password)
if awx_token is None:
    sys.exit("Authentication token not found")

print(
    f"""export TOWER_HOST={awx_host}
export TOWER_VERIFY_SSL=False
export TOWER_USERNAME={awx_username}
export TOWER_OAUTH_TOKEN={awx_token}
"""
)
