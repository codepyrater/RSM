# Recipe Management System

## Overview
The Recipe Management System is a web-based application that allows users to manage their recipes. It provides features for users to create, edit, view, and delete recipes. The system also suggests recipes based on ingredients provided by the user.

## Technologies Used
### Frontend:
- Tkinter: Used for the graphical user interface (GUI) of the application.

### Backend:
- Python: The core programming language for the backend.
- MySQL: The database system used for storing user data and recipes.
- MySQL Connector: A Python library for connecting to MySQL databases.
- Hashlib: Used for hashing user passwords for security.

### Deployment:
- The application is designed to run locally on the user's machine.

## Database Schema
### Users Table
- **UserID (Primary Key)**: A unique identifier for each user.
- **Username**: The username of the user.
- **Email**: The email address of the user.
- **PasswordHash**: The hashed password of the user.

### Ingredients Table
- **IngredientID (Primary Key)**: A unique identifier for each ingredient.
- **Name**: The name of the ingredient.

### Recipes Table
- **RecipeID (Primary Key)**: A unique identifier for each recipe.
- **UserID (Foreign Key)**: A reference to the UserID in the Users table, indicating which user created the recipe.
- **Title**: The title of the recipe.
- **Ingredients**: A string storing a list of ingredients separated by commas.
- **Preparation**: The preparation steps for the recipe.

### RecipeIngredients Table
- **RecipeIngredientID (Primary Key)**: A unique identifier for each record.
- **RecipeID (Foreign Key)**: A reference to the RecipeID in the Recipes table, indicating which recipe the ingredient belongs to.
- **IngredientID (Foreign Key)**: A reference to the IngredientID in the Ingredients table, indicating which ingredient is used in the recipe.

### UserIngredients Table
- **UserIngredientID (Primary Key)**: A unique identifier for each record.
- **UserID (Foreign Key)**: A reference to the UserID in the Users table, indicating which user the ingredient belongs to.
- **IngredientID (Foreign Key)**: A reference to the IngredientID in the Ingredients table, indicating which ingredient is added by the user.

## Screens
### Login Screen
- Users can log in with their username and password.

### Registration Screen
- New users can register with a username, email, and password.

### Main Application Screen
- After logging in, users are presented with the main application screen.
- They can choose to add a new recipe, view/update their existing recipes, or get recipe suggestions based on ingredients.

### Add Recipe Screen
- Users can enter a title, ingredients, and preparation steps for a new recipe.

### View/Update Recipes Screen
- Users can view a list of their existing recipes.
- They can choose to update a recipe, which allows them to edit the title, ingredients, and preparation steps.
- Users can also choose to delete a recipe.

### Get Recipe Suggestions Screen
- Users can enter a list of ingredients, and the system suggests recipes that match those ingredients.

## Usage
1. Clone the project repository to your local machine.
2. Install the required Python libraries (`tkinter`, `mysql.connector`, `hashlib`).
3. Set up a MySQL database with the specified schema and update the database configuration in the code.
4. Run the Python script to start the application.

## Contributors
- Srikar Punna

## License
This project is licensed under the MIT License.
