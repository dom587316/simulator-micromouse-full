import java.util.*;
import java.io.*;

int cols = 16, rows = 16;
int cellSize = 40;
Cell[][] grid;
ArrayList<Cell> stack = new ArrayList<Cell>();
Cell current;
boolean solving = false;
ArrayList<Cell> path = new ArrayList<Cell>();
Cell start, end;

void setup() {
  size(640, 640);
  frameRate(30);
  grid = new Cell[cols][rows];
  
  selectMazeFile();
}

void draw() {
  background(255);
  
  for (int i = 0; i < cols; i++) {
    for (int j = 0; j < rows; j++) {
      if (grid[i][j] != null) {
        grid[i][j].show();
      }
    }
  }
  
  if (!solving && start != null && end != null) {
    floodFill();
    solving = true;
  }
  
  if (start != null) {
    fill(0, 255, 0);
    rect(start.i * cellSize, start.j * cellSize, cellSize, cellSize);
  }
  
  if (end != null) {
    fill(255, 0, 0);
    rect(end.i * cellSize, end.j * cellSize, cellSize, cellSize);
  }
  
  for (Cell c : path) {
    fill(0, 0, 255);
    rect(c.i * cellSize + cellSize / 4, c.j * cellSize + cellSize / 4, cellSize / 2, cellSize / 2);
  }
}

void selectMazeFile() {
  selectInput("Select a maze file:", "fileSelected");
}

void fileSelected(File selection) {
  if (selection != null) {
    loadMaze(selection.getAbsolutePath());
  } else {
    println("No file selected.");
  }
}

void loadMaze(String filename) {
  try {
    BufferedReader br = new BufferedReader(new FileReader(filename));
    String line;
    int row = 0;
    while ((line = br.readLine()) != null && row < rows * 2 + 1) {
      if (row % 2 == 0) {
        // Dòng chứa các góc và tường ngang
        for (int col = 0; col < cols; col++) {
          grid[col][row / 2] = new Cell(col, row / 2);
          if (line.charAt(col * 4 + 2) == '-') {
            grid[col][row / 2].walls[0] = true; // Tường trên
          }
        }
      } else {
        // Dòng chứa các tường dọc và đường đi
        for (int col = 0; col < cols; col++) {
          if (grid[col][row / 2] == null) {
            grid[col][row / 2] = new Cell(col, row / 2);
          }
          char c = line.charAt(col * 4);
          if (c == '|') {
            grid[col][row / 2].walls[3] = true; // Tường trái
          }
          c = line.charAt(col * 4 + 2);
          if (c == 'S') start = grid[col][row / 2];
          if (c == 'G') end = grid[col][row / 2];
        }
      }
      row++;
    }
    br.close();
  } catch (Exception e) {
    println("Error loading maze: " + e.getMessage());
  }
}


void floodFill() {
  if (end == null) return;
  Queue<Cell> queue = new LinkedList<>();
  end.value = 0;
  queue.add(end);
  
  while (!queue.isEmpty()) {
    Cell current = queue.poll();
    for (Cell neighbor : current.getValidNeighbors()) {
      if (neighbor.value == -1) {
        neighbor.value = current.value + 1;
        queue.add(neighbor);
      }
    }
  }
}

class Cell {
  int i, j;
  boolean[] walls = {false, false, false, false}; // Top, Right, Bottom, Left
  int value = -1;
  
  Cell(int i, int j) {
    this.i = i;
    this.j = j;
  }
  
  void show() {
    int x = i * cellSize;
    int y = j * cellSize;
    stroke(0);
    if (walls[0]) line(x, y, x + cellSize, y);
    if (walls[1]) line(x + cellSize, y, x + cellSize, y + cellSize);
    if (walls[2]) line(x, y + cellSize, x + cellSize, y + cellSize);
    if (walls[3]) line(x, y, x, y + cellSize);
    
    if (value >= 0) {
      fill(255, 255, 0);
      textSize(12);
      text(value, x + cellSize / 3, y + cellSize / 2);
    }
  }
  
  ArrayList<Cell> getValidNeighbors() {
    ArrayList<Cell> neighbors = new ArrayList<>();
    if (i > 0 && !walls[3] && !grid[i-1][j].walls[1]) neighbors.add(grid[i-1][j]); // Left
    if (i < cols-1 && !walls[1] && !grid[i+1][j].walls[3]) neighbors.add(grid[i+1][j]); // Right
    if (j > 0 && !walls[0] && !grid[i][j-1].walls[2]) neighbors.add(grid[i][j-1]); // Top
    if (j < rows-1 && !walls[2] && !grid[i][j+1].walls[0]) neighbors.add(grid[i][j+1]); // Bottom
    return neighbors;
  }
}
