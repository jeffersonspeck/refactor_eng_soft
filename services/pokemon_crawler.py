"""pokemon_crawler.py
====================
Módulo responsável por varrer ("crawlear") páginas do site **pokemythology.net**
e extrair informações tabulares sobre Pokémon.  
O fluxo de uso previsto é:

1. Instanciar ``PokemonCrawler`` com a URL de uma lista ou página individual.
2. Chamar ``crawl()`` - que devolve um ``list[Pokemon]``.

O módulo também oferece ``discover_pages`` (método estático) para, a partir da
página *lista01.htm*, descobrir todos os demais HTML relevantes.

Boas-práticas adotadas
----------------------
* **Docstrings** completos em todas as classes e métodos.
* **Inline-comments** apenas onde o código não é auto-explicativo.
* **Logging** em vez de ``print`` para erros ou avisos.
* **Typed hints** (`list[str]`, `Iterable[Pokemon]`, …) para legibilidade e IDE support.
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

# Cores usadas nas tabelas do site; mantidas como *constantes* de módulo.
HEADER_COLORS = ["#96B8FB", "#ADC7FB"]
VALUE_COLORS: list[str] = ["#CADAF9", "#cadaf9", "#DEE9FF"]


class ParsingError(Exception):
    """Erro genérico de parsing (ex.: tabela fora do padrão ou campo essencial ausente)."""


class PokemonCrawler:
    """Crawleia páginas HTML da *PokéMythology* e devolve objetos :class:`Pokemon`."""

    BASE_URL = "https://pokemythology.net"

    def __init__(self, url: str) -> None:
        self.url = url

    # ---------------------------------------------------------------------
    # Métodos utilitários (HTTP / descoberta)
    # ---------------------------------------------------------------------
    @staticmethod
    def discover_pages(start_page: str) -> list[str]:
        """Descobre todas as sub‑páginas de Pokémon a partir da *start_page*.

        A função busca links que começam com ``/conteudo/pokemon/`` e terminam
        com ``.htm``; devolve a lista **ordenada e sem duplicatas**.
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
        """Faz download do HTML da :pyattr:`url` com *user-agent* customizado."""
        try:
            req = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req) as resp:
                return resp.read().decode("latin1")
        except (URLError, HTTPError):
            logging.error("Error accessing URL %s", self.url, exc_info=True)
            raise

    # ------------------------------------------------------------------
    # Pipeline público
    # ------------------------------------------------------------------
    def crawl(self) -> list[Pokemon]:
        """Retorna uma lista de :class:`Pokemon` encontrados na página."""
        html = self.fetch_html()
        return list(self._parse_tables(html))

    # ------------------------------------------------------------------
    # Parsing interno
    # ------------------------------------------------------------------
    def _parse_tables(self, html: str) -> Iterable[Pokemon]:
        """Lê todas as tabelas *principais* e converte em objetos ``Pokemon``.

        Uma *tabela principal* é identificada por possuir atributo ``id`` no
        HTML. O método percorre cada linha (``<tr>``) e:
        1. Captura imagem principal e shiny quando existir;
        2. Lê pares *label: valor*;
        3. Feed a um :class:`PokemonBuilder`.
        """
        soup = BeautifulSoup(html, "html.parser")

        for ix, table in enumerate(soup.find_all("table"), start=1):
            if not table.get("id"):
                continue  # ignora tabelas decorativas

            try:
                row_data: dict[str, str] = {}
                main_image: str | None = None
                trs = table.find_all("tr")

                for pos, tr in enumerate(trs):
                    tds = tr.find_all("td")
                    if not tds:
                        continue

                    # --------------------------------------------------
                    # Imagem principal (primeira <img> encontrada na coluna 0)
                    # --------------------------------------------------
                    if not main_image and tds[0].find("img"):
                        img = tds[0].find("img")
                        if img and img.get("src"):
                            main_image = urljoin(self.BASE_URL, img["src"])
                            row_data["Imagem"] = main_image

                    # --------------------------------------------------
                    # Número do Pokémon (formato "001")
                    # --------------------------------------------------
                    if len(tds) >= 2 and "Nº" in tds[0].get_text():
                        row_data["Nº"] = tds[1].get_text(strip=True)
                        # Não faz *continue* – podemos ter mais info na mesma linha

                    # --------------------------------------------------
                    # Coloration shiny (procura "Coloração Shiny" na linha atual
                    # ou na próxima, se necessário)
                    # --------------------------------------------------
                    line_txt = tr.get_text(" ", strip=True).lower()
                    if "coloração shiny" in line_txt:
                        shiny_img = tr.find("img") or (trs[pos + 1].find("img") if pos + 1 < len(trs) else None)
                        if shiny_img and shiny_img.get("src"):
                            row_data["Coloração Shiny"] = urljoin(self.BASE_URL, shiny_img["src"])
                        continue

                    # Coloration shiny embutida na linha do nome
                    if len(tds) >= 2 and "Nome:" in tds[0].get_text():
                        img = tr.find("img")
                        if img and img.get("src"):
                            row_data["Coloração Shiny"] = urljoin(self.BASE_URL, img["src"])

                    # --------------------------------------------------
                    # Pares label/valor (0‑1, 2‑3, ...)
                    # --------------------------------------------------
                    for i in range(0, len(tds) - 1, 2):
                        label = tds[i].get_text(strip=True)
                        if not label.endswith(":"):
                            continue
                        value = tds[i + 1].get_text(" ", strip=True)
                        row_data[label.rstrip(":")] = value

                # ------------------------------------------------------
                # Constrói o objeto ``Pokemon`` via builder
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

                # Outros atributos genéricos (altura, peso, etc.)
                for k, v in row_data.items():
                    if k not in {"Nº", "Nome", "Tipo"}:
                        builder.add_attribute(k, v)

                yield builder.build()

            except Exception:  # noqa: BLE001 — queremos log detalhado
                logging.error("Failed to process table %d na URL %s", ix, self.url, exc_info=True)