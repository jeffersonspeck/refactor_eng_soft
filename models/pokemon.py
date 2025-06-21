"""
Módulo pokemon.py
===================

Define a estrutura de dados imutável para representar um Pokémon.
Utiliza ``@dataclass`` com ``frozen=True`` para garantir imutabilidade.

A classe oferece um método ``to_dict()`` que transforma a instância
em um dicionário formatado para exportação em CSV ou exibição.

Uso:
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
        # Campos fixos padronizados
        data = {
            "Nº": str(self.number),
            "Nome": self.name,
            "Tipo": "/".join(self.types),
            "Imagem": self.image or ""
        }
        # Acrescenta atributos extras capturados do HTML
        data.update(self.extra_attributes)
        return data
