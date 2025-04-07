import tkinter as tk
from tkinter import ttk
import events


def create_ui():
    root = tk.Tk()
    root.title("dabomb")
    root.geometry("800x600")

    # Section 1: Header
    header = tk.Frame(root, pady=5)
    header.pack(fill=tk.X)

    title = tk.Label(header, text="dabomb", font=("Arial", 14, "bold"))
    title.pack(side=tk.LEFT, padx=10)

    user_info_var = tk.StringVar()
    user_info = tk.Label(header, textvariable=user_info_var, anchor="e")
    user_info.pack(side=tk.RIGHT, padx=10)

    # Section 2: Unopened boxes
    box_container = tk.Frame(root, height=100, pady=5)
    box_container.pack(fill=tk.X)

    box_frames = []
    for i in range(5):
        box = tk.Frame(box_container, width=80, height=80, relief=tk.RIDGE, borderwidth=2)
        box.pack(side=tk.LEFT, padx=5, pady=5)
        sender = tk.Label(box, text=f"User{i}", font=("Arial", 10))
        sender.pack()
        trust = tk.Label(box, text="TP: 5", font=("Arial", 14, "bold"))
        trust.pack()
        box_frames.append(box)

    # Section 3: Message area
    main_area = tk.Frame(root)
    main_area.pack(fill=tk.BOTH, expand=True)

    # User list
    user_list = tk.Listbox(main_area, width=20)
    user_list.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
    for name in ["Bob", "Charlie"]:
        user_list.insert(tk.END, name)

    # Messages and input area
    msg_area = tk.Frame(main_area)
    msg_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    messages = tk.Text(msg_area, state='disabled', height=20)
    messages.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Input row
    input_frame = tk.Frame(msg_area)
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    msg_entry = tk.Entry(input_frame)
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    point_entry = tk.Entry(input_frame, width=5)
    point_entry.pack(side=tk.LEFT, padx=5)

    # Buttons
    button_frame = tk.Frame(msg_area)
    button_frame.pack(pady=5)

    def get_selected_user():
        selected = user_list.curselection()
        return user_list.get(selected[0]) if selected else None

    def send(kind):
        receiver = get_selected_user()
        text = msg_entry.get()
        points = point_entry.get()
        if receiver and text:
            events.handle_send_message(receiver, text, points, kind)
            msg_entry.delete(0, tk.END)
            point_entry.delete(0, tk.END)
            refresh_ui()

    btn_plain = tk.Button(button_frame, text="Send Plain", command=lambda: send("plain"))
    btn_plain.pack(side=tk.LEFT, padx=5)

    btn_bomb = tk.Button(button_frame, text="Send Bomb", command=lambda: send("bomb"))
    btn_bomb.pack(side=tk.LEFT, padx=5)

    btn_gift = tk.Button(button_frame, text="Send Gift", command=lambda: send("gift"))
    btn_gift.pack(side=tk.LEFT, padx=5)

    def refresh_ui():
        user, points = events.load_user_info()
        if user and points:
            user_info_var.set(f"{user['name']} | Trust: {points['trust_points']} | Points: {points['game_points']}")

        # You could also update unopened boxes and message area here

    events.context["refresh_ui"] = refresh_ui
    refresh_ui()

    root.mainloop()
