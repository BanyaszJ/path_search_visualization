# Dungeon Crawler BFS Visualizer

A real-time visualization of the Breadth-First Search (BFS) pathfinding algorithm using Pygame. This interactive tool demonstrates how BFS explores a grid-based maze to find the shortest path between two points.

## Features

- **Real-time BFS visualization**: Watch the algorithm explore the maze step by step
- **Interactive maze editing**: Draw walls by clicking and dragging with the left mouse button
- **Path reconstruction**: Visualizes the shortest path once the target is found
- **Live statistics**: Shows queue depth and number of visited cells
- **Grid-based interface**: Clean, easy-to-understand visual representation

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Install Python 3.x from [python.org](https://python.org)
2. Install Pygame:
   ```bash
   pip install pygame
   ```

## Usage

1. Run the program:
   ```bash
   python bfs_visualizer.py
   ```

2. The visualizer will open with:
   - **Green square**: Start position (top-left area)
   - **Red square**: End position (bottom-right area)
   - **Black background**: Empty, traversable space
   - **White squares**: Walls (obstacles)

## Controls

| Key/Action | Function |
|------------|----------|
| **Enter** | Toggle automatic stepping on/off |
| **R** | Reset the algorithm and clear the maze |
| **Left Mouse Button** | Draw walls by clicking and dragging |

## Visual Legend

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Start position |
| 🔴 **Red** | End/target position |
| 🟡 **Yellow** | Visited cells |
| 🔵 **Blue** | Current position being explored |
| 🟣 **Purple** | Final shortest path (when found) |
| ⬜ **White** | Walls/obstacles |
| ⬛ **Black** | Empty traversable space |

## How It Works

The BFS algorithm works by:

1. Starting from the green start position
2. Exploring all neighboring cells (up, down, left, right) 
3. Adding unexplored neighbors to a queue
4. Processing cells in First-In-First-Out (FIFO) order
5. Tracking parent relationships to reconstruct the path
6. Continuing until the red target is found

### Algorithm Properties

- **Completeness**: Will always find a path if one exists
- **Optimality**: Guarantees the shortest path in unweighted grids
- **Time Complexity**: O(V + E) where V is vertices and E is edges
- **Space Complexity**: O(V) for the queue and visited set


## Educational Use

This visualizer is perfect for:

- Learning pathfinding algorithms
- Understanding BFS traversal patterns
- Comparing different search strategies
- Teaching graph theory concepts
- Demonstrating algorithm efficiency

## Performance Notes

- Grid size: 40×30 cells (with default settings)
- Runs at 120 FPS for smooth visualization
- Step delay: 0.02 seconds in automatic mode
- Memory efficient with deque-based queue implementation

## Potential Enhancements

- Add A* algorithm comparison
- Implement diagonal movement
- Support for weighted edges
- Save/load maze configurations
- Multiple start/end points

## License

This project is open source and available for educational purposes.
