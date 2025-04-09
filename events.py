import api

# Example context object to hold current user ID and callbacks
context = {
    "user_id": 1,
    "refresh_ui": None  # this will be set by layout to trigger UI refresh
}

def load_user_info():
    user = api.get_user(context["user_id"])
    points = api.get_points(context["user_id"])
    return user, points

def load_user_info_for(uid):
    user = api.get_user(uid)
    points = api.get_points(uid)
    return user, points

def load_unopened_boxes():
    unopened = api.get_unopened_messages(context["user_id"])
    return unopened

def load_messages():
    return api.get_messages(context["user_id"])

def handle_send_message(receiver_id, message_text, point_value, message_type):
    if not message_text.strip():
        return False
    return api.send_message(
        sender_id=context["user_id"],
        receiver_id=receiver_id,
        message_type=message_type,
        message=message_text.strip()
    )

def handle_open_message(message_id):
    success = api.open_message(message_id)
    if success and context["refresh_ui"]:
        context["refresh_ui"]()  # trigger UI refresh
    return success
