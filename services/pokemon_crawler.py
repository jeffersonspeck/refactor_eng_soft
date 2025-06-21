import logging
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import requests
import unicodedata
from urllib.parse import urljoin
from models.pokemon import Pokemon
from typing import Iterable
from bs4 import BeautifulSoup
from models.pokemon_builder import PokemonBuilder

HEADER_COLORS = ["#96B8FB", "#ADC7FB"]
VALUE_COLORS  = ["#CADAF9", "#cadaf9", "#DEE9FF"]

class ParsingError(Exception):
    pass

class PokemonCrawler:
    BASE_URL = "https://pokemythology.net"        
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def discover_pages(start_page: str) -> list[str]:
        resp = requests.get(start_page, headers={"User-Agent": "Mozilla/5.0"})
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/conteudo/pokemon/") and href.endswith(".htm"):
                full_url = urljoin(PokemonCrawler.BASE_URL, href)
                links.append(full_url)

        return sorted(set(links))


    def fetch_html(self) -> str:
        try:
            req = Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req) as response:
                return response.read().decode("latin1")
        except (URLError, HTTPError) as e:
            logging.error("Erro ao acessar a URL %s", self.url, exc_info=True)
            raise

    def crawl(self) -> list[Pokemon]:
        html = self.fetch_html()
        return list(self._parse_tables(html))

    def _parse_tables(self, html: str):
        soup = BeautifulSoup(html, "html.parser")

        for ix, table in enumerate(soup.find_all("table"), start=1):
            if not table.get("id"):          # só tabelas principais
                continue

            try:
                row_data   = {}
                main_image = None

                trs = table.find_all("tr")
                for pos, tr in enumerate(trs):
                    tds = tr.find_all("td")
                    if not tds:
                        continue

                    print([td.get_text(strip=True) for td in tds])

                    # ---------- imagem principal ----------
                    if not main_image and tds[0].find("img"):
                        img = tds[0].find("img")
                        if img and img.get("src"):
                            main_image = urljoin(self.BASE_URL, img["src"])
                            row_data["Imagem"] = main_image

                    if len(tds) >= 2 and "Nº" in tds[0].get_text():
                        num_str = tds[1].get_text(strip=True)  # ex.: "001"
                        row_data["Nº"] = num_str               # mantém com zeros à esquerda
                        # não faça continue — ainda queremos processar o resto da linha     

                    # ---------- shiny ----------
                    line_txt = tr.get_text(" ", strip=True).lower()
                    if "coloração shiny" in line_txt:
                        # tenta pegar imagem na MESMA linha
                        shiny_img = tr.find("img")
                        # se não houver, olha a próxima linha
                        if not shiny_img and pos + 1 < len(trs):
                            shiny_img = trs[pos + 1].find("img")
                        if shiny_img and shiny_img.get("src"):
                            row_data["Coloração Shiny"] = urljoin(self.BASE_URL, shiny_img["src"])
                        continue

                    # Captura imagem shiny na mesma linha do nome
                    if len(tds) >= 2 and "Nome:" in tds[0].get_text():
                        img = tr.find("img")
                        if img and img.get("src"):
                            shiny_image = urljoin(self.BASE_URL, img["src"])
                            row_data["Coloração Shiny"] = shiny_image          

                    # ---------- pares label/valor ----------
                    # percorre 0-1, 2-3, ...
                    for i in range(0, len(tds) - 1, 2):
                        label = tds[i].get_text(strip=True)
                        if not label.endswith(":"):
                            continue
                        value = tds[i + 1].get_text(" ", strip=True)
                        row_data[label.rstrip(":")] = value

                # ---------- constrói Pokémon ----------
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

                for k, v in row_data.items():
                    if k not in {"Nº", "Nome", "Tipo"}:
                        builder.add_attribute(k, v)

                yield builder.build()

            except Exception:
                logging.error("Erro ao processar tabela %d", ix, exc_info=True)
