import logging
import os

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"

if "ACCESS_TOKEN_EXPIRE_MINUTES" not in os.environ:
    logger.critical(
        "ACCESS_TOKEN_EXPIRE_MINUTES environment variable not set, using the its default value."
    )
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
except ValueError:
    # Handle the exception
    raise Exception(
        "ACCESS_TOKEN_EXPIRE_MINUTES environment variable must be an integer."
    )

if "SECRET_KEY" not in os.environ:
    logger.critical(
        "SECRET_KEY environment variable not set, using the its default value, this is a security risk."
    )
    # set the secret key environment variable, in real application it will be set directly by the system
    # to get a string like this run: openssl rand -hex 32
    os.environ[
        "SECRET_KEY"
    ] = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
SECRET_KEY = os.getenv("SECRET_KEY")

if "DATABASE_CONNECTION_STRING" not in os.environ:
    logger.info(
        "DATABASE_CONNECTION_STRING environment variable not set, using the its default value."
    )
    os.environ["DATABASE_CONNECTION_STRING"] = "sqlite:///./database.db"
DATABASE_CONNECTION_STRING = os.environ["DATABASE_CONNECTION_STRING"]
