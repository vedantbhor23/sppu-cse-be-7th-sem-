import threading
import time
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ------------------- MERGE FUNCTION -------------------
def merge(arr, left, mid, right):
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left

    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


# ------------------- NORMAL MERGE SORT -------------------
def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)


# ------------------- MULTITHREADED MERGE SORT -------------------
def threaded_merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        left_thread = threading.Thread(target=threaded_merge_sort, args=(arr, left, mid))
        right_thread = threading.Thread(target=threaded_merge_sort, args=(arr, mid + 1, right))
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()
        merge(arr, left, mid, right)


# ------------------- MAIN FUNCTION (GUI HANDLER) -------------------
def run_sort():
    try:
        n = int(entry_n.get())
        user_input = entry_arr.get().strip()

        if user_input.lower() == "r":
            arr = [random.randint(0, 100000) for _ in range(n)]
        else:
            arr = list(map(int, user_input.split()))
            if len(arr) != n:
                messagebox.showwarning("Input Warning", "Number of elements doesn't match input count.")
                return

        arr1 = arr.copy()
        arr2 = arr.copy()

        # --- Normal Merge Sort ---
        start_time = time.time()
        merge_sort(arr1, 0, len(arr1) - 1)
        normal_time = time.time() - start_time

        # --- Multithreaded Merge Sort ---
        start_time = time.time()
        threaded_merge_sort(arr2, 0, len(arr2) - 1)
        threaded_time = time.time() - start_time

        # --- Display Results ---
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"🌀 Sorted Array (Normal Merge Sort):\n{arr1}\n\n")
        output_text.insert(tk.END, f"⚙️ Sorted Array (Multithreaded Merge Sort):\n{arr2}\n\n")
        output_text.insert(tk.END, f"⏱ Normal Merge Sort Time        : {normal_time:.6f} sec\n")
        output_text.insert(tk.END, f"🚀 Multithreaded Merge Sort Time : {threaded_time:.6f} sec\n")

        if threaded_time < normal_time:
            improvement = ((normal_time - threaded_time) / normal_time) * 100
            output_text.insert(tk.END, f"\n✅ Multithreaded Merge Sort is faster by {improvement:.2f}%!\n")
        elif threaded_time > normal_time:
            slowdown = ((threaded_time - normal_time) / threaded_time) * 100
            output_text.insert(tk.END, f"\n⚠️ Normal Merge Sort performed better (Thread overhead {slowdown:.2f}%).\n")
        else:
            output_text.insert(tk.END, "\n⚖️ Both algorithms performed equally well.\n")

        output_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer inputs.")


# ------------------- STYLING FUNCTION -------------------
def style_widget(widget, bg, fg, font=("Arial", 12), padx=6, pady=6):
    widget.config(bg=bg, fg=fg, font=font, padx=padx, pady=pady)


# ------------------- TKINTER UI SETUP -------------------
root = tk.Tk()
root.title("Merge Sort vs Multithreaded Merge Sort")
root.geometry("800x650")
root.config(bg="#0b132b")

# Header
header = tk.Label(root, text="🔹 Merge Sort vs Multithreaded Merge Sort 🔹", 
                  bg="#1c2541", fg="white", font=("Helvetica", 18, "bold"), pady=15)
header.pack(fill="x")

# Input frame
frame_input = tk.Frame(root, bg="#3a506b", bd=3, relief="ridge")
frame_input.pack(pady=20, padx=20, fill="x")

tk.Label(frame_input, text="Enter number of elements:", bg="#3a506b", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="e")
entry_n = tk.Entry(frame_input, width=10, font=("Arial", 12))
entry_n.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame_input, text="Enter elements (or 'r' for random):", bg="#3a506b", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_arr = tk.Entry(frame_input, width=50, font=("Arial", 12))
entry_arr.grid(row=1, column=1, padx=10, pady=8)

# Run Button
btn_run = tk.Button(root, text="🚀 Run Comparison", command=run_sort,
                    bg="#5bc0be", fg="black", activebackground="#0b132b",
                    font=("Arial", 14, "bold"), relief="raised", bd=4, width=20)
btn_run.pack(pady=15)

# Output box
output_frame = tk.Frame(root, bg="#1c2541", bd=3, relief="ridge")
output_frame.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(output_frame, text="📊 Output & Results:", bg="#1c2541", fg="#fff", font=("Arial", 13, "bold")).pack(pady=5)
output_text = scrolledtext.ScrolledText(output_frame, width=90, height=20, wrap=tk.WORD, font=("Consolas", 11), bg="#f0f0f0", fg="#000", bd=2)
output_text.pack(padx=10, pady=10)
output_text.config(state=tk.DISABLED)

# Footer
footer = tk.Label(root, text="Developed by Vedant Bhor 💻", bg="#0b132b", fg="#5bc0be", font=("Arial", 10, "italic"))
footer.pack(pady=8)

root.mainloop()
