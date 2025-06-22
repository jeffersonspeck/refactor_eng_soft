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
from typing import Optional

def setup_logging(
    log_file: str = "logs/errors.txt",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    enable_console: bool = True,
    append: bool = False,
    logger_name: Optional[str] = None
) -> logging.Logger:
    """
    [PT-BR] Configura o sistema de logging com opções para arquivo e console.
    [EN] Sets up the logging system with options for file and console.

    Parâmetros / Parameters:
        log_file (str): Caminho para o arquivo de log / Log file path.
        console_level (int): Nível do log para o console / Console log level.
        file_level (int): Nível do log para o arquivo / File log level.
        enable_console (bool): Habilita ou não o log no console / Enable console output.
        append (bool): Se True, adiciona ao arquivo existente / If True, appends to log file.
        logger_name (Optional[str]): Nome do logger / Logger name (None = root logger).

    Retorna / Returns:
        logging.Logger: Instância configurada do logger / Configured logger instance.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    mode = "a" if append else "w"
    f_handler = logging.FileHandler(log_file, mode=mode, encoding="utf-8")
    f_handler.setLevel(file_level)

    fmt = logging.Formatter("%(asctime)s - %(levelname)-8s - %(name)s - %(message)s")
    f_handler.setFormatter(fmt)
    logger.addHandler(f_handler)

    if enable_console:
        c_handler = logging.StreamHandler()
        c_handler.setLevel(console_level)
        c_handler.setFormatter(fmt)
        logger.addHandler(c_handler)

    return logger