import pygame
import sys
from world import World
from agent import Agent

# Display settings
TILE_SIZE = 50
FPS = 5

# Colours
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GREY   = (100, 100, 100)
YELLOW = (255, 255, 0)
BLUE   = (0,   100, 255)
BROWN  = (139, 69,  19)

def draw_world(screen, world):
    grid = world.grid
    player_row = world.player_row
    player_col = world.player_col

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if cell == '#':
                colour = GREY
            elif cell == 'K':
                colour = YELLOW
            elif cell == 'D':
                colour = BROWN
            else:
                colour = WHITE

            pygame.draw.rect(screen, colour, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 1)

    # Draw player as blue circle
    px = player_col * TILE_SIZE + TILE_SIZE // 2
    py = player_row * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, BLUE, (px, py), TILE_SIZE // 3)

def main():
    api_key = input("Enter your Groq API key: ").strip()

    world = World()
    agent = Agent(api_key)

    pygame.init()
    rows = len(world.grid)
    cols = len(world.grid[0])
    screen = pygame.display.set_mode((cols * TILE_SIZE, rows * TILE_SIZE))
    pygame.display.set_caption("LLM Agent World")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_world(screen, world)
        pygame.display.flip()

        if not world.goal_achieved:
            obs = world.get_observation()
            action, reasoning = agent.choose_action(obs)
            print(f"Action: {action}")
            print(f"Reasoning: {reasoning}\n")
            world.apply_action(action)
        else:
            print("🎉 GOAL ACHIEVED! The agent won!")
            pygame.display.set_caption("LLM Agent World - GOAL ACHIEVED!")
            pygame.time.wait(3000)  # show the winning state for 3 seconds
            running = False

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
