import tkinter as tk
from tkinter import messagebox, font, PhotoImage
import re
import mysql.connector
from mysql.connector import Error
import hashlib
from PIL import Image, ImageTk
from db import create_db_connection

# Style settings
bg_color = "lightblue"
button_color = "lightblue"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)

    
#funtion for registeration form
# Function to register a new user
def register_user(username, email, password, confirm_password):
    if password != confirm_password:
        messagebox.showwarning("Password Mismatch", "The passwords do not match.")
        return
    if not is_valid_email(email):
        messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        return
    
    
    
    
    
# Check password criteria
    # Regex explanation:
    # ^(?=.*\d) - At least one digit
    # (?=.*[A-Z]) - At least one uppercase letter
    # (?=.*[!@#$%^&*()]) - At least one special character
    # .{8,12}$ - Length between 8 to 12 characters
    if not re.match(r"^(?=.*\d)(?=.*[A-Z])(?=.*[!@#$%^&*()]).{8,12}$", password):
        messagebox.showwarning(
            "Password Requirement",
            "Password must be 8-12 characters long, include an uppercase letter, a number, and a special character."
        )
        return
  

    # Hash the password before storing it
    password_hash = hashlib.sha256(password.strip().encode()).hexdigest()
    print(f"Register Hash: {password_hash}")
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (Username, Email, PasswordHash) VALUES (%s, %s, %s)",
                (username, email, password_hash)
            )
            conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
        except Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()
            

def is_valid_email(email):
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9._%-]+@(gmail\.com|cmich\.edu|outlook\.com)$'
    if re.match(regex, email):
        return True
    else:
        return False

       
# Function to handle the register button click
def register_button_clicked():
    username = new_username_entry.get()
    email = email_entry.get()
    password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    register_user(username, email, password, confirm_password)
    
  

# Function for creating the registration form
def show_registration_form():
    global new_username_entry, email_entry, new_password_entry, confirm_password_entry, bg_color, label_font
    
    # Create the top-level window
    register_window = tk.Toplevel()
    register_window.geometry("1000x800")  # Adjust size as needed
    register_window.configure(bg=bg_color)
    
    # Set window size
    window_width = 1000
    window_height = 800
    register_window.geometry(f"{window_width}x{window_height}")


    
    
    
    register_window.title("Register New User")

    
    # Center frame
    center_frame = tk.Frame(register_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Heading
    heading_label = tk.Label(center_frame, text="User Registration", font=heading_font, bg=bg_color)
    heading_label.pack(pady=20)

    tk.Label(center_frame,text="Username:", font=label_font, bg=bg_color).pack()
    new_username_entry = tk.Entry(center_frame)
    new_username_entry.pack()

    tk.Label(center_frame,text="Email:", font=label_font, bg=bg_color).pack()
    email_entry = tk.Entry(center_frame)
    email_entry.pack()

    tk.Label(center_frame, text="Password:", font=label_font, bg=bg_color).pack()
    new_password_entry = tk.Entry(center_frame)
    new_password_entry.pack()

    tk.Label(center_frame, text="Confirm Password:", font=label_font, bg=bg_color).pack()
    confirm_password_entry = tk.Entry(center_frame, show="*")
    confirm_password_entry.pack()

    register_button = tk.Button(center_frame, text="Register", command=register_button_clicked)
    register_button.pack(pady=20)
   
