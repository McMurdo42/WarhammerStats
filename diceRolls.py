import random
import matplotlib.pyplot as plt


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
        if d6() >= save-abs(armorP):
            output += 1
    return output

def howmanyAttacks(Attacks):
    if 'D' in Attacks:
        output = random.randint(1,int(Attacks[Attacks.find('D')+1]))
    else:
        output = int(Attacks)
    return output



def mainloop():
    Attacks = input('How many attacks (can be dice roll): ')
    BallisticSkill = int(input('BallisticSkill: '))
    ArmorP = int(input('AP: '))
    Save = int(input('SV: '))
    Strength = int(input('Strength: '))
    Toughness = int(input('Toughness: '))
    Damage = str(input('Damage (can be string): '))

    iterations = 30000
    damageList = []


    for i in range(0,iterations):
        AttacksTurn = howmanyAttacks(Attacks)
        hits = rollHit(AttacksTurn,BallisticSkill)
        hits = woundDice(hits,damageMod(Damage))
        wounds = rollWound(hits,Strength,Toughness)
        damageInflicted = saves(Save,ArmorP,wounds)
        damageList.append(damageInflicted)
    
    totalDamage = 0
    for i in range(0,iterations):
        totalDamage += damageList[i]
    
    average = totalDamage / iterations
    print(average)


mainloop()