"""
Módulo pokemon_builder.py
===========================

[PT-BR] Implementa o padrão de projeto Builder para facilitar a construção
de objetos ``Pokemon`` de forma incremental e segura.

[EN] Implements the Builder design pattern to simplify the incremental and safe
construction of ``Pokemon`` objects.

Uso / Usage:
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
        # [PT-BR] Armazena atributos intermediários antes de construir o objeto final
        # [EN] Stores intermediate attributes before building the final object
        self._attrs = {
            "types": [],
            "extra_attributes": {}
        }

    def number(self, n: str):
        # [PT-BR] Define o número do Pokémon (mantém zeros à esquerda)
        # [EN] Sets the Pokémon number (keeps leading zeros)
        self._attrs["number"] = n
        return self

    def name(self, n: str):
        # [PT-BR] Define o nome principal do Pokémon
        # [EN] Sets the main name of the Pokémon
        self._attrs["name"] = n
        return self

    def add_type(self, t: str):
        # [PT-BR] Adiciona um tipo à lista de tipos
        # [EN] Adds a type to the types list
        self._attrs["types"].append(t)
        return self

    def image(self, url: str):
        # [PT-BR] Define a URL da imagem principal
        # [EN] Sets the main image URL
        self._attrs["image"] = url
        return self

    def add_attribute(self, key: str, value: str):
        # [PT-BR] Adiciona um atributo extra ao dicionário de atributos personalizados
        # [EN] Adds an extra attribute to the custom attributes dictionary
        self._attrs["extra_attributes"][key] = value
        return self

    def build(self) -> Pokemon:
        # [PT-BR] Constrói e retorna a instância final de Pokemon
        # [EN] Builds and returns the final Pokemon instance
        return Pokemon(
            number=self._attrs.get("number", 0),
            name=self._attrs.get("name", ""),
            types=self._attrs["types"],
            image=self._attrs.get("image"),
            extra_attributes=self._attrs["extra_attributes"]
        )