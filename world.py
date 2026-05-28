EMPTY = '.'
WALL = '#'
PLAYER = '@'
KEY = 'K'
DOOR = 'D'

DIRECTIONS = {
    'north': (-1, 0),
    'south': (1, 0),
    'east':  (0, 1),
    'west':  (0, -1),
}

LEVEL = [
    "#######",
    "#@....#",
    "#.###.#",
    "#.#K..#",
    "#.###.#",
    "#....D#",
    "#######",
]

class World:
    def __init__(self):
        self.grid = [list(row) for row in LEVEL]
        self.player_row = 0
        self.player_col = 0
        self.inventory = []
        self.goal_achieved = False
        self.message = ""
        self.steps = 0

        # Find player starting position
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == PLAYER:
                    self.player_row = r
                    self.player_col = c
                    self.grid[r][c] = EMPTY

    def apply_action(self, action):
        self.steps += 1
        action = action.strip().lower()

        if action in DIRECTIONS:
            dr, dc = DIRECTIONS[action]
            nr, nc = self.player_row + dr, self.player_col + dc

            cell = self.grid[nr][nc]

            if cell == WALL:
                self.message = "Blocked by a wall."
            elif cell == DOOR:
                if KEY in self.inventory:
                    self.grid[nr][nc] = EMPTY
                    self.player_row, self.player_col = nr, nc
                    self.goal_achieved = True
                    self.message = "You used the key to open the door! Goal achieved!"
                else:
                    self.message = "The door is locked. You need a key."
            else:
                self.player_row, self.player_col = nr, nc
                self.message = f"Moved {action}."
                # Auto pick up key if stepped on it
                if self.grid[self.player_row][self.player_col] == KEY:
                    self.inventory.append(KEY)
                    self.grid[self.player_row][self.player_col] = EMPTY
                    self.message = f"Moved {action} and picked up the key!"

        elif action == "pick_up":
            cell = self.grid[self.player_row][self.player_col]
            if cell == KEY:
                self.inventory.append(KEY)
                self.grid[self.player_row][self.player_col] = EMPTY
                self.message = "Picked up the key!"
            else:
                self.message = "Nothing to pick up here."

        else:
            self.message = f"Unknown action: {action}"

        return self.message

    def get_observation(self):
        # Returns currently visible cells as absolute (row, col) grid positions.
        # Also returns player position, inventory, last message, and passable directions.
        visible = {}

        for direction in DIRECTIONS:
            focus = (self.player_row, self.player_col)
            while True:
                # Add 3x3 neighbourhood of focus point to visible cells
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = focus[0] + dr, focus[1] + dc
                        if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                            visible[(nr, nc)] = self.grid[nr][nc]

                # Move focus forward, stop at walls or out of bounds
                try:
                    next_r = focus[0] + DIRECTIONS[direction][0]
                    next_c = focus[1] + DIRECTIONS[direction][1]
                    if self.grid[next_r][next_c] == WALL:
                        break
                    focus = (next_r, next_c)
                except:
                    break

        # Work out which directions are passable from current position
        passable = []
        for direction, (dr, dc) in DIRECTIONS.items():
            nr, nc = self.player_row + dr, self.player_col + dc
            if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                if self.grid[nr][nc] != WALL:
                    passable.append(direction)

        return {
            "visible": visible,
            "player_pos": (self.player_row, self.player_col),
            "inventory": list(self.inventory) if self.inventory else [],
            "last_message": self.message,
            "passable_directions": passable,
        }
