# user-config-lookup

## Running the program

Running the container:

```bash
export PROJECT_NAME=user_config_lookup$(whoami) \
&& docker build -t user_config_lookup . \
&& docker run --name $PROJECT_NAME -p 5500:5500 user_config_lookup
```

Make sure to forward the port `5500` from the VM to your local computer!
