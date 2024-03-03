import tkinter as tk
from tkinter import messagebox, font, PhotoImage
import re
import mysql.connector
from mysql.connector import Error
import hashlib
from PIL import Image, ImageTk

# Database configuration
db_config = {
    'user': 'root',
    'password': 'Srikar@123456',
    'host': '127.0.0.1',
    'database': 'RSM',
    'raise_on_warnings': True
}

# Function to create a database connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None
    
    
    