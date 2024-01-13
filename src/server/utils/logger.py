import logging
import logging.config
import os

import coloredlogs
import yaml


def setup_logging(default_path, default_level=logging.INFO, env_key='LOG_CFG'):
    """
    | **@author:** Prathyush SP
    | Logging Setup
    """
    path = default_path
    logging_environment_variable_was_set = False
    value = os.getenv(env_key, None)
    if value:
        path = value
        logging_environment_variable_was_set = True
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')

    logger = logging.getLogger(__name__)
    if not logging_environment_variable_was_set:
        logger.warning('LOG_CFG environment variable was not set, using the default logging configuration location.')
