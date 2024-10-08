import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def d6():
    return random.randint(1,6)

def d4():
    return random.randint(1,4)

def rollHit(Attacks,BallisticSkill):
    hit = 0
    for i in range(0,Attacks):
        if d6() >= BallisticSkill:
            hit += 1
    return hit

def rollWound(hits,Strength,Tough):
    wound = 0
    ratio = Strength/Tough
    for i in range(0,hits):
        if ratio >= 2:
            if d6() >= 2:
                wound += 1
        elif ratio > 1:
            if d6() >= 3:
                wound += 1
        elif ratio == 1:
            if d6() >= 4:
                wound += 1
        elif ratio > 0.5:
            if d6() >= 5:
                wound += 1
        else:
            if d6() >= 6:
                wound += 1
    return wound

def damageMod(damage):
    if 'D' in damage:
        pos1 = damage.find('D')
        if '+' in damage:
            pos2 = damage.find('+')
            output = random.randint(1,int(damage[pos1+1])) + int(damage[pos2+1])
        else:
            output = random.randint(1,int(damage[pos1+1]))
    else:
        output = int(damage)
    return output

def woundDice(hits,damage):
    return hits*damage

def saves(save,armorP,wounds):
    output = 0
    for i in range(0,wounds):
        if d6() >= save+abs(armorP):
            output += 1
    return output

def howmanyAttacks(Attacks):
    if 'D' in Attacks:
        output = random.randint(1,int(Attacks[Attacks.find('D')+1]))
    else:
        output = int(Attacks)
    return output

def indiMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, Units):
    AttacksTurn = howmanyAttacks(Attacks) * Units
    hits = rollHit(AttacksTurn, BallisticSkill)
    wounds = rollWound(hits, Strength, Toughness)
    damageInflicted = (wounds - saves(Save, ArmorP, wounds)) * damageMod(Damage)
    return damageInflicted

def totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units):
    damageList = []
    for i in range(0, iterations):
        AttacksTurn = howmanyAttacks(Attacks) * Units
        hits = rollHit(AttacksTurn, BallisticSkill)
        wounds = rollWound(hits, Strength, Toughness)
        damageInflicted = (wounds - saves(Save, ArmorP, wounds)) * damageMod(Damage)
        damageList.append(damageInflicted)
    average = np.mean(damageList)
    std_dev = np.std(damageList)
    return average, std_dev



def mainloop():
    Units = int(input('How many units: '))
    Attacks = input('How many attacks (can be dice roll): ')
    BallisticSkill = int(input('BallisticSkill: '))
    ArmorP = int(input('AP: '))
    Strength = int(input('Strength: '))
    Damage = str(input('Damage (can be string): '))


    iterations = 3000

    toughs = list(range(1, 15))
    saves = list(range(1, 7))

     # Create 2D arrays to store the average and standard deviation
    avg_matrix = np.zeros((len(toughs), len(saves)))
    std_matrix = np.zeros((len(toughs), len(saves)))

    # Perform calculations for each Toughness and Save combination
    for i, Toughness in enumerate(toughs):
        for j, Save in enumerate(saves):
            average, std_dev = totMath(Attacks, BallisticSkill, Damage, Strength, Toughness, Save, ArmorP, iterations, Units)
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
    plt.title('Average Damage ± Standard Deviation Heatmap')
    plt.show()


mainloop()