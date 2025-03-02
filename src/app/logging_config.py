import logging
from config import config

logging.basicConfig(
    level=config["logging"]["level"],
    format=config["logging"]["format"],
    datefmt=config["logging"]["datefmt"],
)
logger = logging.getLogger(__name__)
