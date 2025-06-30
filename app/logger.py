# app/logger.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    # Crear un logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Evitar duplicar handlers si ya están configurados
    if logger.hasHandlers():
        logger.handlers.clear()

    # Crear un handler para la consola y establecer el formato JSON
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    log_handler.setFormatter(formatter)

    # Añadir el handler al logger
    logger.addHandler(log_handler)
