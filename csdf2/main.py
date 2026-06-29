import hashlib
import json
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ------------------------------
# 1. Calculate SHA-256 hash
# ------------------------------
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None


# ------------------------------
# 2. Store initial hashes
# ------------------------------
def store_hashes(file_paths, db_file="hashes.json"):
    hashes = {}
    for file_path in file_paths:
        file_hash = calculate_hash(file_path)
        if file_hash:
            hashes[file_path] = file_hash
    with open(db_file, "w") as f:
        json.dump(hashes, f)
    messagebox.showinfo("✅ Success", f"Hashes stored in {db_file}")


# ------------------------------
# 3. Verify all files
# ------------------------------
def verify_all(db_file="hashes.json"):
    if not os.path.exists(db_file):
        messagebox.showerror("⚠️ Error", "No stored hashes found. Run 'Store Hashes' first.")
        return None

    with open(db_file, "r") as f:
        stored_hashes = json.load(f)

    results = {}
    for file_path, old_hash in stored_hashes.items():
        new_hash = calculate_hash(file_path)
        if not new_hash:
            status = "❌ File not found"
        elif old_hash == new_hash:
            status = "✅ SAFE"
        else:
            status = "⚠️ MODIFIED"
        results[file_path] = status
    return results


# ------------------------------
# 4. Generate forensic report
# ------------------------------
def generate_report(results, report_dir="."):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"Forensic_Report_{timestamp}.txt"
    report_path = os.path.join(report_dir, report_name)

    with open(report_path, "w", encoding="utf-8") as report:
        for file_path, status in results.items():
            line = f"{file_path} → {status}\n"
            report.write(line)

    messagebox.showinfo("📄 Report Generated", f"Forensic report saved at:\n{report_path}")


# ------------------------------
# 5. GUI Functions
# ------------------------------
def browse_files():
    files = filedialog.askopenfilenames(title="Select Files to Monitor")
    file_list.delete(1.0, tk.END)
    for f in files:
        file_list.insert(tk.END, f + "\n")


def store_hash_button():
    files = file_list.get(1.0, tk.END).strip().split("\n")
    if not files or files == ['']:
        messagebox.showwarning("⚠️ No Files", "Please select files first.")
        return
    store_hashes(files)


def verify_button():
    results = verify_all()
    if results:
        output_text.delete(1.0, tk.END)
        for file_path, status in results.items():
            output_text.insert(tk.END, f"{file_path} → {status}\n")
        generate_report(results, os.getcwd())


# ------------------------------
# 6. Button Hover Effects
# ------------------------------
def on_enter(e):
    e.widget['background'] = "#73c2fb"

def on_leave(e):
    e.widget['background'] = "#4da6ff"


# ------------------------------
# 7. Tkinter GUI Layout
# ------------------------------
root = tk.Tk()
root.title("File Integrity Monitoring Tool")
root.geometry("800x550")
root.configure(bg="#f3f4fb")

# Header Frame with gradient effect using Canvas
header = tk.Canvas(root, width=800, height=80, bg="#89cff0", highlightthickness=0)
header.pack(fill="x")

# Simulate a gradient by layering rectangles
for i in range(80):
    color = f"#89cff0"
    header.create_rectangle(0, i, 800, i+1, fill=color, outline=color)

header_text = header.create_text(
    400, 40,
    text="🔒 File Integrity Monitoring Tool",
    font=("Segoe UI", 20, "bold"),
    fill="white"
)

# Frame for buttons
frame = tk.Frame(root, bg="#f3f4fb")
frame.pack(pady=20)

style = {
    "bg": "#4da6ff",
    "fg": "white",
    "font": ("Segoe UI", 10, "bold"),
    "relief": "flat",
    "width": 15,
    "height": 2,
    "bd": 0
}

browse_btn = tk.Button(frame, text="📁 Browse Files", command=browse_files, **style)
browse_btn.grid(row=0, column=0, padx=10)
browse_btn.bind("<Enter>", on_enter)
browse_btn.bind("<Leave>", on_leave)

store_btn = tk.Button(frame, text="💾 Store Hashes", command=store_hash_button, **style)
store_btn.grid(row=0, column=1, padx=10)
store_btn.bind("<Enter>", on_enter)
store_btn.bind("<Leave>", on_leave)

verify_btn = tk.Button(frame, text="🧩 Verify Files", command=verify_button, **style)
verify_btn.grid(row=0, column=2, padx=10)
verify_btn.bind("<Enter>", on_enter)
verify_btn.bind("<Leave>", on_leave)

# File list section
file_list_label = tk.Label(root, text="📂 Selected Files:", bg="#f3f4fb", font=("Segoe UI", 11, "bold"), fg="#333")
file_list_label.pack(anchor="w", padx=20)

file_list = scrolledtext.ScrolledText(root, height=7, width=90, font=("Consolas", 10))
file_list.pack(padx=20, pady=5)

# Output section
output_label = tk.Label(root, text="🧾 Verification Output:", bg="#f3f4fb", font=("Segoe UI", 11, "bold"), fg="#333")
output_label.pack(anchor="w", padx=20, pady=(10, 0))

output_text = scrolledtext.ScrolledText(root, height=10, width=90, font=("Consolas", 10))
output_text.pack(padx=20, pady=5)

# Footer
footer = tk.Label(root, text="© 2025 Cyber Forensics Lab | Powered by SHA-256 Verification", bg="#f3f4fb", fg="#777", font=("Segoe UI", 9))
footer.pack(side="bottom", pady=10)

root.mainloop()
