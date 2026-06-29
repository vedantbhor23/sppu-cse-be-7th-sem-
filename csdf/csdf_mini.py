# forgery_ui_orange_fixed_multi.py
import cv2
import numpy as np
from PIL import Image, ImageTk, ExifTags
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# ------------------------ CONFIG ------------------------
ELA_OUTPUT = "ela_result.jpg"
EDGES_OUTPUT = "edges_result.jpg"
TEMP_ELA = "temp_ela.jpg"
PREVIEW_SIZE = (350, 350)

# ------------------------ CORE ANALYSIS FUNCTIONS ------------------------
def error_level_analysis(image_path, temp_filename=TEMP_ELA, quality=90):
    original = Image.open(image_path).convert("RGB")
    original.save(temp_filename, "JPEG", quality=quality)
    compressed = Image.open(temp_filename).convert("RGB")

    diff = np.abs(np.asarray(original, dtype=np.int16) - np.asarray(compressed, dtype=np.int16))
    extrema = diff.max()
    scale = 255.0 / extrema if extrema != 0 else 1.0
    diff = (diff * scale).astype(np.uint8)
    ela_image = Image.fromarray(diff)

    try:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    except Exception:
        pass
    return ela_image.convert("RGB")

def metadata_analysis(image_path):
    exif_data = {}
    try:
        image = Image.open(image_path)
        if hasattr(image, "_getexif") and image._getexif():
            for tag, value in image._getexif().items():
                name = ExifTags.TAGS.get(tag, tag)
                exif_data[name] = value
    except Exception:
        return {}
    return exif_data

def edge_analysis(image_path):
    img_cv = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img_cv is None:
        raise FileNotFoundError(f"cv2 could not read image: {image_path}")
    edges = cv2.Canny(img_cv, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(edges_rgb)

# ------------------------ GUI SETUP ------------------------
root = tk.Tk()
root.title("🧠 Image Forgery Detection (Orange Theme)")
root.geometry("1200x750")
root.config(bg="#1c1a17")
root.resizable(False, False)

title = tk.Label(root, text="🔍 Image Forgery Detection System",
                 bg="#1c1a17", fg="#f4a261", font=("Arial", 22, "bold"))
title.pack(pady=12)

frame_buttons = tk.Frame(root, bg="#1c1a17")
frame_buttons.pack(pady=6)

selected_images = []  # store multiple paths

# ------------------------ IMAGE PANELS ------------------------
frame_display = tk.Frame(root, bg="#1c1a17")
frame_display.pack(pady=10)

blank = Image.new("RGB", PREVIEW_SIZE, (45, 42, 37))
blank_tk = ImageTk.PhotoImage(blank)

lbl_original = tk.Label(frame_display, image=blank_tk, bg="#2b2a27")
lbl_original.image = blank_tk
lbl_original.grid(row=0, column=0, padx=12)

lbl_ela = tk.Label(frame_display, image=blank_tk, bg="#2b2a27")
lbl_ela.image = blank_tk
lbl_ela.grid(row=0, column=1, padx=12)

lbl_edges = tk.Label(frame_display, image=blank_tk, bg="#2b2a27")
lbl_edges.image = blank_tk
lbl_edges.grid(row=0, column=2, padx=12)

tk.Label(frame_display, text="Original", bg="#1c1a17", fg="#f4a261", font=("Arial", 12, "bold")).grid(row=1, column=0, pady=6)
tk.Label(frame_display, text="ELA Result", bg="#1c1a17", fg="#f4a261", font=("Arial", 12, "bold")).grid(row=1, column=1, pady=6)
tk.Label(frame_display, text="Edges Result", bg="#1c1a17", fg="#f4a261", font=("Arial", 12, "bold")).grid(row=1, column=2, pady=6)

# ------------------------ METADATA BOX ------------------------
frame_meta = tk.LabelFrame(root, text="📋 Metadata Information", bg="#1c1a17", fg="#f4a261", font=("Arial", 14, "bold"))
frame_meta.pack(fill="both", expand=False, padx=18, pady=12)

text_meta = tk.Text(frame_meta, height=6, bg="#2b2a27", fg="white", font=("Consolas", 11))
text_meta.pack(fill="both", expand=True, padx=8, pady=8)

# ------------------------ STATUS & FOOTER ------------------------
lbl_status = tk.Label(root, text="No image selected", bg="#1c1a17", fg="#e9c46a", font=("Arial", 11, "italic"))
lbl_status.pack(pady=6)

footer = tk.Label(root, text="Developed by Vedant Bhor 💻",
                  bg="#1c1a17", fg="#f4a261", font=("Arial", 10, "italic"))
footer.pack(side="bottom", fill="x", pady=8)

# ------------------------ BUTTON BEHAVIOR ------------------------
def browse_images():
    global selected_images
    paths = filedialog.askopenfilenames(title="Select one or more images",
                                        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if not paths:
        return
    selected_images = list(paths)
    lbl_status.config(text=f"{len(selected_images)} image(s) selected", fg="#e76f51")
    text_meta.delete("1.0", tk.END)

    # preview first image
    try:
        img = Image.open(selected_images[0]).convert("RGB").resize(PREVIEW_SIZE, Image.LANCZOS)
        tkimg = ImageTk.PhotoImage(img)
        lbl_original.config(image=tkimg)
        lbl_original.image = tkimg
    except Exception as ex:
        messagebox.showerror("Error", f"Failed to open image: {ex}")
        selected_images = []

def run_analysis():
    global selected_images
    if not selected_images:
        messagebox.showwarning("No image", "Please select one or more images first.")
        return

    for idx, img_path in enumerate(selected_images, start=1):
        lbl_status.config(text=f"Analyzing ({idx}/{len(selected_images)}): {os.path.basename(img_path)}", fg="#ffbe0b")
        root.update_idletasks()

        # metadata
        try:
            meta = metadata_analysis(img_path)
            text_meta.delete("1.0", tk.END)
            if meta:
                for k, v in meta.items():
                    text_meta.insert(tk.END, f"{k}: {v}\n")
            else:
                text_meta.insert(tk.END, "No metadata found or stripped from image.")
        except Exception as ex:
            text_meta.delete("1.0", tk.END)
            text_meta.insert(tk.END, f"Metadata read error: {ex}")

        # ELA
        try:
            ela = error_level_analysis(img_path)
            ela_resized = ela.resize(PREVIEW_SIZE, Image.LANCZOS)
            ela_tk = ImageTk.PhotoImage(ela_resized)
            lbl_ela.config(image=ela_tk)
            lbl_ela.image = ela_tk
            ela.save(f"ELA_{os.path.basename(img_path)}")
        except Exception as ex:
            messagebox.showerror("ELA Error", f"Error during ELA: {ex}")
            lbl_ela.config(image=blank_tk)
            lbl_ela.image = blank_tk

        # Edges
        try:
            edges = edge_analysis(img_path)
            edges_resized = edges.resize(PREVIEW_SIZE, Image.LANCZOS)
            edges_tk = ImageTk.PhotoImage(edges_resized)
            lbl_edges.config(image=edges_tk)
            lbl_edges.image = edges_tk
            edges.save(f"Edges_{os.path.basename(img_path)}")
        except Exception as ex:
            messagebox.showerror("Edges Error", f"Error during edge detection: {ex}")
            lbl_edges.config(image=blank_tk)
            lbl_edges.image = blank_tk

    lbl_status.config(text="✅ Analysis completed for all selected images!", fg="#f4a261")

# Hover effects
def on_enter(e):
    e.widget.config(bg="#e76f51", fg="white")
def on_leave(e):
    e.widget.config(bg="#f4a261", fg="#1c1a17")

btn_style = {
    "font": ("Arial", 13, "bold"),
    "bg": "#f4a261",
    "fg": "#1c1a17",
    "relief": "flat",
    "padx": 16,
    "pady": 8,
    "cursor": "hand2"
}

btn_select = tk.Button(frame_buttons, text="📁 Select Images", command=browse_images, **btn_style)
btn_select.grid(row=0, column=0, padx=12)
btn_select.bind("<Enter>", on_enter); btn_select.bind("<Leave>", on_leave)

btn_run = tk.Button(frame_buttons, text="🔎 Run Analysis", command=run_analysis, **btn_style)
btn_run.grid(row=0, column=1, padx=12)
btn_run.bind("<Enter>", on_enter); btn_run.bind("<Leave>", on_leave)

# Start GUI
root.mainloop()
