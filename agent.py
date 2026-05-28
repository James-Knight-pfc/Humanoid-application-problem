from groq import Groq
import re

class Agent:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.memory = {}       # {(row, col): cell_content} — builds up over time
        self.history = []      # conversation history so the model remembers previous moves
        self.first_turn = True

    def _render_map(self, player_pos):
        # Render the agent's known map as ASCII, with ? for unexplored cells
        if not self.memory:
            return "No map data yet."

        rows = [r for r, c in self.memory]
        cols = [c for r, c in self.memory]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        lines = []
        for r in range(min_r, max_r + 1):
            line = ""
            for c in range(min_c, max_c + 1):
                if (r, c) == player_pos:
                    line += "@"
                elif (r, c) in self.memory:
                    line += self.memory[(r, c)]
                else:
                    line += "?"
            lines.append(line)
        return "\n".join(lines)

    def format_observation(self, obs):
        player_pos = obs["player_pos"]
        inventory = obs["inventory"] if obs["inventory"] else ["empty"]
        map_str = self._render_map(player_pos)

        observation = f"""Map (@ = you, K = key, D = door, # = wall, . = empty, ? = unexplored):
{map_str}

Inventory: {inventory}
Last action result: {obs['last_message']}
You can move: {obs['passable_directions']}
Available actions: north, south, east, west, pick_up
One sentence of reasoning, then end with: ACTION: <action>"""

        if self.first_turn:
            self.first_turn = False
            return f"""You are an agent in a 2D grid world. Choose 1 action per turn.
Goal: Find the key (K), pick it up by moving onto it, then walk into the door (D) to win.
You cannot pass through walls (#). You are represented by @. The key is represented by K.
North is up, south is down, east is right, west is left.
Unexplored areas are shown as ?. Explore to find the key and door.
You have a 300 token limit so dont go above that.
{observation}"""

        return observation

    def choose_action(self, obs):
        # Merge newly visible cells into memory
        for pos, cell in obs["visible"].items():
            self.memory[pos] = cell
        # Mark player's own cell as empty in memory (not as @ symbol)
        self.memory[obs["player_pos"]] = EMPTY = "."

        print("Calling Groq...")
        prompt = self.format_observation(obs)
        print(prompt)

        self.history.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=self.history
        )
        text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": text})

        match = re.search(r'ACTION:\s*(\w+)', text, re.IGNORECASE)
        if match:
            action = match.group(1).lower()
        else:
            action = "look"

        return action, text
