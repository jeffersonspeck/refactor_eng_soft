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

import requests  # type: ignore
from bs4 import BeautifulSoup, Tag  # type: ignore

from models.pokemon import Pokemon
from models.pokemon_builder import PokemonBuilder

class PokemonFields:
    NUM = "Nº"
    NAME = "Nome"
    TYPE = "Tipo"
    IMAGE = "Imagem"
    SHINY = "Coloração Shiny"

class PokemonCrawler:
    BASE_URL = "https://pokemythology.net"

    def __init__(self, url: str) -> None:
        self.url = url

    @staticmethod
    def discover_pages(start_page: str) -> list[str]:
        resp = requests.get(start_page, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        links = [urljoin(PokemonCrawler.BASE_URL, a["href"])
                 for a in soup.find_all("a", href=True)
                 if a["href"].startswith("/conteudo/pokemon/") and a["href"].endswith(".htm")]

        return sorted(set(links))

    # ------------------------------------------------------------------
    # [PT-BR] Faz download do HTML da URL com *user-agent* customizado.
    # [EN] Downloads HTML content from the given URL with a custom user-agent.
    # ------------------------------------------------------------------
    def fetch_html(self) -> str:
        try:
            req = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req) as resp:
                return resp.read().decode("latin1")
        except (URLError, HTTPError) as e:
            logging.error("Error accessing URL %s: %s", self.url, str(e), exc_info=True)
            raise

    # ------------------------------------------------------------------
    # [PT-BR] Pipeline público
    # [EN] Public pipeline
    # ------------------------------------------------------------------
    def crawl(self) -> list[Pokemon]:
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
            except (AttributeError, IndexError, TypeError) as e:
                logging.error("Error parsing table on URL %s: %s", self.url, str(e), exc_info=True)

    def _parse_single_table(self, table: Tag) -> Pokemon:
        row_data: dict[str, str] = {}
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

    def _maybe_extract_main_image(self, tds: list[Tag], row_data: dict[str, str]) -> None:
        if PokemonFields.IMAGE not in row_data:
            img_tag = tds[0].find("img")
            if img_tag and img_tag.get("src"):
                row_data[PokemonFields.IMAGE] = urljoin(self.BASE_URL, img_tag["src"])

    def _maybe_extract_number(self, tds: list[Tag], row_data: dict[str, str]) -> None:
        if len(tds) >= 3 and tds[1].get_text(strip=True) == f"{PokemonFields.NUM}:":
            row_data[PokemonFields.NUM] = tds[2].get_text(strip=True)
        elif len(tds) >= 2 and PokemonFields.NUM in tds[0].get_text():
            row_data[PokemonFields.NUM] = tds[1].get_text(strip=True)

    def _maybe_extract_shiny(self, tr: Tag, trs: list[Tag], pos: int, row_data: dict[str, str]) -> None:
        line_txt = tr.get_text(" ", strip=True).lower()
        if "coloração shiny" in line_txt:
            shiny_img = tr.find("img") or (trs[pos + 1].find("img") if pos + 1 < len(trs) else None)
            if shiny_img and shiny_img.get("src"):
                row_data[PokemonFields.SHINY] = urljoin(self.BASE_URL, shiny_img["src"])
        elif len(tr.find_all("td")) >= 2 and "Nome:" in tr.find_all("td")[0].get_text():
            img = tr.find("img")
            if img and img.get("src"):
                row_data[PokemonFields.SHINY] = urljoin(self.BASE_URL, img["src"])

    def _maybe_extract_label_value_pairs(self, tds: list[Tag], row_data: dict[str, str]) -> None:
        for i in range(0, len(tds) - 1, 2):
            label = tds[i].get_text(strip=True)
            if not label.endswith(":"):
                continue
            value = " ".join(tds[i + 1].get_text(" ", strip=True).split())
            row_data[label.rstrip(":")] = value

    def _build_pokemon(self, data: dict[str, str]) -> Pokemon:
        builder = PokemonBuilder()

        if PokemonFields.NUM in data:
            builder.number(data[PokemonFields.NUM])
        if PokemonFields.NAME in data:
            builder.name(data[PokemonFields.NAME])
        if PokemonFields.TYPE in data:
            for t in data[PokemonFields.TYPE].split("/"):
                builder.add_type(t.strip())
        if PokemonFields.IMAGE in data:
            builder.image(data[PokemonFields.IMAGE])

        for k, v in data.items():
            if k not in {PokemonFields.NUM, PokemonFields.NAME, PokemonFields.TYPE, PokemonFields.IMAGE}:
                builder.add_attribute(k, v)

        return builder.build()