# space-shooter

A top-down space shooter prototype built with Pygame. The player moves left and right, shoots automatically, destroys enemies for score, and restarts after game over.

## Features

- Continuous enemy spawning
- Automatic shooting with cooldown
- Collision detection between bullets and enemies
- Score tracking
- Game over state with restart support

## Controls

- Left / Right Arrow or A / D: Move
- R: Restart after game over

## Tech Stack

- Python
- Pygame

## Local Setup

1. Install dependencies.

```bash
pip install -r requirements.txt
```

2. Run the game.

```bash
python src/main.py
```

## Project Structure

```text
.
├── README.md
├── requirements.txt
└── src/
	└── main.py
```

## Notes

- This is a compact prototype and a good base for adding power-ups, sound, boss enemies, and a start screen.
