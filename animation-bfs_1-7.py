import time
import tkinter as tk
from collections import deque

# 4 hướng di chuyển: (x, y)
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
        self.visible = False  # Chưa nhìn thấy

def read_maze_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    rows = len(lines) // 2
    cols = (len(lines[0]) + 1) // 4
    maze = [[Cell() for _ in range(cols)] for _ in range(rows)]
    start, goal = None, set()

    for r in range(rows):
        for c in range(cols):
            x, y = r * 2 + 1, c * 4 + 2
            
            if lines[x][y] == 'S':
                start = (r, c)
            elif lines[x][y] == 'G':
                goal.add((r, c))

            if lines[x - 1][y] == '-':  # Tường trên
                maze[r][c].walls[0] = True
            else:
                maze[r][c].walls[0] = False

            if lines[x + 1][y] == '-':  # Tường dưới
                maze[r][c].walls[2] = True
            else:
                maze[r][c].walls[2] = False

            if lines[x][y - 2] == '|':  # Tường trái
                maze[r][c].walls[3] = True
            else:
                maze[r][c].walls[3] = False

            if lines[x][y + 2] == '|':  # Tường phải
                maze[r][c].walls[1] = True
            else:
                maze[r][c].walls[1] = False

    return maze, start, goal

def bfs_micromouse(maze, start, goal, animation):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, "top")])  # Hướng ban đầu là top
    visited = set([start])
    parent = {start: None}
    direction_map = {}
    
    animation.robot_position = start
    animation.update_display()

    while queue:
        (x, y), direction = queue.popleft()
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

    path = []
    node = next((p for p in goal if p in parent), None)
    while node is not None:
        path.append((node, direction_map.get(node, "top")))
        node = parent[node]
    path.reverse()

    return path if path else None

class MazeAnimation:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = 30  
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.robot_position = None
        self.speed = 0.1

        self.window = tk.Tk()
        self.window.title("Micromouse BFS - Dark Mode")
        self.canvas = tk.Canvas(self.window, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="black")
        self.canvas.pack()
        
        self.speed_scale = tk.Scale(self.window, from_=0.01, to=0.5, resolution=0.01, orient=tk.HORIZONTAL, label="Speed")
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()
    
    def update_display(self):
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
                    if self.maze[r][c].walls[0]:  
                        self.canvas.create_line(x1, y1, x2, y1, fill="black", width=2)
                    if self.maze[r][c].walls[1]:  
                        self.canvas.create_line(x2, y1, x2, y2, fill="black", width=2)
                    if self.maze[r][c].walls[2]:  
                        self.canvas.create_line(x1, y2, x2, y2, fill="black", width=2)
                    if self.maze[r][c].walls[3]:  
                        self.canvas.create_line(x1, y1, x1, y2, fill="black", width=2)
        
        if self.robot_position:
            rx, ry = self.robot_position
            cx, cy = ry * self.cell_size + self.cell_size // 2, rx * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="yellow")
        
        self.window.update()

filename = "mazefiles-master/classic/13ye.txt"
maze, start, goal = read_maze_from_file(filename)

animation = MazeAnimation(maze)
bfs_micromouse(maze, start, goal, animation)
animation.window.mainloop()
