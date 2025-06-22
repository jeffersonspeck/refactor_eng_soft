"""
Módulo csv_writer.py
=====================

[PT-BR]
Função utilitária para gravar listas de objetos ``Pokemon`` em arquivos CSV.
O módulo aplica uma limpeza básica nos dados, removendo quebras de linha e
espaços em excesso, além de pular linhas vazias ou inválidas.

Também registra no log a quantidade de registros exportados e quaisquer
linhas ignoradas por estarem praticamente vazias.

[EN]
Utility function to write lists of ``Pokemon`` objects to CSV files.
The module applies basic data cleaning, removing line breaks and
extra spaces, and skips empty or invalid rows.

It also logs the number of exported records and any skipped entries
due to being nearly empty.

Uso típico / Typical usage:
    from services.csv_writer import write_pokemon_csv

    written = write_pokemon_csv(pokemon_list, "output/pokemons.csv")
    print(f"{written} Pokémon saved.")
"""
import csv
import logging
from typing import Iterable, Protocol, runtime_checkable
from pathlib import Path
from contextlib import suppress

@runtime_checkable
class HasToDict(Protocol):
    def to_dict(self) -> dict[str, object]: ...

def clean_csv_value(value: object) -> object:
    """
    [PT-BR] Limpa valores para escrita em CSV (quebras de linha, espaços).
    [EN] Cleans values for CSV output (line breaks, extra spaces).
    """
    if isinstance(value, str):
        return value.replace("\n", " ").strip()
    return value

def is_effectively_empty(row: dict[str, object]) -> bool:
    """
    [PT-BR] Verifica se a linha está vazia (ignora apenas None ou strings vazias).
    [EN] Checks if the row is effectively empty (ignores None or empty strings).
    """
    return all(v in (None, "") for v in row.values())

def write_pokemon_csv(pokemons: Iterable[HasToDict], path: str | Path, skip_empty: bool = True) -> int:
    """
    [PT-BR] Grava objetos `Pokemon` no CSV, com limpeza básica e validação de linhas.
    [EN] Writes `Pokemon` objects to CSV, with basic cleaning and row validation.

    Parâmetros:
        pokemons (Iterable[HasToDict]): lista de objetos com .to_dict().
        path (str | Path): caminho do arquivo de saída.
        skip_empty (bool): se True, ignora linhas consideradas vazias.

    Retorna:
        int: quantidade de linhas efetivamente gravadas.
    """
    pokemons = list(pokemons)
    if not pokemons:
        logging.warning("Empty Pokémon list: nothing to write.")
        return 0

    try:
        fieldnames = sorted({k for p in pokemons for k in p.to_dict().keys()})
        written = 0

        with open(path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for p in pokemons:
                row = {k: clean_csv_value(v) for k, v in p.to_dict().items()}

                if skip_empty and is_effectively_empty(row):
                    logging.warning("Row skipped—effectively empty: %s", row)
                    continue

                writer.writerow(row)
                written += 1

        logging.info("%d Pokémon exported to '%s'.", written, path)
        return written

    except (IOError, OSError) as e:
        logging.error("Failed to write CSV file '%s': %s", path, str(e), exc_info=True)
        return 0
