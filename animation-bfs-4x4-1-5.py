import time
import tkinter as tk
from collections import deque

DIRECTIONS = {
    "top": (-1, 0, 0),
    "right": (0, 1, 1),
    "bottom": (1, 0, 2),
    "left": (0, -1, 3)
}
DIRECTION_ORDER = ["top", "right", "bottom", "left"]

class Cell:
    def __init__(self):
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False
        self.visible = False

def read_maze_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.replace("\t", "    ").rstrip() for line in f.readlines()]

    print(f"Total lines: {len(lines)}")
    for i, line in enumerate(lines):
        print(f"Line {i}: {repr(line)} (length: {len(line)})")

    max_length = max(len(line) for line in lines)
    lines = [line.ljust(max_length) for line in lines]

    rows = (len(lines) - 1) // 2  
    cols = (max(len(line) for line in lines) - 1) // 4  
    print(f"Detected maze size: {rows}x{cols}")

    maze = [[Cell() for _ in range(cols)] for _ in range(rows)]
    start, goal = None, set()

    for r in range(rows):
        for c in range(cols):
            x, y = r * 2 + 1, c * 4 + 2

            if x >= len(lines) or y >= len(lines[x]):
                continue

            if lines[x][y] == 'S':
                start = (r, c)
                print(f"Start position found at: {start}")

            elif lines[x][y] == 'G':
                goal.add((r, c))

            if lines[x - 1][y] == '-':  
                maze[r][c].walls[0] = True
            else:
                maze[r][c].walls[0] = False

            if lines[x + 1][y] == '-':  
                maze[r][c].walls[2] = True
            else:
                maze[r][c].walls[2] = False

            if lines[x][y - 2] == '|':  
                maze[r][c].walls[3] = True
            else:
                maze[r][c].walls[3] = False

            if lines[x][y + 2] == '|':  
                maze[r][c].walls[1] = True
            else:
                maze[r][c].walls[1] = False

    if start is None:
        print("Maze content:")
        for line in lines:
            print(repr(line))
        raise ValueError("Không tìm thấy vị trí xuất phát 'S' trong tệp mê cung!")

    return maze, start, goal

def bfs_micromouse(maze, start, goal, animation):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, "top")])
    visited = set([start])
    parent = {start: None}
    direction_map = {}
    path_taken = []
    
    animation.robot_position = start
    animation.update_display()

    print("Robot path:")
    current_pos = start
    while queue:
        (x, y), direction = queue.popleft()
        
        # Kiểm tra nếu current_pos có parent hợp lệ trước khi backtracking
        while current_pos != (x, y):
            if parent.get(current_pos) is None:
                break
            prev_x, prev_y = parent[current_pos]
            print(f"{current_pos} -> ({prev_x}, {prev_y}) (backtracking)")
            current_pos = (prev_x, prev_y)
        
        print(f"{current_pos} -> ({x}, {y}) via {direction}")
        current_pos = (x, y)
        
        path_taken.append((x, y))
        maze[x][y].visited = True  
        maze[x][y].visible = True
        animation.robot_position = (x, y)
        animation.update_display()
        time.sleep(animation.speed)
        
        if (x, y) in goal:
            break

        for new_direction in DIRECTION_ORDER:
            dx, dy, wall_idx = DIRECTIONS[new_direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not maze[x][y].walls[wall_idx]:  
                    if (nx, ny) not in visited:
                        queue.append(((nx, ny), new_direction))
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        direction_map[(nx, ny)] = new_direction
    
    print("Full path taken (including backtracking):")
    for i in range(len(path_taken) - 1):
        print(f"{path_taken[i]} -> {path_taken[i+1]}")

    path = []
    node = next((p for p in goal if p in parent), None)
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    if path:
        animation.update_display(path)

    return path if path else None




class MazeAnimation:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = 50
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.robot_position = None
        self.speed = 0.5

        self.window = tk.Tk()
        self.window.title("Micromouse BFS - 4x4 Maze")
        self.canvas = tk.Canvas(self.window, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="black")
        self.canvas.pack()
        
        self.speed_scale = tk.Scale(self.window, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, label="Speed")
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()
    
    def update_display(self, path=None):
        self.speed = self.speed_scale.get()
        self.canvas.delete("all")
        
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                if not self.maze[r][c].visible:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

                if path and (r, c) in path:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="gray")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                
                for i, wall in enumerate(self.maze[r][c].walls):
                    if wall:
                        if i == 0:
                            self.canvas.create_line(x1, y1, x2, y1, fill="black", width=2)
                        elif i == 1:
                            self.canvas.create_line(x2, y1, x2, y2, fill="black", width=2)
                        elif i == 2:
                            self.canvas.create_line(x1, y2, x2, y2, fill="black", width=2)
                        elif i == 3:
                            self.canvas.create_line(x1, y1, x1, y2, fill="black", width=2)
        
        if self.robot_position:
            rx, ry = self.robot_position
            cx, cy = ry * self.cell_size + self.cell_size // 2, rx * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="yellow")

        self.window.update()

filename = "mazefiles-master/classic/minh_001.txt"
maze, start, goal = read_maze_from_file(filename)

animation = MazeAnimation(maze)
bfs_micromouse(maze, start, goal, animation)
animation.window.mainloop()