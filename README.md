# Peer-to-peer-Survivor-Decision-Game

## Proyect Overview

The Peer-to-Peer Decision-Making Game is a multiplayer survival game where two players stranded on a deserted island must collaborate to make decisions that affect the story. Players manage resources, face challenges, and communicate in real-time via a local network using P2P architecture, with handling for disconnections.

## Features

-**P2P Comunication**: Real-time communication between players over a local network.
-**Dynamic Storyline**: Players make choices that affect the story, leading to different outcomes and multiple possible endings.
-**Survival Challenges**: Players face challenges such as natural disasters, health risks, and the need to collaborate or compete.
-**Disconnection Handling**: The system gracefully handles unexpected network issues such as disconnections or network partitions.

## Project Structure

- **/docs**: Project documentation, including the final report.
- **/src**: Source code for the game, including communication and game logic.
- **/tests**: Unit tests for the communication and game logic.
- **README.md**: Project documentation and instructions for setup.

## Installation 💻

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/Peer-to-peer-Survivor-Decision-Game.git

# Navigate to project directory
cd Peer-to-peer-Survivor-Decision-Game/src

# Install dependencies
pip install -r requirements.txt
```


### Game Flow
Initial Setup

Both players will see the connection status:
```bash
Waiting for connection on localhost:5000...
Connected to peer at 127.0.0.1:5001
```
Scenario Presentation

The game will display the current scenario:
```bash
==================================================
Your ship has been wrecked by a storm...
You must act fast: search for food (1) or look for shelter (2).
==================================================
```

Making Decisions

Each player will be prompted:
```bash
Your decision (1/2): 
```
Enter your choice (1 or 2) and press Enter.


Waiting for Peer

After submitting your choice, the game will wait for the other player:
```bash
Waiting for the other player's decision...
```
Outcome Display

Once both players have made their choices, the result is shown:
```bash
==================================================
Your choice: 1
Other player's choice: 2
==================================================
```

The game will then display the outcome of the combined decisions.

Progression

The game will automatically advance to the next scenario based on the players' choices.

### ENJOY THE 41 DIFFERENTS ENDINGS