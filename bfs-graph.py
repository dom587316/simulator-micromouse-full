import time
import os
from collections import deque

# 4 hướng di chuyển: (x, y)
DIRECTIONS = {
    "top": (-1, 0, 0),
    "right": (0, 1, 1),
    "bottom": (1, 0, 2),
    "left": (0, -1, 3)
}

class Cell:
    def __init__(self):
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

def read_maze_from_file(filename):
    """Đọc mê cung từ file, xác định tường theo định dạng Processing"""
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    
    rows = len(lines) // 2
    cols = (len(lines[0]) + 1) // 4
    maze = [[Cell() for _ in range(cols)] for _ in range(rows)]
    start, goal = None, set()

    for r in range(rows):
        for c in range(cols):
            x, y = r * 2 + 1, c * 4 + 2  # Vị trí trong file
            
            # Xác định đường đi
            if lines[x][y] == 'S':
                start = (r, c)
            elif lines[x][y] == 'G':
                goal.add((r, c))

            # Xác định tường
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

def bfs_animation(maze, start, goal):
    """Thuật toán BFS với hiệu ứng dò đường từng ô một"""
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        x, y = queue.popleft()
        maze[x][y].visited = True  # Đánh dấu ô đã thăm
        print_maze_with_robot(maze, (x, y))  # Hiển thị trạng thái hiện tại
        time.sleep(0.1)  # Tạo hiệu ứng animation

        if (x, y) in goal:
            break  # Đã đến đích

        for direction, (dx, dy, wall_idx) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not maze[x][y].walls[wall_idx]:  # Kiểm tra có tường chắn không
                    if (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)

    # Truy vết đường đi
    path = []
    node = next((p for p in goal if p in parent), None)
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path if path else None

def print_maze_with_robot(maze, robot_pos):
    """In mê cung với trạng thái robot tại từng bước"""
    os.system('cls' if os.name == 'nt' else 'clear')  # Xóa màn hình để tạo hiệu ứng động
    rx, ry = robot_pos  # Vị trí hiện tại của robot
    
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if (r, c) == (rx, ry):
                print("R", end=" ")  # In vị trí của robot
            elif maze[r][c].visited:
                print("*", end=" ")  # Đánh dấu ô đã thăm
            elif any(maze[r][c].walls):
                print("#", end=" ")  # Tường
            else:
                print(".", end=" ")  # Đường đi
        print()

def print_path_coordinates(path):
    """In tọa độ từng ô trên đường đi"""
    print("\n📌 **Tọa độ của đường đi từ Start → Goal:**")
    for step, (r, c) in enumerate(path):
        print(f"🟢 Bước {step + 1}: ({r}, {c})")

# Đọc mê cung từ file
filename = "G:/CODE/BEST_PROJECT_2024/python-bfs-simulator/mazefiles-master/classic/13ye.txt"
maze, start, goal = read_maze_from_file(filename)

# Chạy BFS có animation
shortest_path = bfs_animation(maze, start, goal)

# In tọa độ đường đi chi tiết
if shortest_path:
    print_path_coordinates(shortest_path)
else:
    print("\n❌ Không tìm thấy đường đi!")
