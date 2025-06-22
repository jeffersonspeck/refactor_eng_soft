"""
Módulo main.py
==============

[PT-BR]
Ponto de entrada para o sistema de captura de dados Pokémon.

Fluxo principal:
1. Carrega variáveis de configuração do arquivo ``.env`` (START_PAGE, OUTPUT_FILE).
2. Configura sistema de logging.
3. Descobre todas as páginas de listagem de Pokémon a partir da página inicial.
4. Faz o *crawl* de cada página, parseia as tabelas e cria objetos ``Pokemon``.
5. Exporta o conjunto consolidado para um CSV.
6. Executa uma análise opcional do CSV gerado.

Variáveis de ambiente esperadas (definidas em ``.env``):
    START_PAGE   URL da página inicial a ser rastreada.
    OUTPUT_FILE  Caminho do arquivo CSV de saída.

[EN]
Entry point for the Pokémon data capture system.

Main flow:
1. Loads configuration variables from the ``.env`` file (START_PAGE, OUTPUT_FILE).
2. Sets up the logging system.
3. Discovers all Pokémon listing pages starting from the initial one.
4. Crawls each page, parses the tables, and creates ``Pokemon`` objects.
5. Exports the consolidated data to a CSV file.
6. Optionally runs an analysis of the generated CSV.

Expected environment variables (defined in ``.env``):
    START_PAGE   Initial page URL to be crawled.
    OUTPUT_FILE  Output CSV file path.

Usage:
    $ python main.py
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv  # type: ignore

from services.pokemon_crawler import PokemonCrawler
from services.quests import QuestPokemon
from services.logging import setup_logging
from services.csv_writer import write_pokemon_csv  # type: ignore
from services.csv_analyzer import PokemonCSVAnalyzer

# ----------------------------------------------------------------------------
# [PT-BR] Carregamento de variáveis de ambiente e preparação de pastas
# [EN]   Load environment variables and prepare folders
# ----------------------------------------------------------------------------

load_dotenv()
START_PAGE: str = os.getenv(
    "START_PAGE", "https://pokemythology.net/conteudo/pokemon/lista01.htm"
)
OUTPUT_FILE: str = os.getenv("OUTPUT_FILE", "output/pokemons.csv")
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------
# [PT-BR] Descobre todas as páginas a partir da página inicial
# [EN]   Discover all listing pages from the start page
# ----------------------------------------------------------------------------
def discover_urls(start_url: str) -> list[str]:
    urls = PokemonCrawler.discover_pages(start_url)
    if start_url not in urls:
        urls.insert(0, start_url)
    return urls


# ----------------------------------------------------------------------------
# [PT-BR] Realiza o crawling de todas as páginas e retorna a lista consolidada
# [EN]   Crawls all discovered pages and returns the consolidated list
# ----------------------------------------------------------------------------
def crawl_all_pages(urls: list[str]) -> list[dict]:
    all_pokemons = []
    for url in urls:
        logging.info("Crawling Pokémon from: %s", url)
        print(print(QuestPokemon(url).to_text()))

        try:
            pokemons = PokemonCrawler(url).crawl()
            all_pokemons.extend(pokemons)
            print(f"  + {len(pokemons)} Pokémon captured on this page.\n")
            logging.info("  + %d Pokémon captured on this page.", len(pokemons))
        except Exception:
            logging.error("Failed to process %s", url, exc_info=True)
    return all_pokemons


# ----------------------------------------------------------------------------
# [PT-BR] Função principal
# [EN]   Main function
# ----------------------------------------------------------------------------
def main() -> None:
    setup_logging()
    urls = discover_urls(START_PAGE)
    print(f"{len(urls)} pages found. Starting capture…")

    all_pokemons = crawl_all_pages(urls)

    if not all_pokemons:
        logging.warning("No Pokémon captured.")
        return

    written = write_pokemon_csv(all_pokemons, OUTPUT_FILE)
    print(f"\n{written} Pokémon exported to '{OUTPUT_FILE}'.")

    PokemonCSVAnalyzer(OUTPUT_FILE).run_full_report()


# ----------------------------------------------------------------------------
# [PT-BR] Execução direta
# [EN]   Direct execution
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()