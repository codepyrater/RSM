logged_in_user_id = None

def get_logged_in_user_id():
    global logged_in_user_id
    return logged_in_user_id

def set_logged_in_user_id(user_id):
    global logged_in_user_id
    logged_in_user_id = user_id
