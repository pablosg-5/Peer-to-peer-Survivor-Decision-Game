class Game:
    def __init__(self, username, peer_usernames):
        # Scenario database containing all game paths and endings

        self.scenarios = [
            # LEVEL 0: INTRODUCTION
            {
                "scenario": "Your ship has been hit by a storm and no one has survived, except for you and your companion. You lost the rest of your companions during the incident. When you regain consciousness, both of you are stranded on the shore of an unknown island. The sun is approaching the horizon and uncertainty looms over you. You have to act quickly: search for food (1) or look for shelter (2).",
                "choices": [1, 2]
            },
            # ------------------------------
            # LEVEL 1
            # ------------------------------
            # LEVEL 1A: Both look for food - Coming from #Level 0
            {
                "scenario": "You decide to look for food together. You find some fruits in nearby trees, but some look poisonous. Eat the fruits (1) or look for another food source (2)?",
                "choices": [1, 2]
            },
            # LEVEL 1B: One looks for food, the other for shelter - Coming from #Level 0
            {
                "scenario": "One of you looks for food, while the other looks for shelter. The one looking for food finds suspicious fruits, while the other discovers a cave with danger signs. Do you decide to eat the fruits (1) or explore the cave (2)?",
                "choices": [1, 2]
            },
            # LEVEL 1C: Both look for shelter - Coming from #Level 0
            {
                "scenario": "You decide to look for shelter together. You find a cave that seems safe, but you hear noises inside. Enter the cave (1) or look for another place (2)?",
                "choices": [1, 2]
            },
            # ------------------------------
            # LEVEL 2
            # ------------------------------
            # LEVEL 2A: Eat the fruits - Coming from #Level 1A and 1B
            {
                "scenario": "You eat the fruits. One of them turns out to be poisonous and your companion begins to feel ill. Look for help on the island (1) or try to find an antidote in nature (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2B: Death by poisoning - Coming from #Level 1A
            {
                "scenario": "Some fruits turn out to be poisonous. Upon ingesting them, you become poisoned and unable to do anything. While trying to find another food source, you don't realize that your companion is in serious condition, so they die alone. As you continue looking for food, you fall off a cliff without noticing and die. End of game 1",
                "choices": ["end_game"]
            },
            # LEVEL 2C: Look for another food source - Coming from #Level 1A
            {
                "scenario": "You decide to look for another food source. You find a river with fish, but you don't have tools to fish. Try fishing with your hands (1) or keep looking (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2D: Enter the cave - Coming from #Level 1B and 1C
            {
                "scenario": "You enter the cave and discover it's inhabited by a bear. The bear attacks you. Try to defend yourselves (1) or flee (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2E: Death by separation - Coming from #Level 1C
            {
                "scenario": "The one who enters the cave is killed by a bear, while the other gets lost in the forest and dies under mysterious circumstances. End of game 2",
                "choices": ["end_game"]
            },
            # LEVEL 2F: Dual death - Coming from #Level 1B
            {
                "scenario": "The one who enters the cave is killed by a bear, while the one who eats the fruits is fatally poisoned. End of game 3",
                "choices": ["end_game"]
            },
            # LEVEL 2G: Radio rescue - Coming from #Level 1C
            {
                "scenario": "While looking for another place, you find a kind of abandoned shelter. In it, you find a radio that helps you communicate what happened and be rescued. End of game 4",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 3
            # ------------------------------
            # LEVEL 3A: Look for help - Coming from #Level 2A
            {
                "scenario": "Both decide to look for help on the island. After walking for a while, you find a hut of a solitary man. The man offers medicine for the poison, but warns you that it has a price. Accept the man's offer and help him collect herbs in a dangerous swamp (1) or reject the offer and continue looking for an alternative way to heal (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3B: Death by cliff - Coming from #Level 2A
            {
                "scenario": "While trying to find help, you get lost in the jungle and disappear forever. The one looking for a natural antidote falls off a cliff without noticing and dies. End of game 5",
                "choices": ["end_game"]
            },
            # LEVEL 3C: Look for antidote - Coming from #Level 2A
            {
                "scenario": "Both of you venture into the forest looking for healing plants. After several hours of searching, one of the characters falls into a poisonous pit and the poison spreads quickly. Try to get out of the pit in a hurry, even if it puts your life at risk (1) or stay in the pit, hoping to find a safer exit while the effects of the poison advance (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3D: Fish with hands - Coming from #Level 2C
            {
                "scenario": "You try to fish with your hands, but the fish are too fast. After several failed attempts, one of you finds an improvised spear on the shore. Try fishing with the spear (1) or continue looking for another food source (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3E: Death by discussion - Coming from #Level 2C
            {
                "scenario": "While discussing what to do, you are attacked by a bear that kills you. End of game 6",
                "choices": ["end_game"]
            },
            # LEVEL 3F: Death by natural trap - Coming from #Level 2C
            {
                "scenario": "Both fall into a natural trap while exploring and die. End of game 7",
                "choices": ["end_game"]
            },
            # LEVEL 3G: Successful defense - Coming from #Level 2D
            {
                "scenario": "You decide to face the bear with branches and stones. The creature shows aggression, but with effort you manage to scare it away. This allows you to find a flare gun in the cave that helps you get rescued on the beach by a ship. End of game 8",
                "choices": ["end_game"]
            },
            # LEVEL 3H: Death by fleeing - Coming from #Level 2D
            {
                "scenario": "You try to flee from the bear, but are caught and brutally killed. End of game 9",
                "choices": ["end_game"]
            },
            # LEVEL 3I: Death by separation - Coming from #Level 2D
            {
                "scenario": "While one tries to defend himself alone, he is killed by the bear. The other, while trying to flee, trips over a hole and dies due to the blow to the head. End of game 10",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 4
            # ------------------------------
            # LEVEL 4A: Get out of the pit - Coming from #Level 3C
            {
                "scenario": "You manage to get out of the pit together, but one is already infected. Try to burn wood and make signals on the beach to be quickly saved (1) or prioritize building a shelter (2)?",
                "choices": [1, 2]
            },
            # LEVEL 4B: Stay in the pit - Coming from #Level 3C
            {
                "scenario": "You stay in the pit and discover a hidden passage with ancient symbols. Explore the passage (1) or ignore it and wait for help (2)?",
                "choices": [1, 2]
            },
            # LEVEL 4C: Death by different options - Coming from #Level 3C
            {
                "scenario": "By getting out of the pit alone, you die from not being able to survive alone on the island. The one trying to find a safer exit dies affected by the poison. End of game 11",
                "choices": ["end_game"]
            },
            # LEVEL 4D: Death in the swamp - Coming from #Level 3A
            {
                "scenario": "Both die in the swamp due to the creatures that inhabit it and the lack of knowledge of the area. End of game 12",
                "choices": ["end_game"]
            },
            # LEVEL 4E: Death by poison - Coming from #Level 3A
            {
                "scenario": "By rejecting the man's offer, you decide to continue looking for an alternative way to heal. However, the poison spreads quickly and both die at dawn. End of game 13",
                "choices": ["end_game"]
            },
            # LEVEL 4F: Death by separation - Coming from #Level 3A
            {
                "scenario": "By deciding to separate, one of you falls into a natural trap and dies immediately, while the other, not getting an antidote, dies due to the poison. End of game 14",
                "choices": ["end_game"]
            },
            # LEVEL 4G: Adaptation to the island - Coming from #Level 3D
            {
                "scenario": "You manage to catch a big fish and cook it on an improvised fire. The food gives you energy to explore the island. This makes you end up adapting to the island and, due to the impossibility of being rescued, you end up staying to live. End of game 15",
                "choices": ["end_game"]
            },
            # LEVEL 4H: Death in the jungle - Coming from #Level 3D
            {
                "scenario": "By separating your paths, one disappears under strange circumstances in the jungle and the other is attacked by a bear in the forest, leading to his death. End of game 16",
                "choices": ["end_game"]
            },
            # LEVEL 4I: Both choose different things - Coming from 3D
            {
                "scenario": "By separating your paths, one disappears under strange circumstances in the jungle and the other is attacked by a bear in the forest leading to his death. End of game 3",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 5
            # ------------------------------
            # LEVEL 5A: Death by poison - Coming from #Level 4A
            {
                "scenario": "The poison spreads, and without an antidote, both die at dawn. End of game 17",
                "choices": ["end_game"]
            },
            # LEVEL 5B: Death by trap - Coming from #Level 4A
            {
                "scenario": "One falls into a natural trap and dies immediately, while the other, not getting an antidote, dies due to the poison. End of game 18",
                "choices": ["end_game"]
            },
            # LEVEL 5C: Explore ruins - Coming from #Level 4A
            {
                "scenario": "You find a natural cure in a plant and, while exploring the island, you discover ancient ruins covered with strange inscriptions. A mysterious force seems to emanate from the place. Explore the ruins (1) or move away and continue looking for survival (2)?",
                "choices": [1, 2]
            },
            # LEVEL 5D: Explore passage - Coming from #Level 4B
            {
                "scenario": "The passage leads you to a temple where an entity offers you immortality... in exchange for your souls. The temple entity demands a sacrifice. Accept the deal (1) or reject it and flee (2)?",
                "choices": [1, 2]
            },
            # LEVEL 5E: Death by waiting - Coming from #Level 4B
            {
                "scenario": "Both die due to the poison and the wait. End of game 19",
                "choices": ["end_game"]
            },
            # LEVEL 5F: Death in the passage - Coming from #Level 4B
            {
                "scenario": "One dies due to the poison and the wait, the other dies under strange circumstances when starting to enter the passage. End of game 20",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 6
            # ------------------------------
            # LEVEL 6A: Accept entity's deal - Coming from #Level 5D
            {
                "scenario": "One of you dies, but the other gets supernatural powers... and an eternal curse that will make him wander the island as a ghost forever. End of game 21",
                "choices": ["end_game"]
            },
            # LEVEL 6B: Reject entity's deal - Coming from #Level 5D
            {
                "scenario": "The entity gets angry for disturbing its great lethargy and fleeing, and turns you into wild boars of the island with no memories. End of game 22",
                "choices": ["end_game"]
            },
            # LEVEL 6C: Explore ruins - Coming from #Level 5C
            {
                "scenario": "While exploring the ruins, a voice arises in your minds, offering forbidden knowledge in exchange for staying on the island. You feel a dark power enveloping you. Accept the deal (1) or reject it and flee (2)?",
                "choices": [1, 2]
            },
            # LEVEL 6D: Continue exploring - Coming from #Level 5C
            {
                "scenario": "You decide to continue exploring. You find a path that seems to lead to a higher area of the island. Follow the path (1) or return to the shelter (2)?",
                "choices": [1, 2]
            },
            # LEVEL 6E: Death in the ruins - Coming from #Level 5C
            {
                "scenario": "By separating your paths, one disappears under strange circumstances in the ruins and the other is attacked by a bear in the forest, leading to his death. End of game 23",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 7
            # ------------------------------
            # LEVEL 7A: Accept voice's deal - Coming from #Level 6C
            {
                "scenario": "You become guardians of the island with all the knowledge and secrets of it. Therefore, you learn to live on the island and stay forever. End of game 24",
                "choices": ["end_game"]
            },
            # LEVEL 7B: Reject voice's deal - Coming from #Level 6C
            {
                "scenario": "By rejecting the deal, both suffer a sudden death to protect the secrets of the island. End of game 25",
                "choices": ["end_game"]
            },
            # LEVEL 7C: Guardian's betrayal - Coming from #Level 6C
            {
                "scenario": "By only one accepting the deal, he becomes the guardian of the island and murders his companion to protect its secrets. End of game 26",
                "choices": ["end_game"]
            },
            # LEVEL 7D: Follow the path - Coming from #Level 6D
            {
                "scenario": "You decide to follow the path and find a fresh water spring. Stay near the spring (1) or continue exploring (2)?",
                "choices": [1, 2]
            },
            # LEVEL 7E: Return to shelter - Coming from #Level 6D
            {
                "scenario": "You return to the shelter and decide to improve its structure. Over time, you feel safer. You end up choosing to stay and live on the island. End of game 27",
                "choices": ["end_game"]
            },
            # LEVEL 7F: Explore and adapt - Coming from #Level 6D
            {
                "scenario": "By separating your paths, one better reinforces the shelter, adapting to it and the island and staying to live forever. The one who decides to explore manages to find a boat that helps him leave the island and be rescued at sea weeks later. End of game 28",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 8
            # ------------------------------
            # LEVEL 8A: Stay near the spring - Coming from #Level 7D
            {
                "scenario": "You stay near the spring and build a temporary shelter. The fresh water gives you energy, but food is still scarce. Look for food in the surroundings (1) or try to fish (2)?",
                "choices": [1, 2]
            },
            # LEVEL 8B: Final rescue - Coming from #Level 7D
            {
                "scenario": "As you continue exploring, you find a stranded boat on another beach. After several attempts, you manage to set sail and are rescued a few weeks later at sea. End of game 29",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 9
            # ------------------------------
            # LEVEL 9A: Look for food - Coming from #Level 8A
            {
                "scenario": "You look for food in the surroundings and find a tree with unknown fruits. Risk eating them (1) or look for another food source (2)?",
                "choices": [1, 2]
            },
            # LEVEL 9B: Try fishing - Coming from #Level 8A
            {
                "scenario": "You try fishing in the spring, but there are no fish. However, you find a nearby stream. Follow the stream (1) or return to the shelter (2)?",
                "choices": [1, 2]
            },
            # LEVEL 9C: Adaptation and rescue - Coming from #Level 8A
            {
                "scenario": "By separating your paths, one manages to better adapt to the island through fishing and the use of utensils created from wood, adapting to the island and staying to live forever. The one who decides to look in the surroundings manages to find a boat that helps him leave the island and be rescued at sea weeks later. End of game 30",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 10
            # ------------------------------
            # LEVEL 10A: Deadly hallucinations - Coming from #Level 9A
            {
                "scenario": "You eat the unknown fruits. Which causes hallucinations and you kill each other. End of game 31",
                "choices": ["end_game"]
            },
            # LEVEL 10B: Definitive adaptation - Coming from #Level 9A
            {
                "scenario": "You end up finding some eggs near a bird's nest. The experience you gain makes you adapt to the island and stay to survive. End of game 32",
                "choices": ["end_game"]
            },
            # LEVEL 10C: Suicide by hallucinations - Coming from #Level 9A
            {
                "scenario": "The one who decides to eat the fruits suffers great hallucinations, which causes him to kill his companion and then commit suicide. End of game 33",
                "choices": ["end_game"]
            },
            # LEVEL 10D: Explore hidden cave - Coming from #Level 9B
            {
                "scenario": "You follow the stream and find a waterfall. Behind the waterfall, there is a hidden cave. Explore the cave (1) or return to the shelter (2)?",
                "choices": [1, 2]
            },
            # LEVEL 10E: Peaceful life - Coming from #Level 9B
            {
                "scenario": "You decide to stay on the beach and build a life on the island. Over time, you learn to survive and find peace in your new home. End of game 34",
                "choices": ["end_game"]
            },
            # LEVEL 10F: Both choose to return to shelter - Coming from 9B
            {
                "scenario": "You decide to stay on the beach and build a life on the island. Over time, you learn to survive and find peace in your new home. End of game 18",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 11
            # ------------------------------
            # LEVEL 11A: Touch the altar - Coming from #Level 10D
            {
                "scenario": "You explore the cave and find an ancient altar with strange symbols. Touch the altar (1) or ignore it (2)?",
                "choices": [1, 2]
            },
            # LEVEL 11B: Death in the cave - Coming from #Level 10D
            {
                "scenario": "By separating your paths, one manages to better adapt to the island by returning to the shelter, adapting to the island and staying to live forever. The one who decides to explore the cave disappears forever. End of game 35",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 12
            # ------------------------------
            # LEVEL 12A: Infinite knowledge - Coming from #Level 11A
            {
                "scenario": "When touching the altar, a bright light envelops you. A voice offers you infinite knowledge in exchange for staying. Accept (1) or reject (2)?",
                "choices": [1, 2]
            },
            # LEVEL 12B: Rescue by bonfire - Coming from #Level 11A
            {
                "scenario": "You decide to ignore the altar. Upon exiting, you see a ship on the horizon. Make a bonfire (1) or wait (2)?",
                "choices": [1, 2]
            },
            # LEVEL 12C: Deadly trap - Coming from #Level 11A
            {
                "scenario": "One touches the altar and disappears. The other tries to help him and falls into a deadly trap. End of game 36",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 13
            # ------------------------------
            # LEVEL 13A: Cosmic immortality - Coming from #Level 12A
            {
                "scenario": "You are transported to a dimension of eternal knowledge. Where you discover cosmic secrets but lose your humanity and become immortal entities. End of game 37",
                "choices": ["end_game"]
            },
            # LEVEL 13B: Escape from the cave - Coming from #Level 12A
            {
                "scenario": "The entity becomes enraged. The cave collapses. Run (1) or look for an alternative exit (2)?",
                "choices": [1, 2]
            },
            # LEVEL 13C: Final rescue - Coming from #Level 12B
            {
                "scenario": "The ship sees you and you manage to be rescued. End of game 38",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 14
            # ------------------------------
            # LEVEL 14A: Arid desert - Coming from #Level 13B
            {
                "scenario": "You manage to escape, but the outside is now an arid desert, with no traces of life. End of game 39",
                "choices": ["end_game"]
            },
            # LEVEL 14B: Rescue at sea - Coming from #Level 13B
            {
                "scenario": "You look for another exit and find a tunnel that leads you to a deserted beach. You try to build a raft with the remains of the shipwreck. After several attempts, you manage to set sail and are rescued a few weeks later at sea. End of game 40",
                "choices": ["end_game"]
            },
            # LEVEL 14C: Death in the cave - Coming from #Level 13B
            {
                "scenario": "By not agreeing, you are buried by the falling stones, leaving your bodies sealed with the cave. End of game 41",
                "choices": ["end_game"]
            }
        ]

        # State transition matrix: {current_scenario: {(decision1, decision2): next_scenario}}
        self.transitions = {
            # LEVEL 0
            0: {
                (1, 1): 1, (2, 2): 3, (1, 2): 2, (2, 1): 2
            },
            # LEVEL 1A
            1: {
                (1, 1): 4, (2, 2): 6, (1, 2): 5, (2, 1): 5
            },
            # LEVEL 1B
            2: {
                (1, 1): 4, (2, 2): 7, (1, 2): 9, (2, 1): 9
            },
            # LEVEL 1C
            3: {
                (1, 1): 7, (2, 2): 10, (1, 2): 8, (2, 1): 8
            },
            # LEVEL 2A
            4: {
                (1, 1): 11, (2, 2): 13, (1, 2): 12, (2, 1): 12
            },
            # LEVEL 2C
            6: {
                (1, 1): 14, (2, 2): 16, (1, 2): 15, (2, 1): 15
            },
            # LEVEL 2D
            7: {
                (1, 1): 17, (2, 2): 18, (1, 2): 19, (2, 1): 19
            },
            # LEVEL 3A
            11: {
                (1, 1): 23, (2, 2): 24, (1, 2): 25, (2, 1): 25
            },
            # LEVEL 3C
            13: {
                (1, 1): 20, (2, 2): 21, (1, 2): 22, (2, 1): 22
            },
            # LEVEL 3D
            14: {
                (1, 1): 26, (2, 2): 27, (1, 2): 28, (2, 1): 28
            },
            # LEVEL 4A
            20: {
                (1, 1): 29, (2, 2): 30, (1, 2): 31, (2, 1): 31
            },
            # LEVEL 4B
            21: {
                (1, 1): 32, (2, 2): 33, (1, 2): 34, (2, 1): 34
            },
            # LEVEL 5C
            31: {
                (1, 1): 37, (2, 2): 38, (1, 2): 39, (2, 1): 39
            },
            # LEVEL 5D
            32: {
                (1, 1): 35, (2, 2): 36, (1, 2): 36, (2, 1): 36
            },
            # LEVEL 6C
            37: {
                (1, 1): 40, (2, 2): 41, (1, 2): 42, (2, 1): 42
            },
            # LEVEL 6D
            38: {
                (1, 1): 43, (2, 2): 44, (1, 2): 45, (2, 1): 45
            },
            # LEVEL 7D
            43: {
                (1, 1): 46, (2, 2): 47, (1, 2): 45, (2, 1): 45
            },
            # LEVEL 8A
            46: {
                (1, 1): 48, (2, 2): 49, (1, 2): 50, (2, 1): 50
            },
            # LEVEL 9A
            48: {
                (1, 1): 51, (2, 2): 52, (1, 2): 53, (2, 1): 53
            },
            # LEVEL 9B
            49: {
                (1, 1): 54, (2, 2): 55, (1, 2): 56, (2, 1): 56
            },
            # LEVEL 10D
            54: {
                (1, 1): 57, (2, 2): 58, (1, 2): 59, (2, 1): 59
            },
            # LEVEL 11A
            57: {
                (1, 1): 60, (2, 2): 61, (1, 2): 62, (2, 1): 62
            },
            # LEVEL 12A
            59: {
                (1, 1): 63, (2, 2): 64, (1, 2): 65, (2, 1): 65
            },
            # LEVEL 13B
            63: {
                (1, 1): 69, (2, 2): 70, (1, 2): 71, (2, 1): 71
            }
        }

        # Game state management
        self.username = username            # Current player's name
        self.peer_usernames = peer_usernames  # Other players' names
        self.current_scenario = 0           # Current scenario ID
        self.player_decision = None         # Player's current choice
        self.received_decisions = {}        # Decisions from peers
        self.game_over = False              # Game status flag
        self.game_result = ""               # Final game outcome text

    def get_scenario(self):
        # Get current scenario data
        return self.scenarios[self.current_scenario]

    def register_decision(self, username, decision):
        # Store decisions from network peers
        self.received_decisions[username] = decision

    def process_decisions(self):
        # Gather all choices: the player's decision + decisions received from peers
        all_choices = [self.player_decision] + list(self.received_decisions.values())

        # if still you are 3 players
        if len(all_choices) == 3:
            if all(c == 1 for c in all_choices):
                decision_pair = (1, 1)
            elif all(c == 2 for c in all_choices):
                decision_pair = (2, 2)
            else:
                count_1 = sum(1 for c in all_choices if c == 1)
                count_2 = 3 - count_1 

                if count_1 > count_2:  
                    decision_pair = (1, 2)
                else:  
                    decision_pair = (2, 1)

        # if you are 2 players
        elif len(all_choices) == 2:
            p1, p2 = all_choices  # Unpack player decisions

            if p1 == p2:
                decision_pair = (p1, p1)
            else:
                decision_pair = (p1, p2)

        else:
            raise ValueError("Invalid number of decisions. Expected 2 or 3.")
        
        self.apply_scenario_transition(decision_pair)

    def apply_scenario_transition(self, decision_pair):
        current_transitions = self.transitions.get(self.current_scenario, {})
        next_scenario = current_transitions.get(decision_pair, None)

        # Update game state
        self.current_scenario = next_scenario if next_scenario is not None else self.current_scenario
        self.game_over = not self.scenarios[self.current_scenario].get(
            "choices", False)

    def reset_decisions(self):
        # Clear decisions for new round
        self.player_decision = None
        self.received_decisions.clear()

    def full_reset(self):
        # Complete game state reset
        self.current_scenario = 0
        self.reset_decisions()
        self.game_over = False
        self.game_result = ""
