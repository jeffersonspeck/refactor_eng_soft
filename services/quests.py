"""
Módulo quests.py
==================

[PT-BR] Gera uma descrição aleatória de "missão" para cada página crawleada,
inspirada em desafios de jogos da franquia Pokémon.

[EN]    Generates a random "quest" description for each crawled page,
inspired by challenges from the Pokémon game series.

Uso / Usage:
    from services.quests import QuestPokemon
    quest = QuestPokemon(url)
    print(quest.generate_description())
"""
import random
from typing import Optional, Sequence

class QuestPokemon:
    """
    [PT-BR] Gera uma descrição de "missão" simulada para cada URL, inspirada em desafios da franquia.
    [EN]    Generates a simulated "quest" description for each URL, inspired by the franchise's challenges.
    """

    DEFAULT_ENVIRONMENTS = [
        "Dense forest", "Dark cave", "Busy city",
        "Scorching desert", "Snowy mountain", "Ancient ruins",
        "Gloomy swamp", "Frozen lake", "Mysterious village"
    ]

    DEFAULT_DIFFICULTIES = ["Easy", "Medium", "Hard", "Epic"]

    DEFAULT_REWARDS = [
        "You found a special Poké Ball!",
        "You received a rare TM.",
        "An NPC healed your Pokémon.",
        "You caught a rare wild Pokémon.",
        "You received 2000 PokéDollars.",
        "You obtained an evolution item.",
        "You unlocked a new map area.",
        "You received a mysterious egg."
    ]

    DEFAULT_CHALLENGES = [
        "Trainer uses only Fire-type Pokémon",
        "Double battle against twin trainers",
        "Only status moves are allowed (e.g., Growl, Sleep Powder)"
    ]

    def __init__(
        self,
        url: str,
        rng: Optional[random.Random] = None,
        environments: Optional[Sequence[str]] = None,
        difficulties: Optional[Sequence[str]] = None,
        rewards: Optional[Sequence[str]] = None,
        challenges: Optional[Sequence[str]] = None,
    ):
        """
        [PT-BR] Constrói uma missão com sorteio interno.
        [EN]    Builds a quest with internal random selection.
        """
        self.url = url
        self.rng = rng or random.Random()

        self.environment = self.rng.choice(environments or self.DEFAULT_ENVIRONMENTS)
        self.difficulty = self.rng.choice(difficulties or self.DEFAULT_DIFFICULTIES)
        self.challenge = self.rng.choice(challenges or self.DEFAULT_CHALLENGES)
        self.reward = self.rng.choice(rewards or self.DEFAULT_REWARDS)

    def to_text(self) -> str:
        """
        [PT-BR] Retorna uma representação textual da missão.
        [EN]    Returns a textual representation of the quest.
        """
        return (
            f"\n"
            f"Environment: {self.environment}\n"
            f"Path: {self.url}\n"
            f"Challenge: {self.challenge}\n"
            f"Difficulty: {self.difficulty}\n"
            f"Reward: {self.reward}\n"
        )

    def __str__(self) -> str:
        return self.to_text()