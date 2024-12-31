class Game:
    def __init__(self):
        self.scenarios = [
            {
                "question": "You and your partner have found a treasure. Do you share it? (y/n)",
                "choices": {
                    "y": "You both decide to share the treasure. It's a win-win!",
                    "n": "You refuse to share the treasure. The partnership ends badly."
                }
            },
            {
                "question": "You both encounter a wild animal. Do you fight or run? (fight/run)",
                "choices": {
                    "fight": "You fight bravely, but it turns out to be a fatal encounter.",
                    "run": "You both escape safely, but you lost some of your supplies."
                }
            }
        ]
        self.current_scenario = 0

    def get_scenario(self):
        """ Devuelve el escenario actual. """
        if self.current_scenario < len(self.scenarios):
            return self.scenarios[self.current_scenario]
        else:
            return None

    def process_choices(self, choice1, choice2):
        """ Procesa las elecciones de ambos jugadores. """
        scenario = self.get_scenario()
        if not scenario:
            return "Game over!"

        # Repercusiones basadas en las decisiones de ambos jugadores
        if choice1 == choice2:
            return scenario["choices"][choice1]
        else:
            # Lógica para consecuencias si las decisiones son diferentes
            if choice1 == "y" and choice2 == "n":
                return "You shared the treasure, but your partner took it all. Betrayal leads to a fatal outcome."
            elif choice1 == "n" and choice2 == "y":
                return "You didn't want to share, but your partner did. You end up alone and in danger."
            elif choice1 == "fight" and choice2 == "run":
                return "One chose to fight, the other to run. The one who fought suffered the consequences."
            elif choice1 == "run" and choice2 == "fight":
                return "The one who ran away avoided danger, but the one who fought paid the price."
            else:
                return "Unusual choices lead to unexpected outcomes."

    def next_scenario(self):
        """ Pasa al siguiente escenario. """
        if self.current_scenario < len(self.scenarios) - 1:
            self.current_scenario += 1
        else:
            return None
