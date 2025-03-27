class Game:
    def __init__(self, username, peer_usernames):
        # Scenario database containing all game paths and endings

        self.scenarios = [
            # LEVEL 0: INTRODUCTION
            {
                "scenario": "Your ship has been wrecked by a storm, leaving only your group (2-3) alive. The rest of the crew perished. You awaken stranded on an unknown island at dusk. Act fast: search for food (1) or seek shelter (2).",
                "choices": [1, 2]
            },
            # ------------------------------
            # LEVEL 1
            # ------------------------------
            # LEVEL 1A: Both look for food - Coming from #Level 0
            {
                "scenario": "Your group searches for food together. You find fruits in trees—some look poisonous. Eat them (1) or seek alternatives (2)?",
                "choices": [1, 2]
            },
            # LEVEL 1B: One looks for food, the other for shelter - Coming from #Level 0
            {
                "scenario": "Half your group hunts food (finding suspicious fruits), while others find a cave with danger signs. Eat fruits (1) or explore cave (2)?",
                "choices": [1, 2]
            },
            # LEVEL 1C: Both look for shelter - Coming from #Level 0
            {
                "scenario": "Your group searches for shelter together. A cave seems safe but has strange noises. Enter (1) or keep searching (2)?",
                "choices": [1, 2]
            },
            # ------------------------------
            # LEVEL 2
            # ------------------------------
            # LEVEL 2A: Eat the fruits - Coming from #Level 1A and 1B
            {
                "scenario": "A group member eats a poisoned fruit and collapses. Search the island for help (1) or hunt for natural antidotes (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2B: Death by poisoning - Coming from #Level 1A
            {
                "scenario": "Poisoned fruits incapacitate your group. Members die alone from neglect and cliff falls. Game Over 1",
                "choices": ["end_game"]
            },
            # LEVEL 2C: Look for another food source - Coming from #Level 1A
            {
                "scenario": "Your group finds a fish-filled river but lacks tools. Try hand-fishing (1) or keep searching (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2D: Enter the cave - Coming from #Level 1B and 1C
            {
                "scenario": "The cave houses a bear! Fight it (1) or flee (2)?",
                "choices": [1, 2]
            },
            # LEVEL 2E: Death by separation - Coming from #Level 1C
            {
                "scenario": "Cave explorers die by bear attack; others vanish mysteriously in the forest. Game Over 2",
                "choices": ["end_game"]
            },
            # LEVEL 2F: Dual death - Coming from #Level 1B
            {
                "scenario": "Fruit-eaters die from poison; cave group is mauled by a bear. Game Over 3",
                "choices": ["end_game"]
            },
            # LEVEL 2G: Radio rescue - Coming from #Level 1C
            {
                "scenario": "Your group finds an abandoned radio shelter and calls for rescue. Game Over 4",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 3
            # ------------------------------
            # LEVEL 3A: Look for help - Coming from #Level 2A
            {
                "scenario": "A hermit offers poisoned members medicine in exchange for swamp herb gathering. Accept (1) or refuse (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3B: Death by cliff - Coming from #Level 2A
            {
                "scenario": "Your group gets lost in the jungle. Antidote seekers plummet off a cliff. Game Over 5",
                "choices": ["end_game"]
            },
            # LEVEL 3C: Look for antidote - Coming from #Level 2A
            {
                "scenario": "A member falls into a venomous pit. Escape recklessly (1) or search for safe exits (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3D: Fish with hands - Coming from #Level 2C
            {
                "scenario": "Using a makeshift spear, your group tries fishing. Use it (1) or abandon it (2)?",
                "choices": [1, 2]
            },
            # LEVEL 3E: Death by discussion - Coming from #Level 2C
            {
                "scenario": "Arguments distract your group—a bear ambushes and kills everyone. Game Over 6",
                "choices": ["end_game"]
            },
            # LEVEL 3F: Death by natural trap - Coming from #Level 2C
            {
                "scenario": "Your group triggers a hidden pit trap. All perish. Game Over 7",
                "choices": ["end_game"]
            },
            # LEVEL 3G: Successful defense - Coming from #Level 2D
            {
                "scenario": "Your group scares the bear with sticks and finds a flare gun. Rescue follows! Game Over 8",
                "choices": ["end_game"]
            },
            # LEVEL 3H: Death by fleeing - Coming from #Level 2D
            {
                "scenario": "Fleeing fails—the bear slaughters your group. Game Over 9",
                "choices": ["end_game"]
            },
            # LEVEL 3I: Death by separation - Coming from #Level 2D
            {
                "scenario": "Brave defenders die fighting the bear; fleeing members fall into fatal traps. Game Over 10",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 4
            # ------------------------------
            # LEVEL 4A: Get out of the pit - Coming from #Level 3C
            {
                "scenario": "Your group escapes the pit, but infection spreads. Prioritize rescue signals (1) or shelter (2)?",
                "choices": [1, 2]
            },
            # LEVEL 4B: Stay in the pit - Coming from #Level 3C
            {
                "scenario": "Your group stays in the pit and finds ancient symbols. Explore passage (1) or wait (2)?",
                "choices": [1, 2]
            },
            # LEVEL 4C: Death by different options - Coming from #Level 3C
            {
                "scenario": "Separating kills some via isolation, others via poison. Game Over 11",
                "choices": ["end_game"]
            },
            # LEVEL 4D: Death in the swamp - Coming from #Level 3A
            {
                "scenario": "Swamp creatures annihilate your group. Game Over 12",
                "choices": ["end_game"]
            },
            # LEVEL 4E: Death by poison - Coming from #Level 3A
            {
                "scenario": "Rejecting the hermit’s cure, poison kills everyone by dawn. Game Over 13",
                "choices": ["end_game"]
            },
            # LEVEL 4F: Death by separation - Coming from #Level 3A
            {
                "scenario": "Splitting up traps some; others die from poison. Game Over 14",
                "choices": ["end_game"]
            },
            # LEVEL 4G: Adaptation to the island - Coming from #Level 3D
            {
                "scenario": "Catching fish revitalizes your group—you adapt to island life permanently. Game Over 15",
                "choices": ["end_game"]
            },
            # LEVEL 4H: Death in the jungle - Coming from #Level 3D
            {
                "scenario": "Separating causes jungle disappearances and bear attacks. Game Over 16",
                "choices": ["end_game"]
            },
            # LEVEL 4I: Both choose different things - Coming from 3D
            {
                "scenario": "Mismatched choices lead to jungle deaths. Game Over 3",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 5
            # ------------------------------
            # LEVEL 5A: Death by poison - Coming from #Level 4A
            {
                "scenario": "Poison claims your entire group by dawn. Game Over 17",
                "choices": ["end_game"]
            },
            # LEVEL 5B: Death by trap - Coming from #Level 4A
            {
                "scenario": "Natural traps kill some; poison finishes the rest. Game Over 18",
                "choices": ["end_game"]
            },
            # LEVEL 5C: Explore ruins - Coming from #Level 4A
            {
                "scenario": "Your group finds medicinal plants and ancient ruins. Explore ruins (1) or focus on survival (2)?",
                "choices": [1, 2]
            },
            # LEVEL 5D: Explore passage - Coming from #Level 4B
            {
                "scenario": "A temple entity offers immortality for souls. Accept (1) or flee (2)?",
                "choices": [1, 2]
            },
            # LEVEL 5E: Death by waiting - Coming from #Level 4B
            {
                "scenario": "Your group dies waiting for rescue. Game Over 19",
                "choices": ["end_game"]
            },
            # LEVEL 5F: Death in the passage - Coming from #Level 4B
            {
                "scenario": "Half die from poison; others vanish in the passage. Game Over 20",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 6
            # ------------------------------
            # LEVEL 6A: Accept entity's deal - Coming from #Level 5D
            {
                "scenario": "One gains immortality; others become cursed ghosts. Game Over 21",
                "choices": ["end_game"]
            },
            # LEVEL 6B: Reject entity's deal - Coming from #Level 5D
            {
                "scenario": "The entity transforms your group into mindless boars. Game Over 22",
                "choices": ["end_game"]
            },
            # LEVEL 6C: Explore ruins - Coming from #Level 5C
            {
                "scenario": "A voice offers forbidden knowledge. Accept (1) or reject (2)?",
                "choices": [1, 2]
            },
            # LEVEL 6D: Continue exploring - Coming from #Level 5C
            {
                "scenario": "Your group finds a mountain path. Climb (1) or return to camp (2)?",
                "choices": [1, 2]
            },
            # LEVEL 6E: Death in the ruins - Coming from #Level 5C
            {
                "scenario": "Separating kills some in ruins, others via bears. Game Over 23",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 7
            # ------------------------------
            # LEVEL 7A: Accept voice's deal - Coming from #Level 6C
            {
                "scenario": "Your group becomes immortal island guardians. Game Over 24",
                "choices": ["end_game"]
            },
            # LEVEL 7B: Reject voice's deal - Coming from #Level 6C
            {
                "scenario": "Rejecting the deal kills your group instantly. Game Over 25",
                "choices": ["end_game"]
            },
            # LEVEL 7C: Guardian's betrayal - Coming from #Level 6C
            {
                "scenario": "One betrays the group to become guardian, murdering others. Game Over 26",
                "choices": ["end_game"]
            },
            # LEVEL 7D: Follow the path - Coming from #Level 6D
            {
                "scenario": "Your group finds a freshwater spring. Stay (1) or explore further (2)?",
                "choices": [1, 2]
            },
            # LEVEL 7E: Return to shelter - Coming from #Level 6D
            {
                "scenario": "Improving your shelter, your group adapts to island life forever. Game Over 27",
                "choices": ["end_game"]
            },
            # LEVEL 7F: Explore and adapt - Coming from #Level 6D
            {
                "scenario": "Half build a raft and escape; others stay as permanent residents. Game Over 28",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 8
            # ------------------------------
            # LEVEL 8A: Stay near the spring - Coming from #Level 7D
            {
                "scenario": "Your group stays by the spring. Hunt food (1) or try fishing (2)?",
                "choices": [1, 2]
            },
            # LEVEL 8B: Final rescue - Coming from #Level 7D
            {
                 "scenario": "Your group repairs a stranded boat and escapes. Rescued weeks later! Game Over 29",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 9
            # ------------------------------
            # LEVEL 9A: Look for food - Coming from #Level 8A
            {
                "scenario": "Your group finds strange fruits. Risk eating (1) or keep searching (2)?",
                "choices": [1, 2]
            },
            # LEVEL 9B: Try fishing - Coming from #Level 8A
            {
                "scenario": "No fish here, but a stream appears. Follow it (1) or return (2)?",
                "choices": [1, 2]
            },
            # LEVEL 9C: Adaptation and rescue - Coming from #Level 8A
            {
                "scenario": "Half adapt via fishing; others escape by boat. Game Over 30",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 10
            # ------------------------------
            # LEVEL 10A: Deadly hallucinations - Coming from #Level 9A
            {
                "scenario": "Hallucinogenic fruits drive your group to mutual slaughter. Game Over 31",
                "choices": ["end_game"]
            },
            # LEVEL 10B: Definitive adaptation - Coming from #Level 9A
            {
                "scenario": "Bird eggs help your group thrive permanently. Game Over 32",
                "choices": ["end_game"]
            },
            # LEVEL 10C: Suicide by hallucinations - Coming from #Level 9A
            {
                "scenario": "One hallucinates, kills companions, then suicides. Game Over 33",
                "choices": ["end_game"]
            },
            # LEVEL 10D: Explore hidden cave - Coming from #Level 9B
            {
                "scenario": "Following the stream reveals a waterfall cave. Explore (1) or retreat (2)?",
                "choices": [1, 2]
            },
            # LEVEL 10E: Peaceful life - Coming from #Level 9B
            {
                "scenario": "Your group builds a peaceful island life. Game Over 34",
                "choices": ["end_game"]
            },
            # LEVEL 10F: Both choose to return to shelter - Coming from 9B
            {
                "scenario": "Staying on the beach leads to permanent adaptation. Game Over 18",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 11
            # ------------------------------
            # LEVEL 11A: Touch the altar - Coming from #Level 10D
            {
                "scenario": "Your group finds an altar with glowing symbols. Touch it (1) or ignore (2)?",
                "choices": [1, 2]
            },
            # LEVEL 11B: Death in the cave - Coming from #Level 10D
            {
                "scenario": "Half adapt to the island; others vanish in the cave. Game Over 35",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 12
            # ------------------------------
            # LEVEL 12A: Infinite knowledge - Coming from #Level 11A
            {
                "scenario": "A voice offers infinite knowledge for eternal service. Accept (1) or reject (2)?",
                "choices": [1, 2]
            },
            # LEVEL 12B: Rescue by bonfire - Coming from #Level 11A
            {
                "scenario": "A ship appears on the horizon! Light a bonfire (1) or wait (2)?",
                "choices": [1, 2]
            },
            # LEVEL 12C: Deadly trap - Coming from #Level 11A
            {
                "scenario": "One vanishes at the altar; others die in traps. Game Over 36",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 13
            # ------------------------------
            # LEVEL 13A: Cosmic immortality - Coming from #Level 12A
            {
                "scenario": "Your group ascends to cosmic immortality. Game Over 37",
                "choices": ["end_game"]
            },
            # LEVEL 13B: Escape from the cave - Coming from #Level 12A
            {
                "scenario": "The enraged entity collapses the cave. Run (1) or find another exit (2)?",
                "choices": [1, 2]
            },
            # LEVEL 13C: Final rescue - Coming from #Level 12B
            {
                "scenario": "The ship rescues your group! Game Over 38",
                "choices": ["end_game"]
            },
            # ------------------------------
            # LEVEL 14
            # ------------------------------
            # LEVEL 14A: Arid desert - Coming from #Level 13B
            {
                "scenario": "Your group escapes to a lifeless desert. Game Over 39",
                "choices": ["end_game"]
            },
            # LEVEL 14B: Rescue at sea - Coming from #Level 13B
            {
                "scenario": "A hidden tunnel leads to a raft-building opportunity. Escape succeeds! Game Over 40",
                "choices": ["end_game"]
            },
            # LEVEL 14C: Death in the cave - Coming from #Level 13B
            {
                "scenario": "Cave collapse buries your group forever. Game Over 41",
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
