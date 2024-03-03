import tkinter as tk
from tkinter import messagebox, font, PhotoImage
import re
import mysql.connector
from mysql.connector import Error
import hashlib
from PIL import Image, ImageTk
from db import create_db_connection
import globals 




# Style settings
bg_color = "lightblue"
button_color = "lightblue"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)



# Function to create the Add Recipe window
def add_recipe_window():
    add_window = tk.Toplevel()
    add_window.geometry("1000x800")
    add_window.title("Add New Recipe")
    add_window.configure(bg=bg_color)
    center_frame = tk.Frame(add_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    tk.Label(center_frame, text="Recipe Title",  font=label_font, bg=bg_color).pack()
    title_entry = tk.Entry(center_frame)
    title_entry.pack()

    tk.Label(center_frame, text="Ingredients", font=label_font, bg=bg_color).pack()
    ingredients_entry = tk.Entry(center_frame)
    ingredients_entry.pack()

    tk.Label(center_frame, text="Preparation Steps", font=label_font, bg=bg_color).pack()
    steps_entry = tk.Entry(center_frame)
    steps_entry.pack()

    tk.Button(center_frame, text="Submit", command=lambda: submit_recipe(title_entry.get(), ingredients_entry.get(), steps_entry.get())).pack(pady=10)

    
    
def parse_ingredients(ingredients_str):
    return [ingredient.strip() for ingredient in ingredients_str.split(',')]

    
# Function to submit a recipe to the database
def submit_recipe(title, ingredients_str, steps):
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO recipes (UserID,  title, ingredients, preparation) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (globals.set_logged_in_user_id, title, ingredients_str, steps))
            recipe_id = cursor.lastrowid

            # Handle ingredients
            ingredients_list = parse_ingredients(ingredients_str)

            # Filter out numeric values and keep only text
            filtered_ingredients = [re.sub(r'[^a-zA-Z\s]', '', ingredient).strip() for ingredient in ingredients_list]

            # Remove empty strings from the list
            filtered_ingredients = [ingredient for ingredient in filtered_ingredients if ingredient]

            for ingredient in filtered_ingredients:
                # Check if the ingredient exists in the 'Ingredients' table, if not, add it
                cursor.execute("SELECT IngredientID FROM ingredients WHERE Name = %s", (ingredient,))
                result = cursor.fetchone()
                if result:
                    ingredient_id = result[0]
                else:
                    cursor.execute("INSERT INTO ingredients (Name) VALUES (%s)", (ingredient,))
                    ingredient_id = cursor.lastrowid

                # Link the recipe to this ingredient in 'RecipeIngredients'
                cursor.execute("INSERT INTO recipeingredients (RecipeID, IngredientID) VALUES (%s, %s)", (recipe_id, ingredient_id))

            conn.commit()
            messagebox.showinfo("Success", "Recipe submitted successfully.")
        except Error as e:
            messagebox.showerror("Error", f"Error submitting recipe to MySQL database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")

