"""
Módulo pokemon_builder.py
===========================

Implementa o padrão de projeto Builder para facilitar a construção
de objetos ``Pokemon`` de forma incremental e segura.

Uso:
    builder = PokemonBuilder()
    pokemon = (
        builder.number("025")
               .name("Pikachu")
               .add_type("Electric")
               .image("https://.../pikachu.png")
               .add_attribute("Altura", "0.4m")
               .build()
    )
"""
from models.pokemon import Pokemon

class PokemonBuilder:
    def __init__(self):
        # Armazena atributos intermediários antes de construir o objeto final
        self._attrs = {
            "types": [],
            "extra_attributes": {}
        }

    def number(self, n: str):
        # Define o número do Pokémon (como string para manter zeros à esquerda)
        self._attrs["number"] = n
        return self

    def name(self, n: str):
        # Define o nome principal do Pokémon
        self._attrs["name"] = n
        return self

    def add_type(self, t: str):
        # Adiciona um tipo à lista de tipos
        self._attrs["types"].append(t)
        return self

    def image(self, url: str):
        # Define a URL da imagem principal
        self._attrs["image"] = url
        return self

    def add_attribute(self, key: str, value: str):
        # Adiciona um atributo extra ao dicionário de atributos não padronizados
        self._attrs["extra_attributes"][key] = value
        return self

    def build(self) -> Pokemon:
        # Constrói e retorna a instância final de Pokemon
        return Pokemon(
            number=self._attrs.get("number", 0),
            name=self._attrs.get("name", ""),
            types=self._attrs["types"],
            image=self._attrs.get("image"),
            extra_attributes=self._attrs["extra_attributes"]
        )