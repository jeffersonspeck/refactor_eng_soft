"""
Módulo logging.py
==========

Módulo de configuração central do sistema de logs. Permite:

- Registro de mensagens em arquivo (.txt) com formatação padronizada;
- Definição de níveis diferentes para log em console e arquivo;
- Criação automática da pasta de logs, se necessário.

Uso:
    from services.logging import setup_logging
    setup_logging()
"""
import logging
import os

def setup_logging(log_file: str = "logs/errors.txt", console_level=logging.INFO, file_level=logging.DEBUG):
    # Garante que a pasta de destino exista
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove handlers anteriores para evitar duplicidade
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler para salvar em arquivo
    f_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    f_handler.setLevel(file_level)

    # Handler de console (desativado por padrão)
    # c_handler = logging.StreamHandler()
    # c_handler.setLevel(console_level)

    fmt = logging.Formatter("%(asctime)s - %(levelname)-8s - %(name)s - %(message)s")
    f_handler.setFormatter(fmt)
    # c_handler.setFormatter(fmt)

    logger.addHandler(f_handler)
    # logger.addHandler(c_handler)
