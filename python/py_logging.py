import logging
from .py_time import get_time
def setLogging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=f"log/{get_time()}.log",
        filemode='w',
        level=logging.INFO
    )
    logging.info("SET LOGGING")