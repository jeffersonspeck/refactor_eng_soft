#!/usr/bin/env python3
"""
Módulo main.py
======================

Ponto de entrada para o sistema de captura de dados Pokémon.

Fluxo principal:
1. Carrega variáveis de configuração do arquivo ``.env`` (START_PAGE, OUTPUT_FILE).
2. Configura sistema de logging.
3. Descobre todas as páginas de listagem de Pokémon a partir da página inicial.
4. Faz o *crawl* de cada página, parseia as tabelas e cria objetos ``Pokemon``.
5. Exporta o conjunto consolidado para um CSV.
6. Executa uma análise opcional do CSV gerado.

Uso:
    $ python main.py

Variáveis de ambiente esperadas (definidas em ``.env``):
    START_PAGE   URL da página inicial a ser rastreada.
    OUTPUT_FILE  Caminho do arquivo CSV de saída.
"""
import csv
import logging
import os
from pathlib import Path

from dotenv import load_dotenv # type: ignore

from services.pokemon_crawler import PokemonCrawler
from services.quests import QuestPokemon
from services.logging import setup_logging
from services.csv_analyzer import PokemonCSVAnalyzer

# ---------------------------------------------------------------------------
# Configuração da aplicação
# ---------------------------------------------------------------------------

# Carrega variáveis do arquivo .env (na raiz do projeto)
load_dotenv()

START_PAGE: str = os.getenv(
    "START_PAGE", "https://pokemythology.net/conteudo/pokemon/lista01.htm"
)
OUTPUT_FILE: str = os.getenv("OUTPUT_FILE", "output/pokemons.csv")

# Garante que a pasta de saída exista
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

# Configura logging (arquivo + console)
setup_logging()
#-----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Função principal
# ----------------------------------------------------------------------------
def main() -> None:
    """Fluxo principal de execução."""

    # Descoberta de páginas a partir da página inicial
    urls = PokemonCrawler.discover_pages(START_PAGE)
    if START_PAGE not in urls:
        urls.insert(0, START_PAGE)

    print(f"{len(urls)} pages found. Starting capture…")
    all_pokemons = []

    # Itera sobre cada URL coletada
    for url in urls:
        logging.info("Crawling Pokémon from: %s", url)

        # Exemplo de uso da classe QuestPokemon com texto lúdico no console
        print(QuestPokemon(url).generate_description())

        try:
            pokemons = PokemonCrawler(url).crawl()
            all_pokemons.extend(pokemons)
            print(f"  + {len(pokemons)} Pokémon captured on this page.\n")
            logging.info("  + %d Pokémon captured on this page.", len(pokemons))
        except Exception:  # pylint: disable=broad-except
            logging.error("Failed to process %s", url, exc_info=True)

    if not all_pokemons:
        logging.warning("No Pokémon captured.")
        return

    # -----------------------------------------------------------------------------
    # Escrita do CSV consolidado
    # -----------------------------------------------------------------------------
    fieldnames = sorted({k for p in all_pokemons for k in p.to_dict().keys()})
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in all_pokemons:
            row = {
                k: (v.replace("\n", " ").strip() if isinstance(v, str) else v)
                for k, v in p.to_dict().items()
            }
            if all(v in (None, "", "0") for v in row.values()):
                logging.warning("Row skipped—almost empty: %s", row)
                continue
            writer.writerow(row)

    print(f"\n{len(all_pokemons)} Pokémon exported to '{OUTPUT_FILE}'.")
    #------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # Análise opcional do CSV contendo estatísticas e consistência. gravada no log
    # -----------------------------------------------------------------------------
    PokemonCSVAnalyzer(OUTPUT_FILE).run_full_report()

# ---------------------------------------------------------------------------
# Execução direta
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()