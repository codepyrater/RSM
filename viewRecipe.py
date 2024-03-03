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
import globals 


# Style settings
bg_color = "lightblue"
button_color = "lightblue"
heading_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 12)


def parse_ingredients(ingredients_str):
    return [ingredient.strip() for ingredient in ingredients_str.split(',')]



#Function to view and update the recipes

def view_update_recipes_window():
    view_window = tk.Toplevel()
    view_window.title("View/Update Recipes")
    view_window.configure(bg=bg_color)
    view_window.geometry("1000x800")
    
    
    center_frame = tk.Frame(view_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    # Fetching recipes from the database
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            current_user_id = globals.get_logged_in_user_id()
            cursor.execute("SELECT RecipeID, Title FROM recipes WHERE UserID = %s", (current_user_id,))
            for recipe in cursor.fetchall():
                recipe_id = recipe[0]
                title = recipe[1]
                tk.Label(center_frame, text="Recipe Name: "+title, font=label_font, bg=bg_color).pack()
                tk.Button(center_frame, text="Edit",font=label_font, bg="lightgrey", command=lambda id=recipe_id: edit_recipe(id)).pack()
                tk.Button(center_frame, text="Delete",font=label_font, bg="lightgrey", command=lambda id=recipe_id: delete_recipe(id)).pack()
                
        except Error as e:
            messagebox.showerror("Error", f"Error fetching recipes from MySQL database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")
        
#Function to save the updated recipe
def save_updated_recipe(recipe_id, title, ingredients, preparation):
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Step 1: Update recipe details in the 'recipes' table
            cursor.execute("UPDATE recipes SET Title = %s, Ingredients = %s, Preparation = %s WHERE RecipeID = %s",
                           (title, ingredients, preparation, recipe_id))
            
            # Step 2: Delete existing records in 'RecipeIngredients' for the updated recipe
            cursor.execute("DELETE FROM recipeingredients WHERE RecipeID = %s", (recipe_id,))
            
            # Step 3: Split and parse the new ingredients
            new_ingredients = parse_ingredients(ingredients)
            
            for ingredient in new_ingredients:
                # Step 4: Check if the ingredient exists in the 'Ingredients' table, if not, add it
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
            messagebox.showinfo("Success", "Recipe updated successfully.")
        except Error as e:
            messagebox.showerror("Error", f"Error updating recipe: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")


#Function to edit the recipe
def edit_recipe(recipe_id):
    # Open a window to edit the recipe
    edit_window = tk.Toplevel()
    edit_window.title("Edit Recipe")
    edit_window.configure(bg=bg_color)
    edit_window.geometry("1000x800")
    
    
    center_frame = tk.Frame(edit_window, bg=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    

    # Fetch and display the existing recipe details
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Title, Ingredients, Preparation FROM recipes WHERE RecipeID = %s", (recipe_id,))
            recipe = cursor.fetchone()
            if recipe:
                title = recipe[0]
                ingredients = recipe[1]
                preparation = recipe[2]

                tk.Label(center_frame, text="Title:", font=label_font, bg=bg_color).pack()
                title_entry = tk.Entry(center_frame)
                title_entry.insert(0, title)
                title_entry.pack()

                tk.Label(center_frame, text="Ingredients:", font=label_font, bg=bg_color).pack()
                ingredients_entry = tk.Entry(center_frame)
                ingredients_entry.insert(0, ingredients)
                ingredients_entry.pack()

                tk.Label(center_frame, text="Preparation:", font=label_font, bg=bg_color).pack()
                preparation_entry = tk.Entry(center_frame)
                preparation_entry.insert(0, preparation)
                preparation_entry.pack()

                # Update button to save changes
                tk.Button(center_frame, text="Update", command=lambda: save_updated_recipe(recipe_id, title_entry.get(), ingredients_entry.get(), preparation_entry.get())).pack()

            else:
                messagebox.showerror("Error", "Recipe not found.")
        except Error as e:
            messagebox.showerror("Error", f"Error fetching recipe details from MySQL database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")


#Function to delete the recipe
def delete_recipe(recipe_id):
    # Delete the recipe with the given recipe_id
    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # First, delete any related entries in the 'recipeingredients' table
            cursor.execute("DELETE FROM recipeingredients WHERE RecipeID = %s", (recipe_id,))
            # Now, it's safe to delete the recipe from the 'recipes' table
            cursor.execute("DELETE FROM recipes WHERE RecipeID = %s", (recipe_id,))
            conn.commit()
            messagebox.showinfo("Success", "Recipe deleted successfully.")
        except Error as e:
            # Rollback in case there is any error
            conn.rollback()
            messagebox.showerror("Error", f"Error deleting recipe: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "Cannot connect to the database.")

