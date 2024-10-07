
import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# D6 and D4 dice rolls
def d6():
    return random.randint(1, 6)

def d4():
    return random.randint(1, 4)

# Simulate hit rolls
def rollHit(Attacks, BallisticSkill):
    hit = 0
    for i in range(Attacks):
        if d6() >= BallisticSkill:
            hit += 1
    return hit

# Simulate wound rolls
def rollWound(hits, Strength, Tough):
    wound = 0
    ratio = Strength / Tough
    for i in range(hits):
        if ratio >= 2 and d6() >= 2:
            wound += 1
        elif 1 < ratio < 2 and d6() >= 3:
            wound += 1
        elif ratio == 1 and d6() >= 4:
            wound += 1
        elif 0.5 < ratio < 1 and d6() >= 5:
            wound += 1
        elif ratio <= 0.5 and d6() >= 6:
            wound += 1
    return wound

# Modify damage based on input format
def damageMod(damage):
    if 'D' in damage:
        pos1 = damage.find('D')
        if '+' in damage:
            pos2 = damage.find('+')
            output = random.randint(1, int(damage[pos1 + 1])) + int(damage[pos2 + 1])
        else:
            output = random.randint(1, int(damage[pos1 + 1]))
    else:
        output = int(damage)
    return output

# Simulate saves
def saves(save, armorP, wounds):
    output = 0
    for i in range(wounds):
        if d6() >= save + abs(armorP):
            output += 1
    return output

# Simulate the math for total damage
def totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units):
    damageList = []
    for iteration in range(iterations):
        AttacksTurn = random.randint(1, Attacks) * Units if 'D' in Attacks else int(Attacks) * Units
        hits = rollHit(AttacksTurn, BallisticSkill)
        wounds = rollWound(hits, Strength, Toughness)
        damageInflicted = (wounds - saves(Save, ArmorP, wounds)) * damageMod(Damage)
        damageList.append(damageInflicted)

    average = np.mean(damageList)
    std_dev = np.std(damageList)
    return average, std_dev

# Function to run the simulation and generate the heatmap
def run_simulation(Attacks, BallisticSkill, Strength, Damage, ArmorP, Units, iterations, progress_bar):
    toughs = list(range(1, 15))
    saves = list(range(1, 7))

    avg_matrix = np.zeros((len(toughs), len(saves)))
    std_matrix = np.zeros((len(toughs), len(saves)))

    progress_bar['value'] = 0
    total_combinations = len(toughs) * len(saves)
    step_value = 100 / total_combinations  # Adjust progress step based on combinations

    for i, Toughness in enumerate(toughs):
        for j, Save in enumerate(saves):
            avg, std = totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units)
            avg_matrix[i][j] = avg
            std_matrix[i][j] = std

            # Update progress bar for each combination of Toughness and Save
            progress_bar['value'] += step_value
            progress_bar.update()

    annot_array = np.empty(avg_matrix.shape, dtype=object)
    for i in range(avg_matrix.shape[0]):
        for j in range(avg_matrix.shape[1]):
            annot_array[i, j] = f"{avg_matrix[i, j]:.1f}\n±{std_matrix[i, j]:.1f}"

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(avg_matrix, annot=annot_array, fmt='', cmap="RdYlGn",
                     xticklabels=[f"{s}+" for s in saves],
                     yticklabels=toughs)
    ax.set_xlabel('Save Values')
    ax.set_ylabel('Toughness')
    plt.title('Average Damage ± Standard Deviation Heatmap')
    plt.show()

# GUI Implementation with Tkinter
def start_gui():
    # Main window
    root = tk.Tk()
    root.title("Warhammer 40K Damage Simulation")

    # Inputs for simulation
    ttk.Label(root, text="Attacks:").grid(row=0, column=0)
    attacks_entry = ttk.Entry(root)
    attacks_entry.grid(row=0, column=1)

    ttk.Label(root, text="Ballistic Skill:").grid(row=1, column=0)
    ballistic_skill_entry = ttk.Entry(root)
    ballistic_skill_entry.grid(row=1, column=1)

    ttk.Label(root, text="Strength:").grid(row=2, column=0)
    strength_entry = ttk.Entry(root)
    strength_entry.grid(row=2, column=1)

    ttk.Label(root, text="Damage:").grid(row=3, column=0)
    damage_entry = ttk.Entry(root)
    damage_entry.grid(row=3, column=1)

    ttk.Label(root, text="Armor Penetration (AP):").grid(row=4, column=0)
    armorP_entry = ttk.Entry(root)
    armorP_entry.grid(row=4, column=1)

    ttk.Label(root, text="Units:").grid(row=5, column=0)
    units_entry = ttk.Entry(root)
    units_entry.grid(row=5, column=1)

    ttk.Label(root, text="Iterations:").grid(row=6, column=0)
    iterations_scale = ttk.Scale(root, from_=100, to=5000, orient="horizontal")
    iterations_scale.grid(row=6, column=1)

    # Progress bar
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.grid(row=7, column=0, columnspan=2, pady=10)

    # Button to run the simulation
    def run():
        Attacks = attacks_entry.get()
        BallisticSkill = int(ballistic_skill_entry.get())
        Strength = int(strength_entry.get())
        Damage = damage_entry.get()
        ArmorP = int(armorP_entry.get())
        Units = int(units_entry.get())
        iterations = int(iterations_scale.get())

        run_simulation(Attacks, BallisticSkill, Strength, Damage, ArmorP, Units, iterations, progress)

    run_button = ttk.Button(root, text="Run Simulation", command=run)
    run_button.grid(row=8, column=0, columnspan=2)

    root.mainloop()

# Start the GUI
start_gui()
