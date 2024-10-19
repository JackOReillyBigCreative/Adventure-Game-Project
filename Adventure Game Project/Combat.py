from platform import win32_edition
import Wait
import ASCII
import Player
import random
import Weapons
from threading import Timer
import time
import Score

def print_slow(str):
    for letter in str:
        print(letter, end = ""),
        Wait.wait(random.uniform(0.1, 0.05))
    print("\n")
    #prints text letter-by-letter slowly


def print_fast(str):
    for letter in str:
        print(letter, end = ""),
        Wait.wait(random.uniform(0.0005, 0.0001))
    print("\n")
    #prints text letter-by-letter quickly


def print_very_fast(str):
    for letter in str:
        print(letter, end = ""),
        Wait.wait(random.uniform(0.000005, 0.000001))
    print("\n")
    #prints text letter-by-letter REALLY quickly


def death_screen():
    print_fast(ASCII.death_screen)
    exit()
    #Death screen


def attack_quicktime(timeout):
    global crit
    t = Timer(timeout, print, ["*"])
    print("PRESS ENTER AFTER THE SPECIFIED NUMBER OF SECONDS, BEFORE THE '*' "
          "APPEARS.")
    Wait.wait(2)
    t.start()
    start = time.time()
    prompt = f"PRESS ENTER AFTER {timeout} SECONDS. \n"
    answer = input(prompt)
    t.cancel()
    end = time.time()
    reaction_time = end - start
    boundry_1 = timeout - 0.25
    boundry_2 = timeout + 0.25
    if reaction_time > boundry_1 and reaction_time < boundry_2:
        crit = True
    else:
        crit = False

def standard_combat(target_name, target_health, target_damage,
                    enemy_range, enemy_healing_on_defeat):
    """
    Basic combat system
    """
    print_slow("THREAT DETECTED")
    print(f"{target_name} APPROACHES")
    print(f"{Player.name} ATTACKS FIRST")
    Wait.wait(1)
    combat_loop = True
    weapon_loop = True

    while combat_loop == True:
        #Puts you into a loop until you either lose or win
        print(f"{target_name} HAS {target_health} HP")
        Wait.wait(1)

        while weapon_loop == True:
            #puts you in a loop until you pick a valid weapon
            print(f"""WEAPON CHOICES:
1 - {Weapons.Revolver.Name} - {Weapons.Revolver.Info}
2 - {Weapons.Shotgun.Name} - {Weapons.Shotgun.Info}
3 - {Weapons.Chaingun.Name} - {Weapons.Chaingun.Info}""")
            weapon_choice = str(input("Choice: ")).lower()
            alt_fire = input("Use the alternate firing option? "
                             "(Yes/No): ").lower()

            if "y" in alt_fire:
                if "1" in weapon_choice:
                    target_health = target_health - \
                        int(Weapons.Revolver.Damage) * 2
                    Player.current_health = Player.current_health - 10
                    #If the weapon selected is equal to 1 AND the range
                    #is greater than or equal to the enemies range value,
                    #you attack
                    weapon_loop = False

                elif "2" in weapon_choice:
                    target_health = target_health - \
                        int(Weapons.Shotgun.Damage) * 1.5
                    Player.current_health = Player.current_health - 50
                    #If the weapon selected is equal to 2 you shoot an infinite range
                    #shotgun projectile and take 50 damage
                    weapon_loop = False
                elif "3" in weapon_choice:
                    print("CHAINGUN HAS NO ALT FIRE.")
                    Wait.wait(2)

            elif "n" in alt_fire:
                if "1" in weapon_choice and \
                enemy_range <= Weapons.Revolver.Range:
                    target_health = target_health - \
                        int(Weapons.Revolver.Damage)
                    #If the weapon selected is equal to 1 AND the range is
                    #greater than or equal to the enemies range value,
                    #you attack
                    weapon_loop = False

                elif "2" in weapon_choice and \
                   enemy_range <= Weapons.Shotgun.Range:
                    target_health = target_health - \
                        int(Weapons.Shotgun.Damage)
                    #If the weapon selected is equal to 2 AND the range
                    #is greater than or equal to the enemies range value,
                    #you attack
                    weapon_loop = False

                elif "3" in weapon_choice and \
                    enemy_range <= Weapons.Chaingun.Range \
                   and Weapons.chaingun_used == False:
                    target_health = target_health - \
                            int(Weapons.Chaingun.Damage)
                    #If the weapon selected is equal to 3 AND the range is
                    #greater than or equal to the enemies range value AND the
                    #chaingun is functional, you attack
                    print("CHAINGUN USED, IT CANNOT BE USED AGAIN "
                          "UNTIL REPAIRED")
                    print("\n")
                    Weapons.chaingun_used = True
                    weapon_loop = False

                elif "3" in weapon_choice and Weapons.chaingun_used == True:
                    print("THE CHAINGUN HAS ALREADY BEEN USED. "
                          "YOU CANNOT USE IT AGAIN UNTIL YOU REPAIR IT.")
                    print("\n")
                    #prevents the chaingun from being used if it has already
                    #been used previously

                else:
                    print("PLEASE CHOOSE A VALID WEAPON WITH A SUITABLE "
                          "RANGE. PICK THE NUMBER RELATED TO THE WEAPON.")
                    print("\n")
                    #In case the user enters a weapon that doesnt exist

            else:
                print("WEAPON HAS NO ALT FIRE/INVALID WEAPON")
                print("\n")
                Wait.wait(1)

        weapon_loop = True
        #sets weapon loop back to true so the next turn will work
        if Player.current_health <= 0:
            combat_loop = False
            print(f"{Player.name} HAS RAN OUT OF FUEL.")
            print("\n")
            Wait.wait(2)
            death_screen()
            Wait.wait(1)
            #Death :(

        elif target_health > 0:
            print(f"{target_name} HAS {target_health} HP")
            Wait.wait(1)
            #Tells the player how much health the enemy has
            print(f"{target_name} ATTACKS!")
            print("\n")
            Wait.wait(1)
            print(f"{target_name} HITS AND CAUSES {Player.name} TO LOSE "
                  f"{target_damage} FUEL.")
            Wait.wait(1)
            Player.current_health = Player.current_health - target_damage
            print(f"{Player.name} HAS {Player.current_health} FUEL "
                  "REMAINING.")
            Wait.wait(1)
            if Player.current_health <= 0:
                combat_loop = False
                print(f"{Player.name} HAS RAN OUT OF FUEL.")
                print("\n")
                Wait.wait(2)
                death_screen()
                Wait.wait(1)
                #Death :(

        elif target_health <= 0:
            print(f"{target_name} HAS DIED")
            print("\n")
            Wait.wait(2)
            Player.current_health = Player.current_health + \
                                    enemy_healing_on_defeat
            Player.HealthCheck()
            print(f"{Player.name} HAS {Player.current_health} "
                  "FUEL REMAINING.")
            Wait.wait(2)
            combat_loop = False
            print(f"{Player.name} WINS.")
            print("\n")
            Score.score_modify(200)
            Wait.wait(1)
            #Victory!!! combat ends and the player heals,
            #determined by the enemies healing factor.

        else:
            print("ERROR")
            exit()
            #debug message

win_condition = False
def hijacked_boss_fight(boss_name, boss_health):
    """
    Boss fight system
    """
    global boss_combat_loop
    global win_condition
    global loose_condition
    win_condition = False
    loose_condition = False
    defend = False
    dodge = False

    base_damage = 200
    boss_attacks = [f"{boss_name} prepares to use its REVOLVER!",
                    f"{boss_name} prepares to use its SHOTGUN!", 
                    f"{boss_name} prepares to use its CHAINGUN!",
                    f"{boss_name} prepares to use its ALT REVOLVER",
                    f"{boss_name} prepares to use its ALT SHOTGUN"]
    #Enemy bowing animation
    boss_combat_loop = True
    print_slow("PREPARE YOURSELF.")
    print("BOSS FIGHT MODE ACTIVE...")
    Wait.wait(1)
    print(f"{boss_name} APPROACHES")
    print(f"{Player.name} ATTACKS FIRST")
    Wait.wait(1)
    while boss_combat_loop:
        b_attack = boss_attacks[random.randint(0, 4)]
        print(b_attack)
        Wait.wait(1)
        print(r"""Actions:

ATTACK - Deal 200 base damage, 2x damage if you hit a critical hit.
DEFEND - Negate 75% of the damage from the incoming attack.
DODGE - Small chance of dodging the incoming attack, some attacks are easier to dodge than others.""")
#I cannot make raw text follow pep-8 without damaging how it looks in-game
        while True:
            #Keeps the player in a loop until they make a valid choice
            p_action = input("WHAT ACTION DO YOU PICK?: ").upper()
            if p_action == "ATTACK" or p_action == "DEFEND" or \
            p_action == "DODGE":
                break
            else:
                print("INVALID OPTION.")
                Wait.wait(1)
        defend = False
        dodge = False
        if p_action == "ATTACK":
            print("YOU ATTACK!")
            attack_quicktime(random.randint(3, 6))
            if crit == True:
                print("CRITICAL HIT!")
                boss_health -= base_damage * 2
                #If the player hits a crit they deal 2x damage.
            else:
                print("STANDARD HIT!")
                boss_health -= base_damage
            Wait.wait(1)
        elif p_action == "DEFEND":
            print("YOU PREPARE YOURSELF FOR THE INCOMING ATTACK!")
            defend = True
            #Defend option

        elif p_action == "DODGE":
            print("YOU PREPARE TO DODGE!")
            dodge = True
            #dodge option
        if boss_combat_loop == False:
            break
        
        if boss_health <= 0:
            win_condition = True
            print(f"{boss_name} WAS DEFEATED!")
            Score.score_modify(5000)
            Wait.wait(1)
            print_very_fast(ASCII.win_screen)
            Wait.wait(3)
            break
        #if the boss has 0 or lower hp the player wins
        else:
            pass

        print(f"{boss_name} READIES ITS ATTACK...")

        #Enemy turn
        #All the enemies attacks are very similar:
        #-They have different behaviour for each option
        #-Defending reduces damage for most attacks
        #-Dodging has a change to not take any damage
        #-If the player attacked the boss gets to attack normally.
 
        if "ALT" in b_attack:
            #If the "ALT" is in the attack flavour text then the
            #game will do one of the alt attacks
            if "REVOLVER" in b_attack:
                print(f"{boss_name} CHARGES UP ITS REVOLVER...")
                Wait.wait(1)
                if defend == False and dodge == False:
                    Player.b_current_health -= 300
                    print(f"{Player.name} TAKES 300 DAMAGE!")
                    Wait.wait(1)
                    #Alternate revolver attack
                elif defend == True:
                    print(f"DEFEND FAILED!")
                    Wait.wait(1)
                    Player.b_current_health -= 300
                    print(f"{Player.name} TAKES 300 DAMAGE!")
                    Wait.wait(1)
                    #You cannot defend from the alt revolver.
                elif dodge == True:
                    print(f"{Player.name} DODGED ALL INCOMING PROJECTILES!")
                    Wait.wait(1)
                    #You can always dodge the alt revolver
            elif "SHOTGUN" in b_attack:
                print(f"{boss_name}'S SHOTGUN FLOODS WITH HELL ENERGY!")
                Wait.wait(1)
                if defend == False and dodge == False:
                    Player.b_current_health -= 400
                    print(f"{Player.name} TAKES 400 DAMAGE!")
                    Wait.wait(1)
                    #Alternate shotgun attack
                elif defend == True:
                    Player.b_current_health -= 100
                    print(f"{Player.name} DEFENDS AND TAKES 100 DAMAGE!")
                    Wait.wait(1)
                    #Defend from damage
                elif dodge == True:
                    dodge_chance = random.randint(1, 4)
                    if dodge_chance == 1:
                        print(f"{Player.name} DODGED ALL INCOMING "
                              "PROJECTILES!")
                        Wait.wait(1)
                    else:
                        print("DODGE FAILED.")
                        Wait.wait(1)
                        Player.b_current_health -= 400
                        print(f"{Player.name} TAKES 400 DAMAGE!")
                        Wait.wait(1)
                    #Dodge from the alt shotgun
        else:
            if "REVOLVER" in b_attack:
                print(f"{boss_name} AIMS ITS REVOLVER AT YOU!")
                Wait.wait(1)
                if defend == False and dodge == False:
                    Player.b_current_health -= 100
                    print(f"{Player.name} TAKES 100 DAMAGE!")
                    Wait.wait(1)
                    #Revolver attack
                elif defend == True:
                    Player.b_current_health -= 25
                    print(f"{Player.name} DEFENDS AND TAKES 25 DAMAGE.")
                    Wait.wait(1)
                    #Defend from damage
                elif dodge == True:
                    dodge_chance = random.randint(0, 100)
                    if dodge_chance <= 75:
                        print(f"{Player.name} DODGED ALL INCOMING"
                              "PROJECTILES!")
                        Wait.wait(1)
                    else:
                        print(f"DODGE FAILED.")
                        Wait.wait(1)
                        Player.b_current_health -= 100
                        print(f"{Player.name} TAKES 100 DAMAGE!")
                        Wait.wait(1)
                    #75% chance of dodging incoming attack.

            elif "SHOTGUN" in b_attack:
                print(f"{boss_name} CHARGES TOWARDS YOU WITH ITS SHOTGUN!")
                Wait.wait(1)
                if defend == False and dodge == False:
                    Player.b_current_health -= 200
                    print(f"{Player.name} TAKES 200 DAMAGE!")
                    Wait.wait(1)
                    #Shotgun attack
                elif defend == True:
                    Player.b_current_health -= 50
                    print(f"{Player.name} DEFENDS AND TAKES 50 DAMAGE!")
                    Wait.wait(1)
                    #Defend from attack
                elif dodge == True:
                    dodge_chance = random.randint(1,3)
                    if dodge_chance == 1:
                        print(f"{Player.name} DODGED ALL INCOMING "
                              "PROJECTILES!")
                        Wait.wait(1)
                    else:
                        print("DODGE FAILED.")
                        Wait.wait(1)
                        Player.b_current_health -= 200
                        print(f"{Player.name} TAKES 200 DAMAGE!")
                        Wait.wait(1)
                    #Dodging system, 1 in 3 chance to dodge.
            elif "CHAINGUN" in b_attack:
                print(f"{boss_name} POINTS ITS CHAINGUN TOWARDS YOU!")
                Wait.wait(1)
                if defend == False and dodge == False:
                    Player.b_current_health -= 1000
                    print(f"{Player.name} TAKES 1000 DAMAGE!")
                    #Chaingun attack
                    Wait.wait(1)
                elif defend == True:
                    print(f"{Player.name} BLOCKS ALL INCOMING DAMAGE!")
                    #If the player blocks, the chaingun does zero damage.
                    Wait.wait(1)
                elif dodge == True:
                    print(f"{Player.name} DODGED ALL INCOMING PROJECTILES!")
                    #If the player dodges, the chaingun does zero damage.
                    Wait.wait(1)
        if Player.b_current_health <= 0:
            loose_condition = True
            break
        else:
            pass

        print(f"{Player.name} HAS {Player.b_current_health} FUEL LEFT.")
        Wait.wait(1)

        print(f"{boss_name} HAS {boss_health} HEALTH REMAINING.")
        print("\n")
        #prints how much health the player and boss has, and then loops
        #for another turn