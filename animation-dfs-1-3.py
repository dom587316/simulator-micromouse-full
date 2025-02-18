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
        self.visible = False

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

    return maze, start, goal

def dfs_micromouse(maze, start, animation):
    rows, cols = len(maze), len(maze[0])
    stack = [start]  # Stack DFS
    path_stack = [start]  # Lưu lịch sử đường đi để backtrack từng bước
    visited_positions = []  # Lưu lại toàn bộ đường đã đi

    with open("handle.txt", "w") as log_file:
        animation.robot_position = start
        animation.update_display()
        log_file.write(f"Move to {start[0]}, {start[1]}\n")

        while stack:
            x, y = stack.pop()

            if maze[x][y].visited:
                continue

            # Đánh dấu ô đã thăm
            maze[x][y].visited = True
            maze[x][y].visible = True
            animation.robot_position = (x, y)
            animation.update_display()
            log_file.write(f"Move to {x}, {y}\n")
            visited_positions.append((x, y))  # Lưu lại đường đi để tìm đường ngắn nhất
            path_stack.append((x, y))  # Lưu vào path_stack để backtrack chính xác
            time.sleep(animation.speed)

            # Tìm các lối đi hợp lệ
            next_positions = []
            for new_direction in reversed(DIRECTION_ORDER):  
                dx, dy, wall_idx = DIRECTIONS[new_direction]
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols and not maze[x][y].walls[wall_idx] and not maze[nx][ny].visited:
                    next_positions.append((nx, ny))

            # Nếu có nhiều hơn một lối đi, lưu lại điểm hiện tại để quay về sau
            if len(next_positions) > 1:
                path_stack.append((x, y))  

            # Nếu có lối đi, đi tiếp
            if next_positions:
                stack.extend(next_positions)
            else:
                # Khi không còn lối đi, backtrack từng bước một
                while path_stack:
                    back_x, back_y = path_stack.pop()

                    # Kiểm tra nếu đã quay lại điểm xuất phát
                    if (back_x, back_y) == start:
                        log_file.write(f"Back to start ({back_x}, {back_y}) - Search complete!\n")
                        print("🏁 Quay lại điểm xuất phát. Kết thúc tìm kiếm!")

                        # 🟥 Tìm và hiển thị đường đi ngắn nhất
                        shortest_path = find_shortest_path(maze, start, goal)
                        animation.shortest_path = shortest_path
                        animation.update_display()

                        return  # Dừng chương trình ngay lập tức

                    # Hiển thị robot quay lại từng bước
                    animation.robot_position = (back_x, back_y)
                    animation.update_display()
                    log_file.write(f"Move to {back_x}, {back_y}\n")
                    time.sleep(animation.speed)

                    # Sau khi quay lại, kiểm tra xem còn hướng nào chưa đi không
                    remaining_paths = []
                    for new_direction in reversed(DIRECTION_ORDER):
                        dx, dy, wall_idx = DIRECTIONS[new_direction]
                        nx, ny = back_x + dx, back_y + dy

                        if 0 <= nx < rows and 0 <= ny < cols and not maze[back_x][back_y].walls[wall_idx] and not maze[nx][ny].visited:
                            remaining_paths.append((nx, ny))

                    # Nếu còn đường chưa đi, tiếp tục DFS
                    if remaining_paths:
                        stack.extend(remaining_paths)
                        break


def find_shortest_path(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        path = path + [(x, y)]

        if (x, y) in goal:
            # 🟥 Ghi đường đi ngắn nhất vào file
            with open("graph.txt", "a") as log_file:
                log_file.write("\nShortest Path:\n")
                for step in path:
                    log_file.write(f"Move to {step[0]}, {step[1]}\n")

            return path

        for new_direction in DIRECTION_ORDER:
            dx, dy, wall_idx = DIRECTIONS[new_direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not maze[x][y].walls[wall_idx]:
                queue.append(((nx, ny), path))

    return []


class MazeAnimation:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = 30
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.robot_position = None
        self.speed = 0.5
        self.shortest_path = []

        self.window = tk.Tk()
        self.window.title("Micromouse DFS - Dark Mode")
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
                
                color = "white" if self.maze[r][c].visible else "black"
                if (r, c) in self.shortest_path:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="gray")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
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

filename = "mazefiles-master/classic/50.txt"
maze, start, goal = read_maze_from_file(filename)

animation = MazeAnimation(maze)
dfs_micromouse(maze, start, animation)
animation.window.mainloop()