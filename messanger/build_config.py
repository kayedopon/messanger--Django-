import json
from getpass import getpass
from django.core.management.utils import get_random_secret_key

def request_info():
    email_host_user = input("Enter your gmail address:\n")
    email_host_password = getpass("Enter your google application password:\n")
    secret_key = get_random_secret_key()

    config = {
        "email_host_user": email_host_user,
        "email_host_password": email_host_password,
        "secret_key": secret_key,
    }

    build_config(config)

def build_config(config):
    json_object = json.dumps(config, indent=4)

    with open("messanger/config.json", "w") as file:
        file.write(json_object)

def main():
    request_info()

if __name__ == "__main__":
    main()
