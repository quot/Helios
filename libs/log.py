import logging

#############
## Logging

log = logging.getLogger(__package__)
log.propagate = False
log.setLevel(logging.DEBUG)

if not log.hasHandlers():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('HELIOS.%(levelname)-7s [%(filename)20s:%(lineno)-4d] %(message)s'))
    log.addHandler(stream_handler)
