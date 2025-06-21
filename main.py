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
import csv
import logging
import os
from pathlib import Path

from dotenv import load_dotenv # type: ignore

from services.pokemon_crawler import PokemonCrawler
from services.quests import QuestPokemon
from services.logging import setup_logging
from services.csv_analyzer import PokemonCSVAnalyzer
from services.csv_writer import write_pokemon_csv # type: ignore   

# ---------------------------------------------------------------------------
# [PT-BR] Configuração da aplicação 
# [EN]    Application setup
# ---------------------------------------------------------------------------

# [PT-BR] Carrega variáveis do arquivo .env (na raiz do projeto)
# [EN]   Loads variables from the .env file (located at the project root)
load_dotenv()

START_PAGE: str = os.getenv(
    "START_PAGE", "https://pokemythology.net/conteudo/pokemon/lista01.htm"
)
OUTPUT_FILE: str = os.getenv("OUTPUT_FILE", "output/pokemons.csv")

# [PT-BR] Garante que a pasta de saída exista
# [EN]   Ensures that the output folder exists
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

# [PT-BR] Configura logging (arquivo + console)
# [EN]   Configures logging (file + console)
setup_logging()

# ----------------------------------------------------------------------------
# [PT-BR] Função principal que orquestra o fluxo completo do programa.
# [EN]   Main function that orchestrates the full program flow.
# ----------------------------------------------------------------------------
def main() -> None:
    """
    [PT-BR] Fluxo principal de execução.
    [EN] Main execution flow.
    """
    # [PT-BR] Descoberta de páginas a partir da página inicial
    # [EN]   Discover sub-pages starting from the initial page
    urls = PokemonCrawler.discover_pages(START_PAGE)
    if START_PAGE not in urls:
        urls.insert(0, START_PAGE)

    print(f"{len(urls)} pages found. Starting capture…")
    all_pokemons = []

    # [PT-BR] Itera sobre cada URL coletada
    # [EN]   Iterates over each collected URL
    for url in urls:
        logging.info("Crawling Pokémon from: %s", url)

        # [PT-BR] Exemplo de uso da classe QuestPokemon com texto lúdico no console
        # [EN] Example usage of the QuestPokemon class with playful text in the console
        print(QuestPokemon(url).generate_description())

        try:
            pokemons = PokemonCrawler(url).crawl()
            all_pokemons.extend(pokemons)
            print(f"  + {len(pokemons)} Pokémon captured on this page.\n")
            logging.info("  + %d Pokémon captured on this page.", len(pokemons))
        except Exception:
            logging.error("Failed to process %s", url, exc_info=True)

    if not all_pokemons:
        logging.warning("No Pokémon captured.")
        return

    # -----------------------------------------------------------------------------
    # [PT-BR] Escrita do CSV consolidado
    # [EN] Writing the consolidated CSV
    # -----------------------------------------------------------------------------
    written = write_pokemon_csv(all_pokemons, OUTPUT_FILE)
    print(f"\n{written} Pokémon exported to '{OUTPUT_FILE}'.")    

    # -------------------------------------------------------------------------------------
    # [PT-BR] Análise opcional do CSV contendo estatísticas e consistência, gravada no log
    # [EN] Optional CSV analysis with statistics and consistency check, logged
    # --------------------------------------------------------------------------------------
    PokemonCSVAnalyzer(OUTPUT_FILE).run_full_report()

# ---------------------------------------------------------------------------
# [PT-BR] Execução direta
# [EN] Direct execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()