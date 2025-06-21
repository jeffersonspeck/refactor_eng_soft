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
from typing import Iterable
from pathlib import Path

def write_pokemon_csv(pokemons: Iterable, path: str | Path) -> int:
    """
    [PT-BR] Grava a lista de objetos Pokemon em um CSV.
    [EN]    Writes the given Pokemon list to a CSV file.

    Retorna / Returns:
        int: quantidade de linhas efetivamente gravadas.
    """
    pokemons = list(pokemons)  # caso seja generator
    if not pokemons:
        logging.warning("Empty Pokémon list: nothing to write.")
        return 0

    fieldnames = sorted({k for p in pokemons for k in p.to_dict().keys()})
    written = 0

    with open(path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for p in pokemons:
            row = {
                k: (v.replace("\n", " ").strip() if isinstance(v, str) else v)
                for k, v in p.to_dict().items()
            }
            if all(v in (None, "", "0") for v in row.values()):
                logging.warning("Row skipped—almost empty: %s", row)
                continue
            writer.writerow(row)
            written += 1

    logging.info("%d Pokémon exported to '%s'.", written, path)    
    return written
