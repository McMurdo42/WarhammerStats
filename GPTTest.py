import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from multiprocessing import Pool, cpu_count

def d6(size=1):
    return np.random.randint(1, 7, size)

def rollHit(Attacks, BallisticSkill):
    hits = d6(Attacks) >= BallisticSkill
    return np.sum(hits)

def rollWound(hits, Strength, Tough):
    ratio = Strength / Tough
    if ratio >= 2:
        return np.sum(d6(hits) >= 2)
    elif ratio > 1:
        return np.sum(d6(hits) >= 3)
    elif ratio == 1:
        return np.sum(d6(hits) >= 4)
    elif ratio > 0.5:
        return np.sum(d6(hits) >= 5)
    else:
        return np.sum(d6(hits) >= 6)

def damageMod(damage):
    if 'D' in damage:
        pos1 = damage.find('D')
        if '+' in damage:
            pos2 = damage.find('+')
            output = np.random.randint(1, int(damage[pos1 + 1]) + 1) + int(damage[pos2 + 1])
        else:
            output = np.random.randint(1, int(damage[pos1 + 1]) + 1)
    else:
        output = int(damage)
    return output

def saves(save, armorP, wounds):
    rolls = d6(wounds)
    return np.sum(rolls >= save + abs(armorP))

def howmanyAttacks(Attacks):
    if 'D' in Attacks:
        return np.random.randint(1, int(Attacks[Attacks.find('D') + 1]) + 1)
    else:
        return int(Attacks)

def single_iteration(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, Units):
    num_attacks = howmanyAttacks(Attacks) * Units
    hits = rollHit(num_attacks, BallisticSkill)
    wounds = rollWound(hits, Strength, Toughness)
    unsaved_wounds = wounds - saves(Save, ArmorP, wounds)
    damage = unsaved_wounds * damageMod(Damage)
    return damage

def totMath_parallel(args):
    Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units = args
    damageList = []

    with Pool(processes=cpu_count()) as pool:
        # Split the iterations across available cores
        results = pool.map(single_iteration_wrapper, [(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, Units)] * iterations)
        damageList.extend(results)

    return np.mean(damageList), np.std(damageList)

def single_iteration_wrapper(args):
    return single_iteration(*args)

def mainloop(Units, Attacks, BallisticSkill, ArmorP, Strength, Damage):
    iterations = 5000

    toughs = np.arange(1, 15)
    saves = np.arange(1, 7)

    avg_matrix = np.zeros((len(toughs), len(saves)))
    std_matrix = np.zeros((len(toughs), len(saves)))

    plt.figure(figsize=(10, 8))

    for i, Toughness in enumerate(toughs):
        for j, Save in enumerate(saves):
            # Perform calculations using the inputs
            average, std_dev = totMath_parallel((Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units))
            avg_matrix[i][j] = average
            std_matrix[i][j] = std_dev

            # Create and update the heatmap dynamically
            plt.clf()
            ax = sns.heatmap(avg_matrix, annot=True, fmt='', cmap="RdYlGn", 
                             xticklabels=[f"{s}+" for s in saves], 
                             yticklabels=toughs)

            ax.set_xlabel('Save Values')
            ax.set_ylabel('Toughness')
            plt.title('Average Damage ± Standard Deviation Heatmap')

            plt.pause(0.1)

    plt.show()

if __name__ == "__main__":
    # Collect input outside of the mainloop and multiprocessing logic
    Units = int(input('How many units: '))
    Attacks = input('How many attacks (can be dice roll): ')
    BallisticSkill = int(input('BallisticSkill: '))
    ArmorP = int(input('AP: '))
    Strength = int(input('Strength: '))
    Damage = str(input('Damage (can be string): '))

    # Pass inputs to the mainloop
    mainloop(Units, Attacks, BallisticSkill, ArmorP, Strength, Damage)
