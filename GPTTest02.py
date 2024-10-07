import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import threading
import time


# Function to run iterations with a progress bar
def run_iterations(stats, iterations, progress_var, progress_label):
    for i in tqdm(range(iterations)):
        # Simulating some processing with time.sleep
        time.sleep(0.1)  # Simulate some time-consuming computation
        
        # Update the progress bar
        progress = int((i + 1) / iterations * 100)
        progress_var.set(progress)
        progress_label.config(text=f'Progress: {progress}%')
    
    # Update progress label when done
    progress_label.config(text='Completed!')


# Function to start the iteration process
def start_iterations():
    # Fetch input stats from the user interface
    stats = {
        'attack': int(attack_entry.get()),
        'defense': int(defense_entry.get()),
        'damage': int(damage_entry.get()),
    }
    
    # Fetch the number of iterations from the user interface
    iterations = int(iterations_entry.get())
    
    # Reset progress
    progress_var.set(0)
    progress_label.config(text="Starting...")
    
    # Start a thread to run the iterations, ensuring the UI remains responsive
    threading.Thread(target=run_iterations, args=(stats, iterations, progress_var, progress_label)).start()


# Set up the UI
root = tk.Tk()
root.title("Stats Input and Iteration Runner")

# Labels and entries for stats input
tk.Label(root, text="Attack:").grid(row=0, column=0, padx=10, pady=5)
attack_entry = tk.Entry(root)
attack_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Defense:").grid(row=1, column=0, padx=10, pady=5)
defense_entry = tk.Entry(root)
defense_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Damage:").grid(row=2, column=0, padx=10, pady=5)
damage_entry = tk.Entry(root)
damage_entry.grid(row=2, column=1, padx=10, pady=5)

# Entry for the number of iterations
tk.Label(root, text="Iterations:").grid(row=3, column=0, padx=10, pady=5)
iterations_entry = tk.Entry(root)
iterations_entry.grid(row=3, column=1, padx=10, pady=5)

# Progress bar and label
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

progress_label = tk.Label(root, text="Progress: 0%")
progress_label.grid(row=5, column=0, columnspan=2)

# Start button to trigger the iteration process
start_button = tk.Button(root, text="Start Iterations", command=start_iterations)
start_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
