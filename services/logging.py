"""
Módulo logging.py
==================

[PT-BR] Módulo de configuração central do sistema de logs. Permite:

- Registro de mensagens em arquivo (.txt) com formatação padronizada;
- Definição de níveis diferentes para log em console e arquivo;
- Criação automática da pasta de logs, se necessário.

[EN] Centralized logging configuration module. Provides:

- Logging to a .txt file with standardized formatting;
- Different logging levels for console and file outputs;
- Automatic creation of the logs directory if it doesn't exist.

Uso / Usage:
    from services.logging import setup_logging
    setup_logging()
"""

import logging
import os

def setup_logging(log_file: str = "logs/errors.txt", console_level=logging.INFO, file_level=logging.DEBUG):
    """
    [PT-BR] Configura o sistema de logging com níveis diferenciados para arquivo e console.
    [EN] Sets up the logging system with different levels for file and console output.
    """
    # [PT-BR] Garante que a pasta de destino exista
    # [EN] Ensures the target directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # [PT-BR] Remove handlers anteriores para evitar duplicidade
    # [EN] Clear previous handlers to avoid duplicate messages
    if logger.hasHandlers():
        logger.handlers.clear()

    # [PT-BR] Handler para salvar em arquivo
    # [EN] File handler
    f_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    f_handler.setLevel(file_level)

    # [PT-BR] Handler de console (desativado por padrão)
    # [EN] Console handler (disabled by default)
    # c_handler = logging.StreamHandler()
    # c_handler.setLevel(console_level)

    fmt = logging.Formatter("%(asctime)s - %(levelname)-8s - %(name)s - %(message)s")
    f_handler.setFormatter(fmt)
    # c_handler.setFormatter(fmt)

    logger.addHandler(f_handler)
    # logger.addHandler(c_handler)