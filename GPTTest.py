import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

def d6():
    return random.randint(1, 6)

def rollHit(Attacks, BallisticSkill, Keywords):
    hit = 0
    crit_hits = 0
    auto_wounds = 0
    for i in range(Attacks):
        roll = d6()
        if roll >= BallisticSkill:
            hit += 1
        # Check for Critical Hits (natural 6s)
        if roll == 6:
            if 'SUSTAINED HITS X' in Keywords:
                crit_hits += int(Keywords[Keywords.index('SUSTAINED HITS X') + 1])
            if 'LETHAL HITS' in Keywords:
                auto_wounds += 1
    return hit + crit_hits, auto_wounds

def rollWound(hits, auto_wounds, Strength, Tough, Keywords):
    wound = auto_wounds
    reroll_count = 0
    ratio = Strength / Tough
    for i in range(hits):
        roll = d6()
        if ratio >= 2 and roll >= 2:
            wound += 1
        elif ratio > 1 and roll >= 3:
            wound += 1
        elif ratio == 1 and roll >= 4:
            wound += 1
        elif ratio > 0.5 and roll >= 5:
            wound += 1
        elif roll >= 6:
            wound += 1
        # Apply Twin-Linked for rerolls
        if roll < 6 and 'TWIN-LINKED' in Keywords:
            reroll_count += 1  # Count the number of rerolls allowed

    # Twin-Linked rerolls
    for _ in range(reroll_count):
        reroll = d6()
        if ratio >= 2 and reroll >= 2:
            wound += 1
        elif ratio > 1 and reroll >= 3:
            wound += 1
        elif ratio == 1 and reroll >= 4:
            wound += 1
        elif ratio > 0.5 and reroll >= 5:
            wound += 1
        elif reroll >= 6:
            wound += 1
            
    return wound

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

def saves(save, armorP, wounds, Keywords):
    output = 0
    for i in range(wounds):
        roll = d6()
        if roll >= save + abs(armorP):
            # Check for Devastating Wounds which ignore saves
            if 'DEVASTATING WOUNDS' in Keywords and roll == 6:
                continue  # Ignore saving throw on a 6
            output += 1
    return output

def howmanyAttacks(Attacks):
    if 'D' in Attacks:
        output = random.randint(1, int(Attacks[Attacks.find('D') + 1]))
    else:
        output = int(Attacks)
    return output

def indiMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, Units, Keywords):
    AttacksTurn = howmanyAttacks(Attacks) * Units
    hits, auto_wounds = rollHit(AttacksTurn, BallisticSkill, Keywords)
    wounds = rollWound(hits, auto_wounds, Strength, Toughness, Keywords)
    damageInflicted = (wounds - saves(Save, ArmorP, wounds, Keywords)) * damageMod(Damage)
    return damageInflicted

def totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units, Keywords):
    damageList = []
    for i in range(iterations):
        AttacksTurn = howmanyAttacks(Attacks) * Units
        hits, auto_wounds = rollHit(AttacksTurn, BallisticSkill, Keywords)
        wounds = rollWound(hits, auto_wounds, Strength, Toughness, Keywords)
        damageInflicted = (wounds - saves(Save, ArmorP, wounds, Keywords)) * damageMod(Damage)
        damageList.append(damageInflicted)
    average = np.mean(damageList)
    std_dev = np.std(damageList)
    return average, std_dev

def show_heatmap(avg_matrix, std_matrix, toughs, saves):
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

def calculate():
    try:
        Units = int(unit_entry.get())
        Attacks = attack_entry.get()
        BallisticSkill = int(bs_entry.get())
        ArmorP = int(ap_entry.get())
        Strength = int(strength_entry.get())
        Damage = damage_entry.get()
        iterations = 500

        Keywords = []
        if keyword_lethal_hits.get():
            Keywords.append('LETHAL HITS')
        if keyword_sustained_hits.get():
            Keywords.append('SUSTAINED HITS X')
        if keyword_twin_linked.get():
            Keywords.append('TWIN-LINKED')
        if keyword_devastating_wounds.get():
            Keywords.append('DEVASTATING WOUNDS')

        toughs = list(range(1, 15))
        saves = list(range(1, 7))

        avg_matrix = np.zeros((len(toughs), len(saves)))
        std_matrix = np.zeros((len(toughs), len(saves)))

        for i, Toughness in enumerate(toughs):
            for j, Save in enumerate(saves):
                average, std_dev = totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units, Keywords)
                avg_matrix[i][j] = average
                std_matrix[i][j] = std_dev

        show_heatmap(avg_matrix, std_matrix, toughs, saves)

    except ValueError:
        messagebox.showerror("Input Error", "Please make sure all fields are filled correctly.")

# GUI using Tkinter
root = tk.Tk()
root.title("Warhammer 40k Damage Calculator")

# Unit Input
ttk.Label(root, text="How many units:").grid(row=0, column=0)
unit_entry = ttk.Entry(root)
unit_entry.grid(row=0, column=1)

# Attacks Input
ttk.Label(root, text="How many attacks (can be dice roll):").grid(row=1, column=0)
attack_entry = ttk.Entry(root)
attack_entry.grid(row=1, column=1)

# Ballistic Skill Input
ttk.Label(root, text="Ballistic Skill:").grid(row=2, column=0)
bs_entry = ttk.Entry(root)
bs_entry.grid(row=2, column=1)

# Armor Penetration Input
ttk.Label(root, text="Armor Penetration (AP):").grid(row=3, column=0)
ap_entry = ttk.Entry(root)
ap_entry.grid(row=3, column=1)

# Strength Input
ttk.Label(root, text="Strength:").grid(row=4, column=0)
strength_entry = ttk.Entry(root)
strength_entry.grid(row=4, column=1)

# Damage Input
ttk.Label(root, text="Damage (can be string):").grid(row=5, column=0)
damage_entry = ttk.Entry(root)
damage_entry.grid(row=5, column=1)

# Weapon Keywords (Checkboxes)
ttk.Label(root, text="Select Weapon Keywords:").grid(row=6, column=0, columnspan=2)

keyword_lethal_hits = tk.BooleanVar()
keyword_sustained_hits = tk.BooleanVar()
keyword_twin_linked = tk.BooleanVar()
keyword_devastating_wounds = tk.BooleanVar()

ttk.Checkbutton(root, text="Lethal Hits", variable=keyword_lethal_hits).grid(row=7, column=0)
ttk.Checkbutton(root, text="Sustained Hits X", variable=keyword_sustained_hits).grid(row=7, column=1)
ttk.Checkbutton(root, text="Twin-Linked", variable=keyword_twin_linked).grid(row=8, column=0)
ttk.Checkbutton(root, text="Devastating Wounds", variable=keyword_devastating_wounds).grid(row=8, column=1)

# Calculate Button
calculate_button = ttk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=9, column=0, columnspan=2)

# Start the Tkinter loop
root.mainloop()
