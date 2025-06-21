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
        """
        [PT-BR] Faz download do HTML da URL com *user-agent* customizado.
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
        """
        [PT-BR] Retorna uma lista de :class:`Pokemon` encontrados na página.
        [EN] Returns a list of :class:`Pokemon` found on the page.
        """
        html = self.fetch_html()
        return list(self._parse_tables(html))

    # ------------------------------------------------------------------
    # [PT-BR] Parsing interno
    # [EN] Internal parsing
    # ------------------------------------------------------------------
    def _parse_tables(self, html: str) -> Iterable[Pokemon]:
        soup = BeautifulSoup(html, "html.parser")
        for table in soup.find_all("table", id=True):
            try:
                yield self._parse_single_table(table)
            except Exception:
                logging.error("Error on URL %s", self.url, exc_info=True)

    def _parse_single_table(self, table: Tag) -> Pokemon: # type: ignore
        row_data: dict[str, str] = {}
        main_image = None
        trs = table.find_all("tr")

        for pos, tr in enumerate(trs):
            tds = tr.find_all("td")
            if not tds:
                continue

            self._maybe_extract_main_image(tds, row_data)
            self._maybe_extract_number(tds, row_data)
            self._maybe_extract_shiny(tr, trs, pos, row_data)
            self._maybe_extract_label_value_pairs(tds, row_data)

        return self._build_pokemon(row_data)

    def _maybe_extract_main_image(self, tds: list[Tag], row_data: dict) -> None: # type: ignore
        if "Imagem" not in row_data and tds[0].find("img"):
            img = tds[0].find("img")
            if img and img.get("src"):
                main_image = urljoin(self.BASE_URL, img["src"])
                row_data["Imagem"] = main_image

    def _maybe_extract_number(self, tds: list[Tag], row_data: dict) -> None: # type: ignore
        if len(tds) >= 3 and tds[1].get_text(strip=True) == "Nº:":
            row_data["Nº"] = tds[2].get_text(strip=True)
        elif len(tds) >= 2 and "Nº" in tds[0].get_text():
            row_data["Nº"] = tds[1].get_text(strip=True)

    def _maybe_extract_shiny(self, tr: Tag, trs: list[Tag], pos: int, row_data: dict) -> None: # type: ignore
        line_txt = tr.get_text(" ", strip=True).lower()
        if "coloração shiny" in line_txt:
            shiny_img = tr.find("img") or (trs[pos + 1].find("img") if pos + 1 < len(trs) else None)
            if shiny_img and shiny_img.get("src"):
                row_data["Coloração Shiny"] = urljoin(self.BASE_URL, shiny_img["src"])
        elif len(tr.find_all("td")) >= 2 and "Nome:" in tr.find_all("td")[0].get_text():
            img = tr.find("img")
            if img and img.get("src"):
                row_data["Coloração Shiny"] = urljoin(self.BASE_URL, img["src"])

    def _maybe_extract_label_value_pairs(self, tds: list[Tag], row_data: dict) -> None: # type: ignore
        for i in range(0, len(tds) - 1, 2):
            label = tds[i].get_text(strip=True)
            if not label.endswith(":"):
                continue
            value = " ".join(tds[i + 1].get_text(" ", strip=True).split())
            row_data[label.rstrip(":")] = value

    def _build_pokemon(self, data: dict[str, str]) -> Pokemon:
        builder = PokemonBuilder()

        if "Nº" in data:
            builder.number(data["Nº"])
        if "Nome" in data:
            builder.name(data["Nome"])
        if "Tipo" in data:
            for t in data["Tipo"].split("/"):
                builder.add_type(t.strip())
        if "Imagem" in data:
            builder.image(data["Imagem"])

        for k, v in data.items():
            if k not in {"Nº", "Nome", "Tipo", "Imagem"}:
                builder.add_attribute(k, v)

        return builder.build()