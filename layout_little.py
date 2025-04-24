import tkinter as tk

root = tk.Tk()
tk.Label(root, text="Hi").pack()
tk.Button(root, text="Close", command=root.destroy).pack()
root.mainloop()
