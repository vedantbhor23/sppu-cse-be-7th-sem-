# titanic_ui_pink.py
# 💖 Pink-Themed Tkinter UI for Titanic Survival Prediction

import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd

# ------------------- Load Model -------------------
  
try:
    model = joblib.load("titanic_model.pkl")
except Exception as e:
    messagebox.showerror("Model Error", f"Could not load model: {e}")
    exit()

# ------------------- Prediction Function -------------------
def predict_survival():
    try:
        Pclass = int(pclass_var.get())
        Sex = sex_var.get().strip().lower()
        Age = float(age_var.get())
        SibSp = int(sibsp_var.get())
        Parch = int(parch_var.get())
        Fare = float(fare_var.get())
        Embarked = embarked_var.get().strip().upper()

        input_data = pd.DataFrame([{
            "Pclass": Pclass,
            "Sex": Sex,
            "Age": Age,
            "SibSp": SibSp,
            "Parch": Parch,
            "Fare": Fare,
            "Embarked": Embarked
        }])

        prediction = model.predict(input_data)[0]
        result = "💗 Survived" if prediction == 1 else "💔 Did Not Survive"

        messagebox.showinfo("Prediction Result", f"Prediction: {result}")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input: {e}")

# ------------------- UI Setup -------------------
root = tk.Tk()
root.title("💖 Titanic Survival Predictor")
root.geometry("450x600")
root.config(bg="#4A0E28")  # Deep rose background

# ------------------- Styling -------------------
TITLE_FONT = ("Segoe UI", 18, "bold")
LABEL_FONT = ("Segoe UI", 12)
ENTRY_FONT = ("Segoe UI", 12)
BUTTON_FONT = ("Segoe UI", 14, "bold")

ACCENT_COLOR = "#FF5C8D"     # Bright pink accent
ENTRY_BG = "#732642"         # Muted rose for entry boxes
TEXT_COLOR = "#FFE6F2"       # Soft pinkish white text

# ------------------- Header -------------------
tk.Label(root, text="💖 Titanic Survival Predictor", font=TITLE_FONT,
         fg=ACCENT_COLOR, bg="#4A0E28").pack(pady=20)

# ------------------- Frame -------------------
form_frame = tk.Frame(root, bg="#4A0E28")
form_frame.pack(pady=10)

labels = [
    "Pclass (1-3)",
    "Sex (male/female)",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked (C/Q/S)"
]

vars_ = []
for lbl in labels:
    tk.Label(form_frame, text=lbl, font=LABEL_FONT, fg=TEXT_COLOR,
             bg="#4A0E28", anchor="w").pack(fill='x', padx=40, pady=5)
    var = tk.StringVar()
    entry = tk.Entry(form_frame, textvariable=var, font=ENTRY_FONT,
                     width=30, bg=ENTRY_BG, fg=TEXT_COLOR,
                     insertbackground=TEXT_COLOR, relief="flat",
                     highlightthickness=2, highlightbackground="#FFB6C1")
    entry.pack(pady=5)
    vars_.append(var)

pclass_var, sex_var, age_var, sibsp_var, parch_var, fare_var, embarked_var = vars_

# ------------------- Button Hover Effect -------------------
def on_enter(e):
    e.widget.config(bg="#FF8FAB", fg="white")

def on_leave(e):
    e.widget.config(bg=ACCENT_COLOR, fg="white")

# ------------------- Predict Button -------------------
predict_btn = tk.Button(root, text="Predict 💫", font=BUTTON_FONT,
                        bg=ACCENT_COLOR, fg="white", relief="flat",
                        padx=10, pady=8, command=predict_survival,
                        cursor="hand2", activebackground="#FF8FAB")
predict_btn.pack(pady=25)

predict_btn.bind("<Enter>", on_enter)
predict_btn.bind("<Leave>", on_leave)

# ------------------- Footer -------------------
tk.Label(root, text="Developed by Vedant Bhor 💻", font=("Segoe UI", 10, "italic"),
         bg="#4A0E28", fg="#FFB6C1").pack(pady=15)

# ------------------- Run -------------------
root.mainloop()
