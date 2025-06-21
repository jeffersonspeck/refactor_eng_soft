"""
Módulo pokemon_crawler.py
==========================

[PT-BR]
Módulo responsável por varrer ("crawlear") páginas do site **pokemythology.net**
e extrair informações tabulares sobre Pokémon.  
O fluxo de uso previsto é:

- Instanciar ``PokemonCrawler`` com a URL de uma lista ou página individual.
- Chamar ``crawl()`` - que devolve uma ``list[Pokemon]``.

O módulo também oferece ``discover_pages`` (método estático) para, a partir da
página *lista01.htm*, descobrir todos os demais HTML relevantes.

[EN]
Module responsible for crawling **pokemythology.net** pages and extracting
tabular Pokémon information.  
Typical usage flow:

- Instantiate ``PokemonCrawler`` with a list or individual page URL.
- Call ``crawl()`` - returns a ``list[Pokemon]``.

The module also provides ``discover_pages`` (static method), which, starting from
*lista01.htm*, discovers all relevant HTML pages.

Uso típico / Typical usage:
    from services.pokemon_crawler import PokemonCrawler

    urls = PokemonCrawler.discover_pages("https://pokemythology.net/conteudo/pokemon/lista01.htm")
    for url in urls:
        pokemons = PokemonCrawler(url).crawl()
        for p in pokemons:
            print(p.to_dict())
"""
from __future__ import annotations

import logging
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

from models.pokemon import Pokemon
from models.pokemon_builder import PokemonBuilder

# [PT-BR] Cores usadas nas tabelas do site; mantidas como *constantes* de módulo.
# [EN] Colors used in the site’s tables; kept as module-level *constants*.
HEADER_COLORS = ["#96B8FB", "#ADC7FB"]
VALUE_COLORS: list[str] = ["#CADAF9", "#cadaf9", "#DEE9FF"]

class ParsingError(Exception):
    """[PT-BR] Erro genérico de parsing (ex.: tabela fora do padrão ou campo essencial ausente).
    [EN] Generic parsing error (e.g., malformed table or missing essential field).
    """
class PokemonCrawler:
    """[PT-BR] Crawleia páginas HTML da *PokéMythology* e devolve objetos :class:`Pokemon`.
    [EN] Crawls *PokéMythology* HTML pages and returns :class:`Pokemon` objects.
    """

    BASE_URL = "https://pokemythology.net"

    def __init__(self, url: str) -> None:
        self.url = url

    # ---------------------------------------------------------------------
    # [PT-BR] Métodos utilitários (HTTP / descoberta)
    # [EN] Utility methods (HTTP / discovery)
    # ---------------------------------------------------------------------
    @staticmethod
    def discover_pages(start_page: str) -> list[str]:
        """
        [PT-BR] Descobre todas as sub-páginas de Pokémon a partir da *start_page*.

        A função realiza uma varredura na página inicial fornecida, buscando todos os links
        que começam com ``/conteudo/pokemon/`` e terminam com ``.htm``. Esses links apontam
        para páginas individuais de Pokémon ou listas relacionadas.

        O retorno é uma lista de URLs absolutas, já resolvidas a partir do domínio base
        do site PokéMythology. A lista final é ordenada alfabeticamente e não contém duplicatas.

        Parâmetros:
            start_page (str): URL completa da primeira página de onde começar a descoberta.

        Retorna:
            list[str]: Lista ordenada e única de URLs para páginas de Pokémon.

        [EN] Discovers all Pokémon sub-pages starting from the given *start_page*.

        This function scans the initial page for all anchor tags whose `href` attribute
        starts with ``/conteudo/pokemon/`` and ends with ``.htm`` — these represent individual
        Pokémon or list pages.

        It returns a list of absolute URLs resolved using the site's base domain.
        The result is an alphabetically sorted list with duplicates removed.

        Parameters:
            start_page (str): Full URL of the starting page for discovery.

        Returns:
            list[str]: Alphabetically sorted, deduplicated list of Pokémon page URLs.
        """
        resp = requests.get(start_page, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        links: list[str] = []
        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            if href.startswith("/conteudo/pokemon/") and href.endswith(".htm"):
                links.append(urljoin(PokemonCrawler.BASE_URL, href))

        return sorted(set(links))

    def fetch_html(self) -> str:
        """[PT-BR] Faz download do HTML da URL com *user-agent* customizado.
        [EN] Downloads HTML content from the given URL with a custom user-agent.
        """
        try:
            req = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req) as resp:
                return resp.read().decode("latin1")
        except (URLError, HTTPError):
            logging.error("Error accessing URL %s", self.url, exc_info=True)
            raise

    # ------------------------------------------------------------------
    # [PT-BR] Pipeline público
    # [EN] Public pipeline
    # ------------------------------------------------------------------
    def crawl(self) -> list[Pokemon]:
        """[PT-BR] Retorna uma lista de :class:`Pokemon` encontrados na página.
        [EN] Returns a list of :class:`Pokemon` found on the page.
        """
        html = self.fetch_html()
        return list(self._parse_tables(html))

    # ------------------------------------------------------------------
    # [PT-BR] Parsing interno
    # [EN] Internal parsing
    # ------------------------------------------------------------------
    def _parse_tables(self, html: str) -> Iterable[Pokemon]:
        """
        [PT-BR] Lê todas as tabelas *principais* e converte em objetos ``Pokemon``.

        Uma *tabela principal* é identificada por possuir o atributo ``id`` no HTML.
        O método percorre cada linha da tabela (elementos ``<tr>``) e realiza as seguintes etapas:
        
        1. Captura a imagem principal do Pokémon (se houver);
        2. Captura a imagem de coloração shiny, quando disponível;
        3. Lê pares de dados no formato *rótulo: valor*;
        4. Preenche um objeto ``PokemonBuilder`` com os dados extraídos.

        Ao final, devolve instâncias de ``Pokemon`` geradas dinamicamente com base nos dados tabulares.

        Parâmetros:
            html (str): Conteúdo HTML bruto da página a ser processada.

        Retorna:
            Iterable[Pokemon]: Objetos ``Pokemon`` criados a partir das tabelas da página.

        [EN] Reads all *main* tables and converts them into ``Pokemon`` objects.

        A *main table* is identified by having an ``id`` attribute in the HTML markup.
        The method iterates over each row (``<tr>`` elements) and performs the following steps:

        1. Extracts the Pokémon's main image (if available);
        2. Extracts the shiny coloration image (if available);
        3. Parses data pairs in the form *label: value*;
        4. Populates a ``PokemonBuilder`` object with the extracted data.

        Returns dynamically built ``Pokemon`` instances based on the page's tabular structure.

        Parameters:
            html (str): Raw HTML content of the page to be parsed.

        Returns:
            Iterable[Pokemon]: List of ``Pokemon`` objects generated from the parsed tables.
        """
        soup = BeautifulSoup(html, "html.parser")

        for ix, table in enumerate(soup.find_all("table"), start=1):
            if not table.get("id"):
                continue  # [PT-BR] Ignora tabelas decorativas (sem atributo 'id')
                          # [EN] Skip decorative tables (those without an 'id' attribute)

            try:
                row_data: dict[str, str] = {}
                main_image: str | None = None
                trs = table.find_all("tr")

                for pos, tr in enumerate(trs):
                    tds = tr.find_all("td")
                    if not tds:
                        continue

                    # --------------------------------------------------
                    # [PT-BR] Imagem principal (primeira <img> encontrada na coluna 0)
                    # [EN]  Main image (first <img> tag found in column 0)
                    # --------------------------------------------------
                    if not main_image and tds[0].find("img"):
                        img = tds[0].find("img")
                        if img and img.get("src"):
                            main_image = urljoin(self.BASE_URL, img["src"])
                            row_data["Imagem"] = main_image

                    # --------------------------------------------------
                    # [PT-BR] Número do Pokémon (formato "001")
                    # [EN]    Pokémon number (format "001")
                    # --------------------------------------------------
                    if len(tds) >= 2 and "Nº" in tds[0].get_text():
                        row_data["Nº"] = tds[1].get_text(strip=True)
                        # Não faz *continue* – podemos ter mais info na mesma linha

                    # --------------------------------------------------
                    # [PT-BR] Coloração shiny (procura "Coloração Shiny" na linha atual ou na próxima, se necessário)
                    # [EN]    Shiny coloration (searches for "Coloração Shiny" in the current row or the next one, if needed)
                    # --------------------------------------------------
                    line_txt = tr.get_text(" ", strip=True).lower()
                    if "coloração shiny" in line_txt:
                        shiny_img = tr.find("img") or (trs[pos + 1].find("img") if pos + 1 < len(trs) else None)
                        if shiny_img and shiny_img.get("src"):
                            row_data["Coloração Shiny"] = urljoin(self.BASE_URL, shiny_img["src"])
                        continue

                    # --------------------------------------------------
                    # [PT-BR] Coloração shiny embutida na linha do nome
                    # [EN]    Shiny coloration embedded in the name row
                    # --------------------------------------------------
                    if len(tds) >= 2 and "Nome:" in tds[0].get_text():
                        img = tr.find("img")
                        if img and img.get("src"):
                            row_data["Coloração Shiny"] = urljoin(self.BASE_URL, img["src"])

                    # --------------------------------------------------
                    # [PT-BR] Pares label/valor (colunas 0‑1, 2‑3, ...)
                    # [EN]    Label/value pairs (columns 0‑1, 2‑3, ...)
                    # --------------------------------------------------
                    for i in range(0, len(tds) - 1, 2):
                        label = tds[i].get_text(strip=True)
                        if not label.endswith(":"):
                            continue
                        value = tds[i + 1].get_text(" ", strip=True)
                        row_data[label.rstrip(":")] = value

                # ------------------------------------------------------
                # [PT-BR] Constrói o objeto ``Pokemon`` via builder
                # [EN]    Builds the ``Pokemon`` object using the builder
                # ------------------------------------------------------
                builder = PokemonBuilder()

                if "Nº" in row_data:
                    builder.number(row_data["Nº"])
                if "Nome" in row_data:
                    builder.name(row_data["Nome"])
                if "Tipo" in row_data:
                    for t in row_data["Tipo"].split("/"):
                        builder.add_type(t.strip())
                if main_image:
                    builder.image(main_image)

                # [PT-BR] Outros atributos genéricos (altura, peso, etc.)
                # [EN]    Generic attributes (height, weight, etc.)
                for k, v in row_data.items():
                    if k not in {"Nº", "Nome", "Tipo"}:
                        builder.add_attribute(k, v)

                yield builder.build()

            except Exception:
                logging.error("Failed to process table %d na URL %s", ix, self.url, exc_info=True)