import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from collections import deque

class VirtualPainter:
    def __init__(self, master):
        self.master = master
        self.master.title("Virtual Painter")
        self.master.geometry("800x600")

        self.canvas = tk.Canvas(self.master, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.last_x = None
        self.last_y = None
        self.color = "black"
        self.brush_size = 2
        self.brush_shape = "circle"
        self.mode = "brush"

        self.shapes = []  # List to store shapes
        self.undo_stack = deque()  # Stack to store undo actions
        self.redo_stack = deque()  # Stack to store redo actions

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Save", command=self.save_drawing)
        file_menu.add_command(label="Load", command=self.load_drawing)
        file_menu.add_command(label="Clear Canvas", command=self.clear_canvas)
        menubar.add_cascade(label="File", menu=file_menu)

        brush_menu = tk.Menu(menubar, tearoff=False)
        brush_menu.add_command(label="Change Color", command=self.change_color)
        brush_menu.add_command(label="Change Size", command=self.change_size)
        brush_menu.add_command(label="Change Shape", command=self.change_shape)
        brush_menu.add_command(label="Switch to Eraser", command=self.switch_to_eraser)
        brush_menu.add_command(label="Switch to Brush", command=self.switch_to_brush)
        menubar.add_cascade(label="Brush", menu=brush_menu)

        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

    def paint(self, event):
        x, y = event.x, event.y
        shape = None
        if self.last_x and self.last_y:
            if self.mode == "brush":
                if self.brush_shape == "circle":
                    shape = self.canvas.create_oval(self.last_x, self.last_y, x, y, width=self.brush_size, outline=self.color, fill=self.color)
                elif self.brush_shape == "rectangle":
                    shape = self.canvas.create_rectangle(self.last_x, self.last_y, x, y, width=self.brush_size, outline=self.color, fill=self.color)
                elif self.brush_shape == "square":
                    side_length = abs(x - self.last_x)
                    shape = self.canvas.create_rectangle(self.last_x, self.last_y, self.last_x + side_length, self.last_y + side_length, width=self.brush_size, outline=self.color, fill=self.color)
            elif self.mode == "eraser":
                eraser_size = self.brush_size * 2
                shape = self.canvas.create_rectangle(x - eraser_size, y - eraser_size, x + eraser_size, y + eraser_size, fill="white", outline="white")
        self.last_x = x
        self.last_y = y

        if shape:
            self.shapes.append(shape)
            self.undo_stack.append(shape)
            self.redo_stack.clear()  # Clear redo stack on new action

    def reset(self, event):
        self.last_x = None
        self.last_y = None

    def change_color(self):
        color = colorchooser.askcolor(title="Choose Color")
        if color[1]:
            self.color = color[1]

    def change_size(self):
        size = simpledialog.askinteger("Brush Size", "Enter brush size:", initialvalue=self.brush_size)
        if size:
            self.brush_size = size

    def change_shape(self):
        shape = simpledialog.askstring("Brush Shape", "Enter brush shape (circle, rectangle, square):", initialvalue=self.brush_shape)
        if shape in ["circle", "rectangle", "square"]:
            self.brush_shape = shape

    def switch_to_eraser(self):
        self.mode = "eraser"

    def switch_to_brush(self):
        self.mode = "brush"

    def undo(self):
        if self.undo_stack:
            shape = self.undo_stack.pop()
            self.canvas.delete(shape)
            self.redo_stack.append(shape)
            self.shapes.remove(shape)

    def redo(self):
        if self.redo_stack:
            shape = self.redo_stack.pop()
            self.canvas.itemconfig(shape, state='normal')
            self.undo_stack.append(shape)
            self.shapes.append(shape)

    def save_drawing(self):
        filename = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps")])
        if filename:
            self.canvas.postscript(file=filename, colormode='color')

    def load_drawing(self):
        filename = filedialog.askopenfilename(filetypes=[("PostScript files", "*.ps")])
        if filename:
            self.canvas.delete("all")
            self.shapes.clear()
            self.undo_stack.clear()
            self.redo_stack.clear()
            self.canvas.update()
            # Load PostScript file as image
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk.PhotoImage(file=filename))

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

def main():
    root = tk.Tk()
    app = VirtualPainter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
