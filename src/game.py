class Game:
    def __init__(self):
        self.scenarios = [
            {"scenario": "You are stranded on an island, do you want to build a shelter (1) or look for food (2)?", "choices": [1, 2]},
            {"scenario": "You come across a wild animal. Do you want to fight (1) or run away (2)?", "choices": [1, 2]},
            # Puedes agregar más escenarios aquí
        ]
        self.results = []

    def get_scenario(self, index):
        return self.scenarios[index]

    def process_decision(self, decision):
        if decision == 1:
            self.results.append("You built a shelter or fought the animal.")
        elif decision == 2:
            self.results.append("You found food or ran away.")

    def get_results(self):
        return self.results
