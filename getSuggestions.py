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



#Function to input the ingredients
def ingredient_input_window():
    ingredient_window = tk.Toplevel()
    ingredient_window.title("Input Ingredients")
    ingredient_window.configure(bg=bg_color)
    ingredient_window.geometry("1000x800")
    
    
    center_frame = tk.Frame(ingredient_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(center_frame, text="Enter Ingredients (comma-separated):", bg= "lightblue").pack(fill='x', pady=10)
    ingredients_entry = tk.Entry(center_frame)
    ingredients_entry.pack()

    tk.Button(center_frame, text="Submit Ingredients", command=lambda: submit_user_ingredients(ingredients_entry.get(), ingredient_window)).pack(fill='x', pady=10)
    
    
#Function to increment the recipe view count    
def increment_recipe_view_count(recipe_id):
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Increment the view count for the recipe
            cursor.execute("UPDATE recipes SET ViewCount = ViewCount + 1 WHERE RecipeID = %s", (recipe_id,))
            conn.commit()
        except Error as e:
            conn.rollback()  # Rollback in case of error
            print(f"Error incrementing view count: {e}")
        finally:
            cursor.close()
            conn.close()

#Function to display the full recipe

def display_full_recipe(recipe_id):
    
    detail_window = tk.Toplevel()
    detail_window.title("Recipe Details")
    detail_window.configure(bg=bg_color)
    detail_window.geometry("1000x800")
    increment_recipe_view_count(recipe_id)
    detail_center_frame = tk.Frame(detail_window, bg=bg_color)
    detail_center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT Title, Ingredients, Preparation FROM recipes WHERE RecipeID = %s", (recipe_id,))
            recipe = cursor.fetchone()
            cursor.close()

            if recipe:
                tk.Label(detail_center_frame, text=f"Title: {recipe['Title']}", font=label_font, bg=bg_color).pack()
                tk.Label(detail_center_frame, text=f"Ingredients: {recipe['Ingredients']}", font=label_font, bg=bg_color).pack()
                tk.Label(detail_center_frame, text=f"Preparation: {recipe['Preparation']}", font=label_font, bg=bg_color).pack()
            else:
                messagebox.showinfo("Not found", "Recipe details not found.")
        except Error as e:
            messagebox.showerror("Error", f"Error fetching recipe details: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")

#Function to submit the user ingredients

def submit_user_ingredients(ingredients, window):
    ingredient_list = [ingredient.strip() for ingredient in ingredients.split(',')]
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            for ingredient in ingredient_list:
                # Assuming you have a function to get IngredientID from ingredient name
                ingredient_id = get_ingredient_id(ingredient, cursor)
                if ingredient_id:
                    cursor.execute("INSERT INTO UserIngredients (UserID, IngredientID) VALUES (%s, %s)", ( globals.set_logged_in_user_id, ingredient_id))
            conn.commit()
            messagebox.showinfo("Success", "Ingredients submitted successfully.")
            window.destroy()
            get_recipe_suggestions(ingredient_list)
        except Error as e:
            messagebox.showerror("Error", f"Error submitting ingredients: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")

def get_ingredient_id(ingredient_name, cursor):
    cursor.execute("SELECT IngredientID FROM Ingredients WHERE Name = %s", (ingredient_name,))
    result = cursor.fetchone()
    return result[0] if result else None


   
#Function to get the recipe suggestions
def get_recipe_suggestions(ingredient_list):
    suggestion_window = tk.Toplevel()
    suggestion_window.title("Recipe Suggestions")
    suggestion_window.configure(bg=bg_color)
    suggestion_window.geometry("1000x800")

    center_frame = tk.Frame(suggestion_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            format_strings = ','.join(['%s'] * len(ingredient_list))
            query = f"""
            SELECT DISTINCT r.RecipeID, r.Title
            FROM Recipes r
            JOIN RecipeIngredients ri ON r.RecipeID = ri.RecipeID
            JOIN Ingredients i ON ri.IngredientID = i.IngredientID
            WHERE ri.IngredientID IN (SELECT IngredientID FROM Ingredients WHERE Name IN ({format_strings}))
            GROUP BY r.RecipeID, r.Title
            """
            cursor.execute(query, tuple(ingredient_list))

            for recipe in cursor.fetchall():
                recipe_id = recipe['RecipeID']
                # recipe_title = recipe['Title']
                recipe_button = tk.Button(center_frame, text=f"Title: {recipe['Title']}", command=lambda r_id=recipe_id: display_full_recipe(r_id))
                recipe_button.pack(fill='x', pady=10)
        except Error as e:
            messagebox.showerror("Error", f"Error fetching recipe suggestions: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")
