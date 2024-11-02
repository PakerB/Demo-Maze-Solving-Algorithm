import random, datetime, os
import tkinter as tk
import tkinter.messagebox as messagebox
import MazeSolvingAlgorithm as MSA
from tkinter import *

window = tk.Tk()
window.state('zoomed')
window.title("Demo Maze Solving Algorithm")
scr_width = window.winfo_screenwidth()
scr_height = window.winfo_screenheight()
window.geometry(f"{scr_width}x{scr_height}+0+0")

# Tạo một cửa sổ chia đôi
panedwindow = tk.PanedWindow(window, orient="horizontal")
panedwindow.pack(fill="both", expand=True)

# Khung bên trái: Canvas
canvas = tk.Canvas(panedwindow, width=scr_width-300, height=scr_height, background="white")
panedwindow.add(canvas)

# Khung bên phải: Các nút
frame = tk.Frame(panedwindow)
panedwindow.add(frame)

width = 1
height = 1
length = 1
grid = []
maze_map = {}
source = (0, 0)
destination = (0, 0)
speed = 300
width_var = StringVar(value="X (default X = 0):")
height_var = StringVar(value="Y (default Y = 0):")
a_star_path_len = StringVar(value="A Star Path Length : 0")
a_star_search_len = StringVar(value="A Star Search Length : 0")

def draw_maze():
    canvas.delete("all")
    for cell in grid:
        x,y = cell
        x1 = 10 + x*length
        x2 = x1 + length
        y1 = 10 + y*length
        y2 = y1 + length
        if maze_map[x,y]['T'] == 0:
            canvas.create_line(x1, y1, x2, y1, width=2, fill="black")  # Cạnh trên
        if maze_map[x,y]['R'] == 0:
            canvas.create_line(x2, y1, x2, y2, width=2, fill="black")  # Cạnh phải
        if maze_map[x,y]['B'] == 0:
            canvas.create_line(x2, y2, x1, y2, width=2, fill="black")  # Cạnh dưới
        if maze_map[x,y]['L'] == 0:
            canvas.create_line(x1, y2, x1, y1, width=2, fill="black")  # Cạnh trái


def breakWall(x1, y1, x2, y2):
    #Break wall between 2 cells
    #T - top edge of the cell
    #R - right edge of the cell
    #B - bottom edge of the cell
    #L - left edge of the cell
    global maze_map
    if x1 == x2:
        if y1 + 1 == y2:
            maze_map[x1,y1]['B'] = 1
            maze_map[x2,y2]['T'] = 1
        else:
            maze_map[x1,y1]['T'] = 1
            maze_map[x2,y2]['B'] = 1
    else:
        if x1 + 1 == x2:
            maze_map[x1,y1]['R'] = 1
            maze_map[x2,y2]['L'] = 1
        else:
            maze_map[x1,y1]['L'] = 1
            maze_map[x2,y2]['R'] = 1


def create_maze():
    
    global maze_map
    global grid
    grid = []
    maze_map = {}
    for x in range(width):
        for y in range(height):
            grid.append((x,y))
            maze_map[x,y]={'T':0,'B':0,'L':0,'R':0}
    x = 0
    y = 0
    _stack = []
    _stack.append((x,y))
    _closed = []
    _closed.append((x,y))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
    wall = []
    while len(_stack) > 0:
        cell = []
        for dx, dy in directions:
            u = x + dx
            v = y + dy
            if (u, v) not in _closed and (u, v) in grid:
                cell.append((u, v))
                wall.append((x, y, u, v))
        if len(cell) > 0:
            u, v = random.choice(cell)
            breakWall(x, y, u, v)
            _closed.append((u, v))
            _stack.append((u, v))
            wall.remove((x, y, u, v))
            x = u
            y = v
        else:
            x, y = _stack.pop()
    
    #Break random wall
    # for i in range(max(1, int(width * height / 20 ))):
    #     x, y, u, v = random.choice(wall)
    #     breakWall(x, y, u, v)
    #     wall.remove((x, y, u, v))
    
    draw_maze()

def print_cell(x, y, color):
    if(x,y) == source or (x,y) == destination:
        color = "red"
    x1 = 10 + x*length
    x2 = x1 + length   
    y1 = 10 + y*length
    y2 = y1 + length 
    inner_offset = 0 
    canvas.create_rectangle(x1 + inner_offset, y1 + inner_offset,
                        x2 - inner_offset, y2 - inner_offset,
                        fill=color, outline='')
    if maze_map[x,y]['T'] == 0:
        canvas.create_line(x1, y1, x2, y1, width=2, fill="black")  # Cạnh trên
    if maze_map[x,y]['R'] == 0:
        canvas.create_line(x2, y1, x2, y2, width=2, fill="black")  # Cạnh phải
    if maze_map[x,y]['B'] == 0:
        canvas.create_line(x2, y2, x1, y2, width=2, fill="black")  # Cạnh dưới
    if maze_map[x,y]['L'] == 0:
        canvas.create_line(x1, y2, x1, y1, width=2, fill="black")  # Cạnh trái

def tracePath(Path, index, color, onComplete=None):
    if len(Path) == 0:
        if onComplete:
            onComplete()  
        return

    x, y = Path[index]
    print_cell(x, y, color)
    Path.pop(index)
    if len(Path) != 0:
        window.after(speed, tracePath, Path, index, color, onComplete)
    else:
        if onComplete:
            window.after(200, onComplete)  

def Sol():
    print_cell(source[0], source[1], "tomato")
    print_cell(destination[0], destination[1], "tomato")

    searchPath, fwdPath = MSA.aStar(maze_map, width, height, source, destination)

    tracePath(searchPath, 0, "DeepSkyBlue2", lambda: tracePath(fwdPath, -1, "yellow2"))
    a_star_path_len.set(f"A Star Path Length : {len(fwdPath)+1}")
    a_star_search_len.set(f"A Star Search Length : {len(searchPath)}")
    

def checkSizeOfMaze():
    try:
        global height
        global width
        height = int(height_entry.get())
        width = int(width_entry.get())
        
        if 0 < width <= 120 and 0 < height <= 80:
            global width_var
            global height_var
            width_var.set(f"X (default X = {(width-1)}):")
            height_var.set(f"Y (default Y = {(height-1)}):")
            global destination
            destination = (width - 1, height - 1)
            global speed
            if (width * height) <= 100:
                speed = 200
            elif (width * height) <= 500:
                speed = 100
            elif (width * height) <= 5000:
                speed = 50
            else:
                speed = 20
            
            global length 
            length = int(min((scr_width-310) / (width+5), (scr_height-50) / (height+5)))
            create_maze()
        else:
            messagebox.showerror("Error", "Please enter valid values within the specified limits.")
    except ValueError:
        messagebox.showerror("Error", "Please enter integer values for length and width.")

def validate_coordinates(x_entry, y_entry, width, height, typ):
    try:
        x_value = x_entry.get()
        y_value = y_entry.get()
        if x_value and y_value:
            x = int(x_value)
            y = int(y_value)
            if 0 <= x < width and 0 <= y < height:
                if typ == 0:
                    global source
                    source = (x,y)
                else:
                    global destination
                    destination = (x,y)
                return True
            else:
                messagebox.showerror(
                    "Invalid Coordinate",
                    f"Error: Coordinate ({x}, {y}) is out of bounds. It must be within (0, 0) to ({width-1}, {height-1})."
                )
                return False
        else:
            return True
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Error: Coordinate values must be integers."
        )
        return False
    
if __name__=='__main__':
    Label(frame, text='Enter the width of the maze (Max 120):').grid(row=0)
    Label(frame, text='Enter the height of the maze (Max 80):').grid(row=1)
    width_entry = Entry(frame)
    height_entry = Entry(frame)
    width_entry.grid(row=0, column=1)
    height_entry.grid(row=1, column=1)
    button_create = tk.Button(frame, text="Create", command=lambda: checkSizeOfMaze()).grid(row=3)
    Label(frame, text='Enter the source coordinate:').grid(row=4)
    Label(frame, text="X (default X = 0):").grid(row=5)
    Label(frame, text="Y (default Y = 0):").grid(row=6)
    source_x = Entry(frame)
    source_y = Entry(frame)
    source_x.grid(row=5, column=1)
    source_y.grid(row=6, column=1)
    Label(frame, text='Enter the destination coordinate:').grid(row=7)
    Label(frame, textvariable = width_var).grid(row=8)
    Label(frame, textvariable = height_var).grid(row=9)
    destination_x = Entry(frame)
    destination_y = Entry(frame)
    destination_x.grid(row=8, column=1)
    destination_y.grid(row=9, column=1)
    button_create = tk.Button(frame, text="A Star Algorithm", command=lambda: (
        validate_coordinates(source_x, source_y, width, height, 0) and 
        validate_coordinates(destination_x, destination_y, width, height, 1) and 
        Sol()
    )).grid(row=12)
    Label(frame,textvariable = a_star_path_len).grid(row=13)
    Label(frame,textvariable = a_star_search_len).grid(row=14)
    window.mainloop()