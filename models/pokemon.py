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
    number: str
    name: str
    types: List[str]
    image: Optional[str] = None
    extra_attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        # [PT-BR] Campos fixos padronizados
        # [EN] Standard fixed fields
        data = {
            "Nº": str(self.number),
            "Nome": self.name,
            "Tipo": "/".join(self.types),
            "Imagem": self.image or ""
        }
        # [PT-BR] Acrescenta atributos extras capturados do HTML
        # [EN] Appends extra attributes extracted from HTML
        data.update(self.extra_attributes)
        return data