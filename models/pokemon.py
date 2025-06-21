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
        # Campos fixos
        data = {
            "Nº": str(self.number),
            "Nome": self.name,
            "Tipo": "/".join(self.types),
            "Imagem": self.image or ""
        }
        # Acrescentar os campos extras
        data.update(self.extra_attributes)
        return data