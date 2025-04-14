import logging
import sys
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("sherpa")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler("logs/sherpa.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
