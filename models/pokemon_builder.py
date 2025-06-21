from models.pokemon import Pokemon

class PokemonBuilder:
    def __init__(self):
        self._attrs = {
            "types": [],
            "extra_attributes": {}
        }

    def number(self, n: str):
        self._attrs["number"] = n
        return self

    def name(self, n: str):
        self._attrs["name"] = n
        return self

    def add_type(self, t: str):
        self._attrs["types"].append(t)
        return self

    def image(self, url: str):
        self._attrs["image"] = url
        return self

    def add_attribute(self, key: str, value: str):
        self._attrs["extra_attributes"][key] = value
        return self

    def build(self) -> Pokemon:
        return Pokemon(
            number=self._attrs.get("number", 0),
            name=self._attrs.get("name", ""),
            types=self._attrs["types"],
            image=self._attrs.get("image"),
            extra_attributes=self._attrs["extra_attributes"]
        )