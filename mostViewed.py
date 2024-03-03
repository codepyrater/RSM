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


#Function to display the most popular recipes

def display_most_popular_recipes():
    popular_window = tk.Toplevel()
    popular_window.title("Most Popular Recipes")
    popular_window.configure(bg=bg_color)
    popular_window.geometry("1000x800")

    center_frame = tk.Frame(popular_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            # Select recipes with the highest view counts
            cursor.execute("SELECT Title, ViewCount FROM recipes ORDER BY ViewCount DESC LIMIT 10")
            for recipe in cursor.fetchall():
                tk.Label(center_frame, text=f"{recipe['Title']} - Views: {recipe['ViewCount']}", bg=bg_color).pack()
        except Error as e:
            messagebox.showerror("Error", f"Error fetching most popular recipes: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")
    # ... In your main_app_window or wherever you want the button ...
 