import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np

# Load the trained Random Forest model
model = joblib.load('random_forest_model.pkl')

# Function to predict calories
def predict_calories():
    try:
        # Get input values from the user
        gender = gender_var.get().strip().lower()
        age = age_entry.get().strip()
        height = height_entry.get().strip()
        weight = weight_entry.get().strip()
        duration = duration_entry.get().strip()

        # Validate that all required fields are filled
        if not all([gender, age, height, weight, duration]):
            raise ValueError("All fields except Body Temperature and Heart Rate must be filled.")

        # Validate gender input
        if gender not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'.")

        # Validate numeric inputs
        numeric_inputs = [age, height, weight, duration]
        for input_value in numeric_inputs:
            try:
                float(input_value)
            except ValueError:
                raise ValueError(f"'{input_value}' is not a valid number.")

        # Convert inputs to the correct type
        age = float(age)
        height = float(height)
        weight = float(weight)
        duration = float(duration)

        # Get body temperature and heart rate based on selection
        body_temp_option = body_temp_var.get()
        heart_rate_option = heart_rate_var.get()

        if body_temp_option == "Enter Manually":
            body_temp = float(body_temp_entry.get().strip())
        else:
            body_temp_mapping = {
                "Low": 37.5,
                "Medium": 40.025453,
                "High": 41.5
            }
            body_temp = body_temp_mapping[body_temp_option]

        if heart_rate_option == "Enter Manually":
            heart_rate = float(heart_rate_entry.get().strip())
        else:
            heart_rate_mapping = {
                "Low": 77,
                "Medium": 95.518533,
                "High": 115
            }
            heart_rate = heart_rate_mapping[heart_rate_option]

        # Preprocess gender
        gender = 1 if gender == 'female' else 0

        # Create an input array for prediction
        user_input = np.array([[gender, age, height, weight, duration, heart_rate, body_temp]])

        # Predict calories burned
        calories_burned = model.predict(user_input)

        # Display the prediction
        messagebox.showinfo('Prediction', f'Calories Burned: {calories_burned[0]:.2f}')

    except ValueError as ve:
        messagebox.showerror('Input Error', str(ve))
    except Exception as e:
        messagebox.showerror('Unexpected Error', f'An unexpected error occurred: {e}')

def toggle_heart_rate_entry(*args):
    if heart_rate_var.get() == "Enter Manually":
        heart_rate_entry.grid(row=5, column=2)
        heart_rate_dropdown.grid_forget()
    else:
        heart_rate_entry.grid_forget()
        heart_rate_dropdown.grid(row=5, column=1)

def toggle_body_temp_entry(*args):
    if body_temp_var.get() == "Enter Manually":
        body_temp_entry.grid(row=6, column=2)
        body_temp_dropdown.grid_forget()
    else:
        body_temp_entry.grid_forget()
        body_temp_dropdown.grid(row=6, column=1)

# Create the main window
root = tk.Tk()
root.title("Calories Burned Predictor (Random Forest)")

# Gender input
tk.Label(root, text="Gender (Male/Female):").grid(row=0, column=0)
gender_var = tk.StringVar()
gender_entry = tk.Entry(root, textvariable=gender_var)
gender_entry.grid(row=0, column=1)

# Age input
tk.Label(root, text="Age:").grid(row=1, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)

# Height input
tk.Label(root, text="Height (in cm):").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

# Weight input
tk.Label(root, text="Weight (in kg):").grid(row=3, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=3, column=1)

# Duration input
tk.Label(root, text="Exercise Duration (in minutes):").grid(row=4, column=0)
duration_entry = tk.Entry(root)
duration_entry.grid(row=4, column=1)

# Heart Rate Options
tk.Label(root, text="Heart Rate:").grid(row=5, column=0)
heart_rate_var = tk.StringVar()
heart_rate_options = ["Low", "Medium", "High", "Enter Manually"]
heart_rate_dropdown = tk.OptionMenu(root, heart_rate_var, *heart_rate_options)
heart_rate_dropdown.grid(row=5, column=1)
heart_rate_var.trace('w', toggle_heart_rate_entry)

# Manual Entry for Heart Rate
heart_rate_entry = tk.Entry(root)
heart_rate_entry.grid(row=5, column=2)
heart_rate_entry.grid_remove()

# Body Temperature Options
tk.Label(root, text="Body Temperature:").grid(row=6, column=0)
body_temp_var = tk.StringVar()
body_temp_options = ["Low", "Medium", "High", "Enter Manually"]
body_temp_dropdown = tk.OptionMenu(root, body_temp_var, *body_temp_options)
body_temp_dropdown.grid(row=6, column=1)
body_temp_var.trace('w', toggle_body_temp_entry)

# Manual Entry for Body Temperature
body_temp_entry = tk.Entry(root)
body_temp_entry.grid(row=6, column=2)
body_temp_entry.grid_remove()

# Predict Button
predict_button = tk.Button(root, text="Predict Calories", command=predict_calories)
predict_button.grid(row=7, column=0, columnspan=2)

# Start the Tkinter loop
root.mainloop()
