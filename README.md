# LLM Agent in a Virtual World

An LLM agent that navigates a 2D grid world, explores its surroundings, and completes a goal - find a key and use it to open a door.

## How It Works

- **world.py** - the grid environment, movement logic, and line-of-sight visibility
- **agent.py** - the agent. Calls a Groq LLM each turn, builds a memory map from what it's seen, and picks an action
- **main.py** - runs the game loop and renders everything with pygame

Each turn the agent gets an ASCII map of what it's explored so far, its inventory, what happened last turn, and which directions it can actually move. It reasons and picks an action.

## Design Choices

**Line-of-sight** - the agent only sees what's visible in straight lines from where it's standing. Walls block vision so it has to explore.

**Memory map** - cells the agent has seen are remembered across turns so it can plan even when they're out of view. Unseen cells show as `?`.

**Conversation history** - the full conversation history is sent to the LLM each turn so it remembers what it's already tried.

**ASCII map** - sending the observation as a visual grid works much better than raw coordinates for spatial reasoning.

## Setup

pip install pygame groq

Get a free Groq API key at console.groq.com

## Run

python main.py

You'll be asked for your Groq API key when it starts.

## Legend
`@` = agent, `K` = key, `D` = door, `#` = wall, `.` = empty, `?` = unexplored
