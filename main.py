import tkinter as tk
from tkinter import messagebox, font, PhotoImage
import re
import mysql.connector
from mysql.connector import Error
import hashlib
from PIL import Image, ImageTk
from db import create_db_connection
import globals 
from registeration import show_registration_form
from dashboard import main_app_window






# Style settings
bg_color = "lightblue"
button_color = "lightblue"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)


# Function to verify user login
def verify_login(username, password):
    conn = create_db_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT UserID, PasswordHash FROM Users WHERE Username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            
            # Hash the input password to compare
            password_hash = hashlib.sha256(password.strip().encode()).hexdigest()
            print(f"Login Hash: {password_hash}")
            print(f"Stored Hash: {user['PasswordHash'] if user else 'No user found'}")

            if user and user['PasswordHash'] == password_hash:
                return user['UserID']
            else:
                return False
        except Error as e:
            messagebox.showerror("Database Query Error", str(e))
        finally:
            conn.close()
    return False



# Function to handle the user verification 
def login_button_clicked():
    username = username_entry.get()
    password = password_entry.get()
    user_id = verify_login(username, password)
    if user_id:
        globals.set_logged_in_user_id(user_id)
        messagebox.showinfo("Login Success", "You have successfully logged in.")
        main_app_window(root)  
    else:
        messagebox.showerror("Login Failed", "The username or password is incorrect.")
  
  
# Tkinter GUI for Login
root = tk.Tk()
root.geometry("1000x800")
root.title("Culinary Canvas")
root.configure(bg=bg_color)


 # Heading
heading_label = tk.Label( text="Culinary Canvas", font=heading_font, bg=bg_color)
heading_label.pack(pady=20)

desired_width = 300
desired_height = 250

# Load the image
image = Image.open("Main_pic.jpeg")
# Resize the image to desired dimensions
image = image.resize((desired_width, desired_height))
    
logo_image = ImageTk.PhotoImage(image)
logo_label = tk.Label(root, image=logo_image, bg=bg_color)  # Assume the background of your image is white
logo_label.pack(pady=20)
    

tk.Label(root, text="Username:", font=label_font, bg=bg_color).pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password:", font=label_font, bg=bg_color).pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login_button_clicked)
login_button.pack(pady=10)

register_label = tk.Label(root, text="New user?",bg=bg_color, font=label_font)
register_label.pack(pady=10)

register_button = tk.Button(root, text="Register", command=show_registration_form)
register_button.pack(pady=10)

root.mainloop()
