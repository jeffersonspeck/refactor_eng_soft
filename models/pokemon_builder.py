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
from typing import TypeVar
Self = TypeVar("Self", bound="PokemonBuilder")
from models.pokemon import Pokemon

class PokemonBuilder:
    """
    [PT-BR] Builder para criar objetos Pokemon de forma segura e incremental.
    [EN] Builder to create Pokemon objects safely and incrementally.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._attrs: dict[str, object] = {
            "types": [],
            "extra_attributes": {}
        }

    def number(self, n: str) -> Self:
        self._attrs["number"] = n
        return self

    def name(self, n: str) -> Self:
        self._attrs["name"] = n
        return self

    def add_type(self, t: str) -> Self:
        self._attrs["types"].append(t)
        return self

    def image(self, url: str) -> Self:
        self._attrs["image"] = url
        return self

    def add_attribute(self, key: str, value: str) -> Self:
        self._attrs["extra_attributes"][key] = value
        return self

    def build(self) -> Pokemon:
        if "number" not in self._attrs or "name" not in self._attrs:
            raise ValueError("Pokemon must have at least a number and a name.")

        pokemon = Pokemon(
            number=self._attrs["number"],
            name=self._attrs["name"],
            types=self._attrs["types"],
            image=self._attrs.get("image"),
            extra_attributes=self._attrs["extra_attributes"]
        )

        self.reset()
        return pokemon