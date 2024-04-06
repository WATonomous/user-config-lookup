# user-config-lookup

## Local Setup

Get all users from the WATO infra config (code example below) and direct the
output to `user_directory.json`. Place the file in the root of this repo,
under the path `./data/user_directory.json`

```py
# see infra config repo for examples of how to use `get_all_users`
import get_all_users
import json
print(json.dumps(get_all_users(), sort_keys=True))
```

Note that an env file is also required to run the app locally.
It should look like the example below and be placed in `./.env`.

```
EMAIL_ADDRESS=<EMAIL>
EMAIL_PASSWORD=<PASSWORD>
SENTRY_DSN=<DSN>
```

The values of these variables can be found in the WATO infra config.

## Running the program

Running the container:

```bash
docker compose up --build
```

Stopping the container:

```bash
docker compose down
```

Make sure to forward the port `5500` from the VM to your local computer!
