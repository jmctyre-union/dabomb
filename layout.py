import tkinter as tk
from tkinter import ttk
import events
import json

def create_ui():
    root = tk.Tk()
    root.title("dabomb")
    root.geometry("800x600")

    context = {
        "receiver_id": None
    }

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
    user_id_map = {"Everyone": None}
    user_list.insert(tk.END, "Everyone")
    for idx, user in enumerate(users):
        user_list.insert(tk.END, user['name'])
        user_id_map[user['name']] = user['id']

    # Messages and input area
    msg_area = tk.Frame(main_area)
    msg_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    messages = tk.Text(msg_area, state='disabled', height=20, wrap=tk.WORD)
    messages.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Input row
    input_frame = tk.Frame(msg_area)
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    receiver_name_var = tk.StringVar()
    receiver_name_label = tk.Label(input_frame, textvariable=receiver_name_var, font=("Arial", 12, "bold"))
    receiver_name_label.pack(side=tk.LEFT, padx=5)

    msg_entry = tk.Entry(input_frame)
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    point_entry = tk.Entry(input_frame, width=5)
    point_entry.pack(side=tk.LEFT, padx=5)

    # Buttons
    button_frame = tk.Frame(msg_area)
    button_frame.pack(pady=5)

    def send(kind):
        text = msg_entry.get()
        points = point_entry.get()
        if text:
            events.handle_send_message(context["receiver_id"], text, points, kind)
            msg_entry.delete(0, tk.END)
            point_entry.delete(0, tk.END)
            refresh_ui()

    btn_plain = tk.Button(button_frame, text="Send Plain", command=lambda: send("plain"))
    btn_plain.pack(side=tk.LEFT, padx=5)

    btn_bomb = tk.Button(button_frame, text="Send Bomb", command=lambda: send("bomb"))
    btn_bomb.pack(side=tk.LEFT, padx=5)

    btn_gift = tk.Button(button_frame, text="Send Gift", command=lambda: send("gift"))
    btn_gift.pack(side=tk.LEFT, padx=5)

    def update_receiver_ui():
        receiver_id = context["receiver_id"]
        if receiver_id is None:
            receiver_name_var.set("Send To: Everyone")
            btn_bomb.config(state=tk.DISABLED)
            btn_gift.config(state=tk.DISABLED)
        else:
            receiver_info_tuple = events.load_user_info_for(receiver_id)
            if receiver_info_tuple:
                receiver_info = receiver_info_tuple[0]
                receiver_name_var.set(f"Send To: {receiver_info['name']}")
            btn_bomb.config(state=tk.NORMAL)
            btn_gift.config(state=tk.NORMAL)

    def on_user_select(event):
        selection = user_list.curselection()
        if selection:
            name = user_list.get(selection[0])
            context["receiver_id"] = user_id_map.get(name)
            update_receiver_ui()

    user_list.bind('<<ListboxSelect>>', on_user_select)

    def refresh_ui():
        user, points = events.load_user_info()

        update_receiver_ui()

        if user and points:
            user_info_var.set(f"{user['name']} | Trust: {points['trust_points']} | Points: {points['game_points']}")

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

        # Update message area
        all_messages = events.load_messages()
        messages.config(state='normal')
        messages.delete(1.0, tk.END)

        for msg in sorted(all_messages, key=lambda m: m['sent_at']):
            sender_user, _ = events.load_user_info_for(msg['sender_id'])
            sender_name = sender_user['name'] if sender_user else f"User {msg['sender_id']}"
            receiver_mention = f"@{events.load_user_info_for(msg['receiver_id'])[0]['name']}" if msg['receiver_id'] else ""

            label = ""
            if msg['message_type'] == 'gift':
                label = "GIFT"
                label_color = "green"
                label_points = "+3"
            elif msg['message_type'] == 'bomb':
                label = "BOMB"
                label_color = "red"
                label_points = "-5"
            else:
                label = ""
                label_color = None
                label_points = ""

            formatted = f"{sender_name} : {receiver_mention}"
            if label:
                formatted += f" : {label}|{label_points}"
            formatted += f" : {msg['message']}\n"

            messages.insert(tk.END, formatted)
        messages.config(state='disabled')
        messages.see(tk.END)

    events.context["refresh_ui"] = refresh_ui
    refresh_ui()

    root.mainloop()
