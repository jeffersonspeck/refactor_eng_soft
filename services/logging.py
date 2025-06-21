import logging
import os

def setup_logging(log_file: str = "logs/errors.txt", console_level=logging.INFO, file_level=logging.DEBUG):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler de arquivo
    f_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    f_handler.setLevel(file_level)

    # Handler de console #comentado o de console
    # c_handler = logging.StreamHandler()
    # c_handler.setLevel(console_level)

    fmt = logging.Formatter("%(asctime)s - %(levelname)-8s - %(name)s - %(message)s")
    f_handler.setFormatter(fmt)
    # c_handler.setFormatter(fmt) #comentado o de console

    logger.addHandler(f_handler)
    # logger.addHandler(c_handler) #comentado o de console