import pygame
import sys
import time
from collections import deque

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
ROWS = WINDOW_HEIGHT // CELL_SIZE
COLS = WINDOW_WIDTH // CELL_SIZE

WHITE = (255, 255, 255)  # Walls
BLACK = (0, 0, 0)  # misc
GREEN = (0, 255, 0)  # Start
RED = (255, 0, 0)  # End
BLUE = (0, 0, 255)  # Current position
YELLOW = (255, 255, 0)  # Visited
PURPLE = (128, 0, 128)  # Path
GRAY = (200, 200, 200)  # Grid lines
LIGHTER_GRAY = (80, 80, 80)  # Empty space


class BFSVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dungeon crawler BFS Visualizer")
        self.clock = pygame.time.Clock()
        self.maze = self.create_maze()

        self.mouse_lmb = 1
        self.mouse_rmb = 3
        self.rmb_down_state = False
        self.lmb_down_state = False

        # print(self.maze)
        self.start = (5, 5)
        self.end = (ROWS - 5, COLS - 5)

        # BFS attrs
        self.visited = set()
        self.queue = deque([self.start])
        self.parent = {}
        self.current = None
        self.found_path = []
        self.algorithm_complete = False

    def add_to_maze(self, row, col, value):
        """Add a value to the maze at the specified row and column"""
        if 0 <= row < ROWS and 0 <= col < COLS:
            self.maze[row][col] = value

    @staticmethod
    def create_maze():
        """Create an example maze with walls (1) and open spaces (0)"""
        maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        return maze

    def get_neighbors(self, row, col):
        """Get valid neighbors (up, down, left, right)"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < ROWS and
                0 <= new_col < COLS and
                self.maze[new_row][new_col] == 0 and
                (new_row, new_col) not in self.visited):
                neighbors.append((new_row, new_col))

        return neighbors

    def reconstruct_path(self):
        """Reconstruct the path from start to end using parent tracking"""
        path = []
        current = self.end
        while current is not None:
            path.append(current)
            current = self.parent.get(current)
        return path[::-1]

    def bfs_step(self):
        """Perform one step of BFS"""
        if not self.queue or self.algorithm_complete:
            return False

        self.current = self.queue.popleft()
        self.visited.add(self.current)

        # Check if we reached the goal
        if self.current == self.end:
            self.found_path = self.reconstruct_path()
            self.algorithm_complete = True
            return True

        # Add neighbors to queue
        neighbors = self.get_neighbors(self.current[0], self.current[1])
        for neighbor in neighbors:
            if neighbor not in self.visited and neighbor not in self.queue:
                self.queue.append(neighbor)
                self.parent[neighbor] = self.current

        return True

    def draw_maze(self):
        self.screen.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                if self.maze[row][col] == 1:  # Wall
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                else:  # Empty space
                    pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw visited cells
                if (row, col) in self.visited:
                    pygame.draw.rect(self.screen, YELLOW, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

                # Draw current position
                if self.current and (row, col) == self.current:
                    pygame.draw.rect(self.screen, BLUE, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

                # Draw start position
                if (row, col) == self.start:
                    pygame.draw.rect(self.screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw end position
                if (row, col) == self.end:
                    pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw final path if found
                if self.algorithm_complete and (row, col) in self.found_path:
                    pygame.draw.rect(self.screen, PURPLE, (x+4, y+4, CELL_SIZE-8, CELL_SIZE-8))

        # Draw grid lines
        for i in range(ROWS + 1):
            pygame.draw.line(self.screen, LIGHTER_GRAY, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(self.screen, LIGHTER_GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_HEIGHT))

    def draw_info(self):
        """Draw information about the algorithm"""
        font = pygame.font.Font(None, 24)
        info_texts = [
            f"Queue depth: {len(self.queue)}",
            f"Visited cells: {len(self.visited)}",
        ]

        y_offset = 10
        for text in info_texts:
            color = BLACK
            rendered = font.render(text, True, color)
            text_rect = rendered.get_rect()
            pygame.draw.rect(self.screen, WHITE, (10, y_offset, text_rect.width + 10, text_rect.height + 5))
            self.screen.blit(rendered, (15, y_offset + 2))
            y_offset += 25

    def run(self):
        """Main game loop"""
        running = True
        auto_step = False
        step_delay = 0.02
        last_step_time = 0

        while running:
            current_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == self.mouse_lmb:
                        self.lmb_down_state = True
                    if event.button == self.mouse_rmb:
                        self.rmb_down_state = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == self.mouse_lmb:
                        self.lmb_down_state = False
                    if event.button == self.mouse_rmb:
                        self.rmb_down_state = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Toggle auto-step
                        auto_step = not auto_step
                    elif event.key == pygame.K_r:  # Reset
                        self.visited.clear()
                        self.queue = deque([self.start])
                        self.parent = {}
                        self.current = None
                        self.found_path = []
                        self.algorithm_complete = False
                        auto_step = False
                        self.maze = self.create_maze()

                if not auto_step:
                    if self.lmb_down_state:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                        self.add_to_maze(grid_y, grid_x, 1)

            # Auto-step if enabled
            if auto_step and current_time - last_step_time > step_delay:
                self.bfs_step()
                last_step_time = current_time

            # Draw everything
            self.draw_maze()
            self.draw_info()

            # Draw controls
            font = pygame.font.Font(None, 20)
            controls = [
                "Enter: Start/stop",
                "R: Reset",
            ]

            y_offset = WINDOW_HEIGHT - 50
            for control in controls:
                rendered = font.render(control, True, BLACK)
                text_rect = rendered.get_rect()
                pygame.draw.rect(self.screen, WHITE, (10, y_offset, text_rect.width + 10, text_rect.height + 5))
                self.screen.blit(rendered, (15, y_offset + 2))
                y_offset += 22

            pygame.display.flip()
            self.clock.tick(120)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    visualizer = BFSVisualizer()
    visualizer.run()
