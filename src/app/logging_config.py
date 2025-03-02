import logging
import logging.config
from config import config

def setup_logging():
    # Convert string log level from config to numeric value
    log_level = getattr(logging, config["logging"]["level"].upper(), logging.INFO)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": config["logging"]["format"],
                "datefmt": config["logging"]["datefmt"],
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": log_level,
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "standard",
                "level": log_level,
                "filename": "app.log",  # You could also load this from config if needed
            },
        },
        "loggers": {
            "": {  # Root logger configuration
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)

# Set up logging using our configuration
setup_logging()
logger = logging.getLogger(__name__)

# Example usage:
logger.info("Logging has been configured.")
