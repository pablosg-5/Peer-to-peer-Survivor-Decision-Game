class Game:
    def __init__(self):
        self.scenarios = [
            {"scenario": "You are stranded on an island, do you want to build a shelter (1) or look for food (2)?", "choices": [1, 2]},
            {"scenario": "You come across a wild animal. Do you want to fight (1) or run away (2)?", "choices": [1, 2]},
            {"scenario": "You find a mysterious cave. Do you enter (1) or continue searching for food (2)?", "choices": [1, 2]},
            {"scenario": "You find a boat. Do you want to repair it (1) or stay on the island (2)?", "choices": [1, 2]},
            {"scenario": "You see a ship in the distance. Do you want to signal for help (1) or ignore it (2)?", "choices": [1, 2]},
            {"scenario": "You are rescued! Do you want to leave the island (1) or stay and explore more (2)?", "choices": [1, 2]},
        ]
        self.current_scenario = 0
        self.player_decision = None
        self.other_player_decision = None

    def get_scenario(self, index):
        return self.scenarios[index]

    def both_players_responded(self):
        """Verifica si ambos jugadores han respondido."""
        return self.player_decision is not None and self.other_player_decision is not None

    def reset_decisions(self):
        """Reinicia las decisiones para el siguiente escenario."""
        self.player_decision = None
        self.other_player_decision = None

    def get_results(self):
        """Genera los resultados basados en las decisiones de ambos jugadores."""
        return f"Your decision: {self.player_decision}, Other player's decision: {self.other_player_decision}"