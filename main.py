import csv
import logging
import os
from services.pokemon_crawler import PokemonCrawler
from services.quests import QuestPokemon
from services.logging import setup_logging
from services.csv_analyzer import PokemonCSVAnalyzer

START_PAGE  = "https://pokemythology.net/conteudo/pokemon/lista01.htm"
OUTPUT_FILE = "output/pokemons.csv"

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Configure logging once, at the start of the application
setup_logging()

def main() -> None:
    urls = PokemonCrawler.discover_pages(START_PAGE)
    if START_PAGE not in urls:
        urls.insert(0, START_PAGE)

    print(f"{len(urls)} pages found. Starting capture…")
    all_pokemons = []

    for url in urls:
        logging.info("Crawling Pokémon from: %s", url)

        quest = QuestPokemon(url)
        print(quest.generate_description())

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

    # Write CSV
    fieldnames = sorted({k for p in all_pokemons for k in p.to_dict().keys()})
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in all_pokemons:
            row = {k: (v.replace("\n", " ").strip() if isinstance(v, str) else v)
                   for k, v in p.to_dict().items()}
            if all(v in (None, "", "0") for v in row.values()):
                logging.warning("Row skipped—almost empty: %s", row)
                continue
            writer.writerow(row)

    print(f"\n{len(all_pokemons)} Pokémon exported to '{OUTPUT_FILE}'.")

    # Optional: analyze missing columns and log the summary
    analyzer = PokemonCSVAnalyzer(OUTPUT_FILE)
    analyzer.run_full_report()

if __name__ == "__main__":
    main()