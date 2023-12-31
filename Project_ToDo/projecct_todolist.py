import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")

        # Header labels
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(padx=10, pady=5)
        tk.Label(self.header_frame, text="No", width=10).pack(side="left")
        tk.Label(self.header_frame, text="Todo", width=30).pack(side="left")
        tk.Label(self.header_frame, text="Time", width=20).pack(side="left")
        tk.Label(self.header_frame, text="Actions", width=10).pack(side="left")

        # Main frame for todo items
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=5)

        self.todos = []

        self.entry = tk.Entry(root, width=60)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.add_todo)

        self.add_button = tk.Button(root, text="Add Todo", command=self.add_todo)
        self.add_button.pack(pady=5)

    def add_todo(self, event=None):
        todo = self.entry.get()
        if todo:
            current_time = datetime.now().strftime("%m/%d %H:%M")
            todo_frame = tk.Frame(self.main_frame)
            todo_frame.pack(anchor="w")
            
            tk.Label(todo_frame, text=str(len(self.todos) + 1), width=10).pack(side="left")
            tk.Label(todo_frame, text=todo, width=30).pack(side="left")
            tk.Label(todo_frame, text=current_time, width=20).pack(side="left")
            
            delete_button = tk.Button(todo_frame, text="Delete", command=lambda: self.delete_todo(todo_frame))
            delete_button.pack(side="left")

            self.todos.append((todo_frame, todo, current_time))
            self.entry.delete(0, "end")

    def delete_todo(self, todo_frame):
        todo_frame.destroy()
        self.todos.remove(todo_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
