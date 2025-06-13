import logging

#############
## Logging ##
#############

logger = logging.getLogger(__package__)
logger.propagate = False
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('HELIOS.%(levelname)-7s [%(filename)20s:%(lineno)-4d] %(message)s'))
    logger.addHandler(stream_handler)
