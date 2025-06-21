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

class QuestPokemon:
    ENVIRONMENTS = [
        "Dense forest", "Dark cave", "Busy city",
        "Scorching desert", "Snowy mountain", "Ancient ruins",
        "Gloomy swamp", "Frozen lake", "Mysterious village"
    ]

    DIFFICULTIES = ["Easy", "Medium", "Hard", "Epic"]

    REWARDS = [
        "You found a special Poké Ball!",
        "You received a rare TM.",
        "An NPC healed your Pokémon.",
        "You caught a rare wild Pokémon.",
        "You received 2000 PokéDollars.",
        "You obtained an evolution item.",
        "You unlocked a new map area.",
        "You received a mysterious egg."
    ]

    CHALLENGES = [
        "Trainer uses only Fire-type Pokémon",
        "Double battle against twin trainers",
        "Only status moves are allowed (e.g., Growl, Sleep Powder)",
    ]

    def __init__(self, url: str):
        # [PT-BR] Armazena a URL e sorteia um conjunto de elementos da missão
        # [EN]    Stores the URL and randomly selects a set of quest elements
        self.url = url
        self.environment = random.choice(self.ENVIRONMENTS)
        self.difficulty = random.choice(self.DIFFICULTIES)
        self.challenge = random.choice(self.CHALLENGES)
        self.reward = random.choice(self.REWARDS)

    def generate_description(self) -> str:
        # [PT-BR] Gera descrição textual da missão formatada
        # [EN]    Generates a formatted textual description of the quest
        return (
            f"\n"
            f"Environment: {self.environment}\n"
            f"Path: {self.url}\n"
            f"Challenge: {self.challenge}\n"
            f"Difficulty: {self.difficulty}\n"
            f"Reward: {self.reward}\n"
        )