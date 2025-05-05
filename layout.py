import tkinter as tk
from tkinter import ttk
import events
import json


def create_ui():
    root = tk.Tk()
    root.title("dabomb")
    root.geometry("800x600")

    receiver = {'id': None}  # Track receiver ID

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

    # Section 3: Message area
    main_area = tk.Frame(root)
    main_area.pack(fill=tk.BOTH, expand=True)

    # User list
    user_list = tk.Listbox(main_area, width=20)
    user_list.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    users = events.load_users()
    user_list.insert(tk.END, "Everyone")
    user_id_map = {"Everyone": None}
    for user in users:
        display_name = f"{user['name']}: {user['game_points']}"
        user_list.insert(tk.END, display_name)
        user_id_map[display_name] = user['id']

    # Messages and input area
    msg_area = tk.Frame(main_area)
    msg_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    messages = tk.Text(msg_area, state='disabled', height=20)
    messages.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Input row
    input_frame = tk.Frame(msg_area)
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    receiver_name_var = tk.StringVar(value="Send To: Everyone")
    receiver_name = tk.Label(input_frame, textvariable=receiver_name_var, font=("Arial", 12, "bold"))
    receiver_name.pack(side=tk.LEFT, padx=5)

    msg_entry = tk.Entry(input_frame)
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    point_entry = tk.Entry(input_frame, width=5)
    point_entry.pack(side=tk.LEFT, padx=5)

    # Buttons
    button_frame = tk.Frame(msg_area)
    button_frame.pack(pady=5)

    btn_plain = tk.Button(button_frame, text="Send Plain", command=lambda: send_plain())
    btn_plain.pack(side=tk.LEFT, padx=5)

    btn_bomb = tk.Button(button_frame, text="Send Bomb", command=lambda: send_bomb(), state=tk.DISABLED)
    btn_bomb.pack(side=tk.LEFT, padx=5)

    btn_gift = tk.Button(button_frame, text="Send Gift", command=lambda: send_gift(), state=tk.DISABLED)
    btn_gift.pack(side=tk.LEFT, padx=5)

    def refresh_user_info():
        user, points = events.load_user_info()
        if user and points:
            user_info_var.set(f"{user['name']} | Trust: {points['trust_points']} | Points: {points['game_points']}")

    def refresh_unopened_boxes():
        for widget in box_container.winfo_children():
            widget.destroy()

        unopened = events.load_unopened_boxes()
        for msg in unopened:
            sender_id = msg["sender_id"]
            sender_user, sender_points = events.load_user_info_for(sender_id)
            sender_name = sender_user['name'] if sender_user else f"User {sender_id}"
            sender_trust = sender_points['trust_points'] if sender_points else "?"

            box = tk.Frame(box_container, width=80, height=80, relief=tk.RIDGE, borderwidth=2)
            box.pack(side=tk.LEFT, padx=5, pady=5)
            sender = tk.Label(box, text=f"{sender_name}", font=("Arial", 10))
            sender.pack()
            trust = tk.Label(box, text=f"TP: {sender_trust}", font=("Arial", 14, "bold"))
            trust.pack()

    def refresh_messages():
        messages.config(state='normal')
        messages.delete(1.0, tk.END)

        opened_msgs = events.load_all_opened_messages()
        for msg in opened_msgs:
            sender_id = msg['sender_id']
            receiver_id = msg.get('receiver_id')
            sender_user, _ = events.load_user_info_for(sender_id)
            sender_name = sender_user['name'] if sender_user else f"User {sender_id}"
            receiver_tag = f"@{events.load_user_info_for(receiver_id)[0]['name']}" if receiver_id else "All"
            kind = msg['message_type']
            points = events.calculate_points_display(kind)
            label = ""
            if kind == "gift":
                label = "GIFT"
            elif kind == "bomb":
                label = "BOMB"

            text = msg['message']
            display = f"{sender_name} : {receiver_tag} : {label}|{points} : {text}\n"
            messages.insert(tk.END, display)

        messages.config(state='disabled')
        messages.see(tk.END)

    def get_selected_user():
        selected = user_list.curselection()
        if selected:
            name = user_list.get(selected[0])
            return user_id_map.get(name)
        return None

    def send_plain():
        current_receiver = receiver['id']
        text = msg_entry.get()
        points = point_entry.get()

        if text:
            events.handle_send_message(current_receiver, text, points)
            msg_entry.delete(0, tk.END)
            point_entry.delete(0, tk.END)
            refresh_messages()

    def send_gift():
        current_receiver = receiver['id']
        text = msg_entry.get()
        points = point_entry.get()
        if current_receiver is None:
            return
        if text:
            events.handle_send_gift(current_receiver, text, points)
            msg_entry.delete(0, tk.END)
            point_entry.delete(0, tk.END)
            refresh_messages()
            refresh_unopened_boxes()  # Update boxes after sending gift

    def send_bomb():
        current_receiver = receiver['id']
        text = msg_entry.get()
        points = point_entry.get()
        if current_receiver is None:
            return
        if text:
            events.handle_send_bomb(current_receiver, text, points)
            msg_entry.delete(0, tk.END)
            point_entry.delete(0, tk.END)
            refresh_messages()
            refresh_unopened_boxes()  # Update boxes after sending bomb

    def on_user_select(event):
        sel = user_list.curselection()
        if sel:
            name = user_list.get(sel[0])
            uid = user_id_map.get(name)
            receiver['id'] = uid
            receiver_name_var.set(f"Send To: {name}")
            if uid is None:
                btn_bomb.config(state=tk.DISABLED)
                btn_gift.config(state=tk.DISABLED)
            else:
                btn_bomb.config(state=tk.NORMAL)
                btn_gift.config(state=tk.NORMAL)

    user_list.bind("<<ListboxSelect>>", on_user_select)

    def refresh_ui():
        refresh_user_info()
        refresh_unopened_boxes()
        refresh_messages()

    events.context["refresh_ui"] = refresh_ui
    refresh_ui()

    root.mainloop()
