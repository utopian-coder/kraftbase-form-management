import os
from dotenv import dotenv_values


def get_env(is_local: bool, dir: str):
    """ Get the environment variables

    Args:
        is_local (bool): If the environment is local
        dir (str): The directory path

    Returns:
        dict[str, str | None]: The environment variables
    """
    return dotenv_values(os.path.join(dir, ".env")) if is_local else os.environ
