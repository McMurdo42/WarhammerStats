import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
import os

# Helper function to convert BallisticSkill or WeaponSkill values like "3+" into numeric thresholds
def convert_skill(skill):
    return int(skill.replace("+", ""))

# Helper function to parse the attacks (e.g., "Assault D6" or "Heavy 1")
def parse_attacks(attacks):
    if "D" in attacks:
        dice_type = attacks.split()[1]
        if "D6" in dice_type:
            return random.randint(1, 6)
        elif "D3" in dice_type:
            return random.randint(1, 3)
    else:
        return int(attacks.split()[1])

# Function to read weapons from CSV including Special attributes
def load_weapons_from_csv(filename):
    weapons = {}
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            weapons[row["Weapon Name"]] = {
                "Attacks": row["Attacks"],
                "BallisticSkill": convert_skill(row["BallisticSkill"]),
                "Damage": row["Damage"],
                "Strength": int(row["Strength"]) if row["Strength"] != "User" else "User",
                "ArmorP": int(row["ArmorP"]),
                "Units": int(row["Units"]),
                "Special": row["Special"]
            }
    return weapons

def d6():
    return random.randint(1, 6)

def rollHit(Attacks, BallisticSkill, special=None):
    hit = 0
    for i in range(0, Attacks):
        roll = d6()
        # Example: Handle "Bladestorm" (critical hit on a 6 causing extra AP)
        if special and "Bladestorm" in special and roll == 6:
            hit += 1
        if roll >= BallisticSkill:
            hit += 1
    return hit

def rollWound(hits, Strength, Tough, special=None):
    wound = 0
    ratio = Strength / Tough if Strength != "User" else 1  # Simplified for now
    for i in range(0, hits):
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
        # Handle "Melta" or other special rules here
    return wound

def damageMod(damage):
    if 'D' in damage:
        pos1 = damage.find('D')
        if '+' in damage:
            pos2 = damage.find('+')
            return random.randint(1, int(damage[pos1+1])) + int(damage[pos2+1])
        else:
            return random.randint(1, int(damage[pos1+1]))
    else:
        return int(damage)

def saves(save, armorP, wounds):
    output = 0
    for i in range(0, wounds):
        if d6() >= save + abs(armorP):
            output += 1
    return output

def totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units, special=None):
    damageList = []
    for i in range(0, iterations):
        AttacksTurn = parse_attacks(Attacks) * Units
        hits = rollHit(AttacksTurn, BallisticSkill, special)
        wounds = rollWound(hits, Strength, Toughness, special)
        damageInflicted = (wounds - saves(Save, ArmorP, wounds)) * damageMod(Damage)
        damageList.append(damageInflicted)
    average = np.mean(damageList)
    std_dev = np.std(damageList)
    return average, std_dev

# Function to generate heatmap for a weapon including special rules
def generate_heatmap_for_weapon(weapon_name, weapon, iterations=3000, save_dir="heatmaps"):
    Attacks = weapon['Attacks']
    BallisticSkill = weapon['BallisticSkill']
    Damage = weapon['Damage']
    Strength = weapon['Strength'] if weapon['Strength'] != "User" else 4  # Example for "User" based strength
    ArmorP = weapon['ArmorP']
    Units = weapon['Units']  # Use the number of units from the weapon profile
    Special = weapon['Special']  # Use the special attributes from the weapon profile

    toughs = list(range(1, 15))
    saves = list(range(1, 7))

    # Create 2D arrays to store the average and standard deviation
    avg_matrix = np.zeros((len(toughs), len(saves)))
    std_matrix = np.zeros((len(toughs), len(saves)))

    # Perform calculations for each Toughness and Save combination
    for i, Toughness in enumerate(toughs):
        for j, Save in enumerate(saves):
            average, std_dev = totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units, Special)
            avg_matrix[i][j] = average
            std_matrix[i][j] = std_dev

    # Create an annotation array to show average and standard deviation together
    annot_array = np.empty(avg_matrix.shape, dtype=object)
    for i in range(avg_matrix.shape[0]):
        for j in range(avg_matrix.shape[1]):
            annot_array[i, j] = f"{avg_matrix[i, j]:.1f}\n±{std_matrix[i, j]:.1f}"

    # Create a heatmap using seaborn
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(avg_matrix, annot=annot_array, fmt='', cmap="RdYlGn", 
                     xticklabels=[f"{s}+" for s in saves], 
                     yticklabels=toughs)

    ax.set_xlabel('Save Values')
    ax.set_ylabel('Toughness')
    plt.title(f'Average Damage ± Standard Deviation Heatmap: {weapon_name} ({Units} units)')

    # Ensure the directory for saving heatmaps exists
    os.makedirs(save_dir, exist_ok=True)

    # Save the plot to a file
    heatmap_filename = os.path.join(save_dir, f"{weapon_name.replace(' ', '_')}_heatmap.png")
    plt.savefig(heatmap_filename)
    plt.close()

    print(f"Heatmap saved for {weapon_name}: {heatmap_filename}")

# Main loop to generate heatmaps for every weapon in the CSV
def mainloop():
    weapons = load_weapons_from_csv('aeldari_weapons_full_special.csv')  # Load from CSV with special attributes

    # Generate heatmap for every weapon
    for weapon_name, weapon_data in weapons.items():
        print(f"Generating heatmap for {weapon_name} with {weapon_data['Units']} units and special rule: {weapon_data['Special']}...")
        generate_heatmap_for_weapon(weapon_name, weapon_data)

mainloop()
