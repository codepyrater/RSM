import tkinter as tk
from tkinter import messagebox, font, PhotoImage
import re
import mysql.connector
from mysql.connector import Error
import hashlib
from PIL import Image, ImageTk
from addRecipe import add_recipe_window
from viewRecipe import view_update_recipes_window
from getSuggestions import ingredient_input_window
from mostViewed import display_most_popular_recipes 

# Style settings
bg_color = "lightblue"
button_color = "lightblue"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)



# Function for creating the main application window
def main_app_window(root):
    root.destroy()  # Close the login window
    main_window = tk.Tk()
    # Center frame
  
    
    
    main_window.geometry("1000x800")
    main_window.title("Culinary Canvas")
    main_window.configure(bg=bg_color)
    
    center_frame = tk.Frame(main_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
     # Heading label for the main application window
 

    # Buttons packed within the center frame
    tk.Button(center_frame, text="Add Recipe", command=add_recipe_window, bg='lightgrey').pack(fill='x', pady=10)
    tk.Button(center_frame, text="View/Update Recipe", command=view_update_recipes_window, bg='lightgrey').pack(fill='x', pady=10)
    tk.Button(center_frame, text="Get Suggestions", command=ingredient_input_window, bg='lightgrey').pack(fill='x', pady=10)
    tk.Button(center_frame, text="Most Popular Recipes", command=display_most_popular_recipes).pack(pady=20)

  
    

    main_window.mainloop()
  
