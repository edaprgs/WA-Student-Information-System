# defined environment variables
# centralized place for storing configuration settings as environment variables
from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")
cloud_name = getenv("cloud_name")
api_key = getenv("api_key")
api_secret = getenv("api_secret")