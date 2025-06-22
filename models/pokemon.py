"""
Módulo pokemon.py
===================

[PT-BR] Define a estrutura de dados imutável para representar um Pokémon.
Utiliza ``@dataclass`` com ``frozen=True`` para garantir imutabilidade.

[EN] Defines an immutable data structure to represent a Pokémon.
Uses ``@dataclass`` with ``frozen=True`` to ensure immutability.

A classe oferece um método ``to_dict()`` que transforma a instância
em um dicionário formatado para exportação em CSV ou exibição.

The class provides a ``to_dict()`` method that converts the instance
into a dictionary formatted for CSV export or display.

Uso / Usage:
    p = Pokemon(number="025", name="Pikachu", types=["Electric"], image="...", extra_attributes={})
    d = p.to_dict()
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass(frozen=True)
class Pokemon:
    """
    [PT-BR] Representa um Pokémon com atributos fixos e extras. Imutável.
    [EN] Represents a Pokémon with fixed and extra attributes. Immutable.
    """
    number: str
    name: str
    types: List[str]
    image: Optional[str] = None
    extra_attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self, type_sep: str = "/") -> dict[str, str]:
        """
        [PT-BR] Converte o Pokémon em dicionário para exportação.
        [EN] Converts the Pokémon into a dictionary for export.

        Parâmetros:
            type_sep (str): Separador dos tipos no campo "Tipo".

        Retorna:
            dict[str, str]: Dicionário formatado.
        """
        data: dict[str, str] = {
            "Nº": self.number,
            "Nome": self.name,
            "Tipo": type_sep.join(self.types),
            "Imagem": self.image or ""
        }
        data.update(self.extra_attributes)
        return data

    def __str__(self) -> str:
        """
        [PT-BR] Representação legível do objeto.
        [EN] Human-readable object representation.
        """
        tipo = "/".join(self.types)
        return f"Pokemon[{self.number}] {self.name} ({tipo})"