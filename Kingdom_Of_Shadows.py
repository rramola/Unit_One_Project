import os
import random
import time
from dataclasses import dataclass

from colorama import Back, Fore


@dataclass
class Inventory:
    lesserHealing: int
    greaterHealing: int
    lesserMana: int
    greaterMana: int
    lesserStamina: int
    greaterStamina: int
    lesserDamage: int
    greaterDamage: int
    lesserDefense: int
    greaterDefense: int


@dataclass
class Character:
    health: int
    mana: int
    stamina: int
    defense: int
    weapon: str
    inventory: Inventory
    currency: int


@dataclass
class Potion:
    name: str
    type: str
    amount: int
    price: int
    quantity: int


@dataclass
class Shop:
    def __init__(self):
        self.potions = []

    def add_potion(self, potion: Potion):
        self.potions.append(potion)

    def get_potions(self):
        return self.potions


@dataclass
class Enemies:
    enemy_type: str
    weakness: str
    resistance: str
    health: int
    attack: int
    description: str


@dataclass
class Battle:
    player: Character
    enemy_type: Enemies
    defending: bool
    smallstrength: int
    largestrength: int
    strengthturns: int
    defenseturns: int
    smalldefense: int
    largedefense: int
    escaped: bool


def createCharacter(characterChoice: str, myCharacter: Character) -> Character:
    starterInventory = Inventory(1, 0, 1, 0, 1, 0, 1, 0, 1, 0)

    if characterChoice == "knight":
        myCharacter = Character(100, 70, 50, 100, "Sword", starterInventory, 100)
    elif characterChoice == "battle mage":
        myCharacter = Character(100, 100, 70, 50, "Staff", starterInventory, 100)
    elif characterChoice == "archer":
        myCharacter = Character(100, 50, 100, 70, "Bow", starterInventory, 100)
    elif characterChoice == "assassin":
        myCharacter = Character(100, 70, 100, 50, "Dagger", starterInventory, 100)
    spawnedChar = myCharacter
    return spawnedChar


def stanceChanger(boss: Enemies) -> None:
    if boss.weakness == "Magic":
        boss.resistance = "Magic"
        boss.weakness = "Physical"
        print(f"{boss.enemy_type} digs its feet into the ground")
    elif boss.weakness == "Physical":
        boss.resistance = "Physical"
        boss.weakness = "Ranged"
        print(f"{boss.enemy_type} lifts up into the air")
    elif boss.weakness == "Ranged":
        boss.resistance = "Ranged"
        boss.weakness = "Magic"
        print(f"{boss.enemy_type} puffs up its chest")


def enemyRandomizer(area: str) -> Enemies:
    troll = Enemies("Troll", "Physical", "Magic", 40, 15, "A simple forest troll")
    ogre = Enemies(
        "Ogre",
        "Physical",
        "Magic",
        60,
        30,
        "A giant ogre. It is carrying a wooden club.",
    )
    werewolf = Enemies(
        "Werewolf",
        "Physical",
        "Magic",
        35,
        25,
        "A werewolf. Its fangs are lightly stained with blood.",
    )
    giantBat = Enemies("Giant Bat", "Ranged", "Physical", 40, 15, "A giant flying bat!")
    witch = Enemies(
        "Witch",
        "Magic",
        "Ranged",
        45,
        20,
        "An old witch. Watch out for her powerful spells.",
    )
    demon = Enemies("Demon", "Physical", "Magic", 60, 25, "A tall fiery demon.")
    wingedimp = Enemies(
        "Winged Imp", "Ranged", "Physical", 45, 20, "A flying imp. It is very nimble."
    )
    gargoyle = Enemies(
        "Gargoyle",
        "Ranged",
        "Physical",
        70,
        35,
        "A giant flying imp-like creature. It's a gargoyle!",
    )
    darkmage = Enemies(
        "Dark Mage",
        "Magic",
        "Ranged",
        60,
        40,
        "A sorcerer very proficient in the Dark Arts.",
    )
    elemental = Enemies(
        "Elemental",
        "Magic",
        "Ranged",
        55,
        45,
        "A large being comprised purely of elemental energy.",
    )

    if area == "forest":
        EnemiesList = [troll, ogre, werewolf, giantBat, witch]
    else:
        EnemiesList = [demon, wingedimp, gargoyle, darkmage, elemental]

    enemy = EnemiesList[random.randint(0, 4)]
    return enemy


def playerTypeCheck(player: Character) -> str:
    if player.weapon == "Sword" or player.weapon == "Dagger":
        return "Physical"
    elif player.weapon == "Staff":
        return "Magic"
    else:
        return "Ranged"


def enemyDamageCalc(battle: Battle) -> float:
    enemydamage = random.randint(10, 20)
    enemydamage = (
        enemydamage + (battle.enemy_type.attack / 9) - (battle.player.defense / 10)
    )
    if battle.defending:
        enemydamage = enemydamage / 2

    return enemydamage


def statCutoffChecks(battle: Battle):
    if battle.player.health > 100:
        battle.player.health = 100
    if battle.player.weapon == "Sword":
        if battle.player.mana > 50:
            battle.player.mana = 50
        if battle.player.stamina > 70:
            battle.player.stamina = 70
        if battle.player.defense > 100 and battle.defenseturns == 0:
            battle.player.defense = 100
    elif battle.player.weapon == "Staff":
        if battle.player.mana > 100:
            battle.player.mana = 100
        if battle.player.stamina > 50:
            battle.player.stamina = 50
        if battle.player.defense > 70 and battle.defenseturns == 0:
            battle.player.defense = 70
    elif battle.player.weapon == "Bow":
        if battle.player.mana > 50:
            battle.player.mana = 50
        if battle.player.stamina > 100:
            battle.player.stamina = 100
        if battle.player.defense > 70 and battle.defenseturns == 0:
            battle.player.defense = 70
    elif battle.player.weapon == "Dagger":
        if battle.player.mana > 70:
            battle.player.mana = 70
        if battle.player.stamina > 100:
            battle.player.stamina = 100
        if battle.player.defense > 50 and battle.defenseturns == 0:
            battle.player.defense = 50


def playerDamageCalc(battle: Battle, choice: str, choice2: str):
    playerType = playerTypeCheck(battle.player)
    PhysicalBuff = False
    MagicBuff = False
    RangedBuff = False
    choice = choice.title()

    if playerType == "Physical":
        PhysicalBuff = True
    elif playerType == "Magic":
        MagicBuff = True
    elif playerType == "Ranged":
        RangedBuff = True
    if choice2 == "heavy":
        damage = random.randint(15, 20)
    else:
        damage = random.randint(5, 10)

    if choice == battle.enemy_type.weakness:
        damage *= 1.5
    elif choice == battle.enemy_type.resistance:
        damage *= 0.8

    if (
        choice == "Physical"
        and PhysicalBuff
        or choice == "Magic"
        and MagicBuff
        or choice == "Ranged"
        and RangedBuff
    ):
        damage *= 1.2

    if battle.largestrength:
        damage *= 1.5
    elif battle.smallstrength:
        damage *= 1.2

    return damage


def battleFunction(battle: Battle, enemy: Enemies) -> bool:
    Health = False
    Defense = False
    Mana = False
    Damage = False
    Stamina = False
    stanceTurns = 5
    battle.escaped = False

    battle.enemy_type = enemy

    while battle.player.health > 0 and battle.enemy_type.health > 0:
        turn = True
        hasMana = True
        hasStamina = True
        battle.defending = False

        if battle.defenseturns > 0:
            print(f"Defense potion active for {battle.defenseturns} turns")
            battle.defenseturns -= 1
        elif battle.defenseturns == 0:
            battle.largedefense = 0
            battle.smalldefense = 0
            statCutoffChecks(battle)

        if battle.strengthturns > 0:
            print(f"Strength potion active for {battle.strengthturns} turns")
            battle.strengthturns -= 1
        elif battle.strengthturns == 0:
            battle.largestrength = 0
            battle.smallstrength = 0

        print(
            f"""\nCurrent enemy: {battle.enemy_type.enemy_type}
Enemy HP: {battle.enemy_type.health}



HP: {battle.player.health}
Mana: {battle.player.mana}
Stamina: {battle.player.stamina}
"""
        )

        while turn:
            choice2 = ""
            choice = (
                input(
                    """What would you like to do?
[  ATTACK  ]
[  SPELLS  ]
[   ITEM   ]
[  ACTION  ]
> """
                )
                .lower()
                .strip()
            )
            if choice == "attack":
                choice = (
                    input(
                        """Which type of attack will you use?
[ PHYSICAL ]
[  RANGED  ]
[   BACK   ]
> """
                    )
                    .lower()
                    .strip()
                )
                if choice == "physical" or choice == "ranged":
                    choice = choice.title()
                    choice2 = (
                        input(
                            """What level?
[  HEAVY  ]  - 15 Stamina
[  LIGHT  ]  - 5 Stamina
[  BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if choice2 == "heavy":
                        if battle.player.stamina >= 15:
                            battle.player.stamina -= 15
                            turn = False
                        else:
                            print("You don't have enough stamina for that!")
                            hasStamina = False

                    elif choice2 == "light":
                        if battle.player.stamina >= 5:
                            battle.player.stamina -= 5
                            turn = False
                        else:
                            print("You don't have enough stamina for that!")
                            hasStamina = False

            elif choice == "spells":
                choice = "Magic"
                choice2 = (
                    input(
                        """What level?
[  HEAVY  ]  - 15 Mana
[  LIGHT  ]  - 5 Mana
[  BACK   ]
> """
                    )
                    .lower()
                    .strip()
                )
                if choice2 == "heavy":
                    if battle.player.mana >= 15:
                        battle.player.mana -= 15
                        turn = False
                    else:
                        print("You don't have enough mana for that!")
                        hasMana = False
                elif choice2 == "light":
                    if battle.player.mana >= 5:
                        battle.player.mana -= 5
                        turn = False
                    else:
                        print("You don't have enough mana for that!")
                        hasMana = False
                else:
                    pass

            elif choice == "item":
                print("Which item would you like to use?")

                if (
                    battle.player.inventory.lesserHealing > 0
                    or battle.player.inventory.greaterHealing > 0
                ):
                    print("[  HEALTH  ]")
                    Health = True
                if (
                    battle.player.inventory.lesserMana > 0
                    or battle.player.inventory.greaterMana > 0
                ):
                    print("[   MANA   ]")
                    Mana = True
                if (
                    battle.player.inventory.lesserStamina > 0
                    or battle.player.inventory.greaterStamina > 0
                ):
                    print("[  STAMINA ]")
                    Stamina = True
                if (
                    battle.player.inventory.lesserDamage > 0
                    or battle.player.inventory.greaterDamage > 0
                ):
                    print("[  DAMAGE  ]")
                    Damage = True
                if (
                    battle.player.inventory.lesserDefense > 0
                    or battle.player.inventory.greaterDefense > 0
                ):
                    print("[  DEFENSE ]")
                    Defense = True
                choice2 = (
                    input(
                        """[   BACK   ]
> """
                    )
                    .lower()
                    .strip()
                )
                if choice2 == "health" and Health:
                    if battle.player.inventory.greaterHealing > 0:
                        print("[  GREATER ]")
                    if battle.player.inventory.lesserHealing > 0:
                        print("[  LESSER  ]")
                    choice3 = (
                        input(
                            """[   BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if (
                        choice3 == "greater"
                        and battle.player.inventory.greaterHealing > 0
                    ):
                        battle.player.inventory.greaterHealing -= 1
                        battle.player.health += 50
                        turn = False
                    elif (
                        choice3 == "lesser"
                        and battle.player.inventory.lesserHealing > 0
                    ):
                        battle.player.inventory.lesserHealing -= 1
                        battle.player.health += 20
                        turn = False
                    if (
                        battle.player.inventory.greaterHealing == 0
                        and battle.player.inventory.lesserHealing == 0
                    ):
                        Health = False
                elif choice2 == "mana" and Mana:
                    if battle.player.inventory.greaterMana > 0:
                        print("[  GREATER ]")
                    if battle.player.inventory.lesserMana > 0:
                        print("[  LESSER  ]")
                    choice3 = (
                        input(
                            """[   BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if choice3 == "greater" and battle.player.inventory.greaterMana > 0:
                        battle.player.inventory.greaterMana -= 1
                        battle.player.mana += 50
                        turn = False
                    elif choice3 == "lesser" and battle.player.inventory.lesserMana > 0:
                        battle.player.inventory.lesserMana -= 1
                        battle.player.mana += 20
                        turn = False
                    if (
                        battle.player.inventory.greaterMana == 0
                        and battle.player.inventory.lesserMana == 0
                    ):
                        Mana = False
                elif choice2 == "stamina" and Stamina:
                    if battle.player.inventory.greaterStamina > 0:
                        print("[  GREATER ]")
                    if battle.player.inventory.lesserStamina > 0:
                        print("[  LESSER  ]")
                    choice3 = (
                        input(
                            """[   BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if (
                        choice3 == "greater"
                        and battle.player.inventory.greaterStamina > 0
                    ):
                        battle.player.inventory.greaterStamina -= 1
                        battle.player.stamina += 50
                        turn = False
                    elif (
                        choice3 == "lesser"
                        and battle.player.inventory.lesserStamina > 0
                    ):
                        battle.player.inventory.lesserStamina -= 1
                        battle.player.stamina += 20
                        turn = False
                    if (
                        battle.player.inventory.greaterStamina == 0
                        and battle.player.inventory.lesserStamina == 0
                    ):
                        Stamina = False
                elif choice2 == "damage" and Damage:
                    if battle.player.inventory.greaterDamage > 0:
                        print("[  GREATER ]")
                    if battle.player.inventory.lesserDamage > 0:
                        print("[  LESSER  ]")
                    choice3 = (
                        input(
                            """[   BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if (
                        choice3 == "greater"
                        and battle.player.inventory.greaterDamage > 0
                    ):
                        battle.player.inventory.greaterDamage -= 1
                        battle.largestrength += 1
                        battle.strengthturns = 5
                        turn = False
                    elif (
                        choice3 == "lesser" and battle.player.inventory.lesserDamage > 0
                    ):
                        battle.player.inventory.lesserDamage -= 1
                        battle.smallstrength += 1
                        battle.strengthturns = 5
                        turn = False
                    if (
                        battle.player.inventory.greaterDamage == 0
                        and battle.player.inventory.lesserDamage == 0
                    ):
                        Damage = False
                elif choice2 == "defense" and Defense:
                    if battle.player.inventory.greaterDefense > 0:
                        print("[  GREATER ]")
                    if battle.player.inventory.lesserDefense > 0:
                        print("[  LESSER  ]")
                    choice3 = (
                        input(
                            """[   BACK   ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if (
                        choice3 == "greater"
                        and battle.player.inventory.greaterDefense > 0
                    ):
                        battle.player.inventory.greaterDefense -= 1
                        battle.player.defense += 50
                        battle.largestrength += 1
                        battle.strengthturns = 5
                        turn = False
                    elif (
                        choice3 == "lesser"
                        and battle.player.inventory.lesserDefense > 0
                    ):
                        battle.player.inventory.lesserDefense -= 1
                        battle.player.defense += 20
                        battle.smalldefense += 1
                        battle.defenseturns = 5
                        turn = False
                    if (
                        battle.player.inventory.greaterDefense == 0
                        and battle.player.inventory.lesserDefense == 0
                    ):
                        Defense = False

            elif choice == "action":
                choice2 = (
                    input(
                        f"""Which action would you like to take?
[  ESCAPE  ] - Flee from battle
[  INSPECT ] - Inspect the enemy
[  DEFEND  ] - 1/2 damage for next attack
[   REST   ] - Replinish some of your {"Mana" if battle.player.weapon == "Staff" else "Stamina"}
[   BACK   ]
> """
                    )
                    .lower()
                    .strip()
                )
                if choice2 == "escape" and battle.enemy_type.enemy_type != "Kryos":
                    escapechance = random.randint(1, 100)
                    if escapechance <= 65:
                        print("\nYou got away safely.\n")
                        input("[Press Enter to Continue]")
                        os.system("clear")
                        battle.escaped = True
                        return False
                    else:
                        print("\nCould not get away.")
                    turn = False

                elif choice2 == "inspect":
                    print(
                        f"""
{battle.enemy_type.description}

Weak to: {battle.enemy_type.weakness}

Strong against: {battle.enemy_type.resistance}"""
                    )

                elif choice2 == "defend":
                    battle.defending = True
                    turn = False

                elif choice2 == "rest":
                    if battle.player.weapon == "Staff":
                        battle.player.mana += 30
                    else:
                        battle.player.stamina += 30
                    statCutoffChecks(battle)
                    print(
                        "You took a brief rest, recovering 30 "
                        + ("Mana" if battle.player.weapon == "Staff" else "Stamina")
                    )
                    turn = False

            else:
                print("Please choose a valid action!")

            if not hasMana or not hasStamina:
                pass
            elif choice2 == "heavy" or choice2 == "light":
                damage = playerDamageCalc(battle, choice, choice2)

                critchance = random.randint(1, 10)
                if battle.player.weapon == "Dagger":
                    critchance = random.randint(1, 5)

                if critchance == 5:
                    damage *= 1.5
                    print(Fore.RED + "\n*CRITICAL HIT*" + Fore.RESET)
                    time.sleep(1)
                damage = round(damage)
                print(Fore.GREEN + f"\n{damage} HP dealt" + Fore.RESET)
                battle.enemy_type.health -= damage
                time.sleep(1)

        if battle.enemy_type.health > 0:
            if battle.enemy_type.enemy_type != "Kryos":
                print(f"\nEnemy {battle.enemy_type.enemy_type} attacks\n")
                time.sleep(1)

                if battle.enemy_type.weakness == "Magic":
                    print(
                        f"Enemy {battle.enemy_type.enemy_type} struck you with a bolt of lightning"
                    )
                elif battle.enemy_type.weakness == "Ranged":
                    print(f"Enemy {battle.enemy_type.enemy_type} swooped down at you")
                elif battle.enemy_type.weakness == "Physical":
                    print(f"Enemy {battle.enemy_type.enemy_type} swung at you")
                time.sleep(1)

                enemydamage = enemyDamageCalc(battle)

                chance = random.randint(1, 100)
                if battle.player.weapon == "Dagger":
                    chance /= 3

                if chance <= 10:
                    print("\n... but it completely missed")
                    enemydamage = 0
                enemydamage = round(enemydamage)
                print(Fore.RED + f"\n{enemydamage} HP lost" + Fore.RESET)
                battle.player.health -= enemydamage
                if battle.player.health < 0:
                    battle.player.health = 0

            else:
                stanceTurns -= 1
                if stanceTurns == 0:
                    stanceChanger(battle.enemy_type)
                    stanceTurns = 5
                else:
                    if battle.enemy_type.weakness == "Magic":
                        print(f"\n{battle.enemy_type.enemy_type} blasts you with fire")
                    elif battle.enemy_type.weakness == "Ranged":
                        print(f"\n{battle.enemy_type.enemy_type} flies at you")
                    elif battle.enemy_type.weakness == "Physical":
                        print(
                            f"\n{battle.enemy_type.enemy_type} slices at you with its claws"
                        )
                    time.sleep(1)

                    enemydamage = enemyDamageCalc(battle)

                    chance = random.randint(1, 100)
                    if battle.player.weapon == "Dagger":
                        chance /= 3

                    if chance <= 10:
                        print("\n... but it completely missed")
                        enemydamage = 0
                    enemydamage = round(enemydamage)
                    print(Fore.RED + f"\n{enemydamage} HP lost" + Fore.RESET)
                    battle.player.health -= enemydamage
                    if battle.player.health < 0:
                        battle.player.health = 0

        if battle.enemy_type.health <= 0:
            if battle.enemy_type.enemy_type != "Kryos":
                print(f"\n{battle.enemy_type.enemy_type} has been defeated")
                time.sleep(1)
                gold = random.randint(30, 60)
                print(f"\nyou got {gold} gold")
                time.sleep(1)
                battle.player.currency += gold
                input("[Press Enter to Continue]")
                os.system("clear")
                return False
            else:
                print(
                    f"\nThe great dragon, {battle.enemy_type.enemy_type}, has been slain by your hands."
                )
                time.sleep(1)
                print(
                    "\nThe kingdom can rest easy knowing that you have freed their lands from its torment."
                )
                time.sleep(1)
                print("\nYOU WIN")
                return True

        if battle.player.health <= 0:
            print("\nUnfortunately, your wounds have become too much to handle")
            time.sleep(1)
            print("\nYou have died")
            return True
    return not battle.player.health > 0


def battleDialogueRandomizer(area, enemy: Enemies) -> str:
    randomNumber = random.randint(1, 7)
    dialogue = ""
    # Forest dialogue
    if area == "forest":
        if randomNumber == 1:
            dialogue = f"""
Birds scatter as you advance through the gloomy forest, the sound of footsteps surround you as you proceed.

{enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 2:
            dialogue = f"""
The trampled sound of limbs surrounds you as you approach this shadowy figure ahead. 

{enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 3:
            dialogue = f"""
The nearing wildlife disperse the area in a panic,

{enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 4:
            dialogue = f"""
The rustling of leaves and snapping of twigs alert you to the presence of danger.

You turn around to face a {enemy.enemy_type} staring at you with unblinking eyes.
What do you do?\n"""
        if randomNumber == 5:
            dialogue = f"""
The sound of a twig snapping echoes through the forest, and you freeze in your tracks.

You can feel your heart pounding in your chest as you realize that a {enemy.enemy_type} is lurking nearby.
What’s your next move?\n"""
        if randomNumber == 6:
            dialogue = f"""
The hairs on the back of your neck stand up as you hear the unmistakable sound of footsteps behind you.

You turn around to face a {enemy.enemy_type} emerging from the shadows.
What’s your plan of action?\n"""
        if randomNumber == 7:
            dialogue = f"""
The eerie silence of the forest is suddenly broken by the sound of flapping wings as birds scatter in all directions.

You look around, and your eyes lock with those of a {enemy.enemy_type}.
What do you do next?\n"""
            # Abyss dialogue
    elif area == "abyss":
        if randomNumber == 1:
            dialogue = f"""
Flames encase the ground around you, the smell of burning flesh engulfs your senses. 

From the darkness, {enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 2:
            dialogue = f"""
Screeching noises and screams loom in the distance, you continue along this path. 

{enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 3:
            dialogue = f"""
Scattered ashes swarm the air around you, as the path ahead of you clears. 

{enemy.enemy_type} approaches you, what will you do?\n"""
        if randomNumber == 4:
            dialogue = f"""
The heat is almost unbearable as you descend into the fiery abyss.

You can hear the sound of {enemy.enemy_type} approaching from behind.
What’s your next move?\n"""
        if randomNumber == 5:
            dialogue = f"""
The air is thick with smoke and ash as you make your way through the fiery abyss.

Suddenly, you hear the sound of {enemy.enemy_type} in the distance.
What do you do?\n"""
        if randomNumber == 6:
            dialogue = f"""
The ground beneath your feet is hot to the touch as you navigate through the fiery abyss.

You can sense that {enemy.enemy_type} is lurking nearby.
What’s your plan of action?\n"""
        if randomNumber == 7:
            dialogue = f"""
The flames dance around you as you venture deeper into the fiery abyss.

You can feel the heat emanating from {enemy.enemy_type} as it approaches you.
What will you do?\n"""

    return dialogue


def battleProgression(area) -> str:
    roll = random.randint(1, 4)
    battleProgressionDialogue = ""
    if area == "forest":
        if roll == 1:
            battleProgressionDialogue = """The scent of pine needles and damp earth fills your nostrils. The trees tower above you, their branches reaching out like fingers. You feel the welcoming essence of the forest, as well as the secrets it holds.\n"""
        elif roll == 2:
            battleProgressionDialogue = """The forest floor is covered in a thick layer of fallen leaves and pine needles. Shadowy figures fill the area, darting through every inch of the forest. Inhabitants of the forest appear weary of your presence, glowing eyes focused on your every move as you proceed through the forest.\n
"""
        elif roll == 3:
            battleProgressionDialogue = """The harmonious sound of birds chirping, fills the air as you proceed through the lush green forest. Nature consumes your every step as you embark upon your journey.\n"""

        elif roll == 4:
            battleProgressionDialogue = """Distant howls and pain-filled screeches swallow the air around you. Beautiful scenery tarnished with a dark undertone is the forest upon which you inspect.\n"""

    elif area == "abyss":
        if roll == 1:
            battleProgressionDialogue = """The heat is almost unbearable in the fiery abyss. The air is thick with smoke and ash, and the ground beneath your feet is hot to the touch. Flames dance around you, casting flickering shadows on the walls.\n"""

        elif roll == 2:
            battleProgressionDialogue = """As you make your way deeper into the abyss, you hear the roar of flames and the crackle of burning wood. The heat is intense, and sweat beads on your forehead. You see molten lava flowing in the distance, its orange glow illuminating the darkness.\n"""
        elif roll == 3:
            battleProgressionDialogue = """The ground trembles beneath your feet as you walk through the fiery abyss. You see demons lurking in the shadows, their eyes glowing red with malice. You hear their distant whispers, filling the air with darkness and pain.\n"""

        elif roll == 4:
            battleProgressionDialogue = """Faint glimpses of light appear from the flames of the fiery abyss, illuminating a path in a place riddled with darkness.\n"""

    return battleProgressionDialogue


def purchase_item(character: Character):
    purchasing = True
    while purchasing:
        purchase = input(
            "Choose a potion type to purchase: [Health], [Mana], [Stamina], [Damage], [Defense] or Go[Back]\n> "
        ).lower()
        if purchase not in ["health", "mana", "stamina", "damage", "defense", "back"]:
            print("Invalid input. Please choose a valid option.")
        elif purchase == "back":
            purchasing = False
        elif purchase == "health":
            health_choice = input("Lesser or Greater? ").lower()
            if health_choice == "lesser":
                if character.currency >= 10:
                    character.inventory.lesserHealing += 1
                    character.currency -= 10
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
            elif health_choice == "greater":
                if character.currency >= 30:
                    character.inventory.greaterHealing += 1
                    character.currency -= 30
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
        elif purchase == "mana":
            mana_choice = input("Lesser or Greater? ").lower()
            if mana_choice == "lesser":
                if character.currency >= 10:
                    character.inventory.lesserMana += 1
                    character.currency -= 10
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
            elif mana_choice == "greater":
                if character.currency >= 30:
                    character.inventory.greaterMana += 1
                    character.currency -= 30
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
        elif purchase == "stamina":
            stamina_choice = input("Lesser or Greater? ").lower()
            if stamina_choice == "lesser":
                if character.currency >= 10:
                    character.inventory.lesserStamina += 1
                    character.currency -= 10
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
            elif stamina_choice == "greater":
                if character.currency >= 30:
                    character.inventory.greaterStamina += 1
                    character.currency -= 30
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
        elif purchase == "damage":
            damage_choice = input("Lesser or Greater? ").lower()
            if damage_choice == "lesser":
                if character.currency >= 10:
                    character.inventory.lesserDamage += 1
                    character.currency -= 10
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
            elif damage_choice == "greater":
                if character.currency >= 30:
                    character.inventory.greaterDamage += 1
                    character.currency -= 30
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
        elif purchase == "defense":
            defense_choice = input("Lesser or Greater? ").lower()
            if defense_choice == "lesser":
                if character.currency >= 10:
                    character.inventory.lesserDefense += 1
                    character.currency -= 10
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")
            elif defense_choice == "greater":
                if character.currency >= 30:
                    character.inventory.greaterDefense += 1
                    character.currency -= 30
                    print(
                        f"Thank you for your purchase. You have {character.currency} gold remaining..."
                    )
                else:
                    print("You don't have enough gold to complete the purchase.")


def main():
    currentArea = ""
    dead = False
    abyssKey = False
    dungeonKey = False
    # Player creation
    invalidInput = True
    name = input("What is your name, warrior? ")
    while invalidInput:
        characterSelection = (
            input(
                """
Please select your character. [Knight], [Battle Mage], [Archer], [Assassin] 
> """
            )
            .lower()
            .strip()
        )
        if (
            characterSelection == "knight"
            or characterSelection == "battle mage"
            or characterSelection == "mage"
            or characterSelection == "archer"
            or characterSelection == "assassin"
        ):
            invalidInput = False
        else:
            dialogueRoll = random.randint(1, 3)
            if dialogueRoll == 1:
                print("That is not one of the characters...")
            elif dialogueRoll == 2:
                print("Sorry, we aren't adding that character until the sequel.")
            else:
                print("Sorry, but that character is DLC")

            if characterSelection == "mage":
                characterSelection = "battle mage"

    placeholderInv = Inventory(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    player = Character(0, 0, 0, 0, "blank", placeholderInv, 0)
    player = createCharacter(characterSelection, player)
    placeholderEnemy = Enemies("", "", "", 0, 0, "")
    BattleInfo = Battle(player, placeholderEnemy, False, 0, 0, 0, 0, 0, 0, False)

    # Create shop
    # Potions
    lesser_health_pot = Potion("Lesser Health Pot", "Health", 20, 10, 0)
    greater_health_pot = Potion("Greater Health Pot", "Health", 50, 30, 0)
    lesser_mana_pot = Potion("Lesser Mana Pot", "Mana", 20, 10, 0)
    greater_mana_pot = Potion("Greater Mana Pot", "Mana", 50, 30, 0)
    lesser_stamina_pot = Potion("Lesser Stamina Pot", "Stamina", 20, 10, 0)
    greater_stamina_pot = Potion("Greater Stamina Pot", "Stamina", 50, 30, 0)
    lesser_damage_pot = Potion("Lesser Damage Pot", "Damage", 20, 10, 0)
    greater_damage_pot = Potion("Greater Damage Pot", "Damage", 50, 30, 0)
    lesser_defense_pot = Potion("Lesser Defense Pot", "Defense", 20, 10, 0)
    greater_defense_pot = Potion("Greater Defense Pot", "Defense", 50, 30, 0)

    # Shop w/added Potions
    shop = Shop()
    shop.add_potion(lesser_health_pot)
    shop.add_potion(greater_health_pot)
    shop.add_potion(lesser_mana_pot)
    shop.add_potion(greater_mana_pot)
    shop.add_potion(lesser_stamina_pot)
    shop.add_potion(greater_stamina_pot)
    shop.add_potion(lesser_damage_pot)
    shop.add_potion(greater_damage_pot)
    shop.add_potion(lesser_defense_pot)
    shop.add_potion(greater_defense_pot)

    # run
    # run = False

    print(
        "\nThe Everest Kingdom has been experiencing constant turmoil from enemy factions surrounding the Kingdom.\n"
    )
    time.sleep(2)
    print(
        f"The lives of innocents are at risk, unless {name.capitalize()} takes initiative to demolish these gruesome foes.\n"
    )
    time.sleep(2)
    print(
        "King Glen Evans I has appointed you as Protector of the Land. The surrounding forest and distant abyss present grave danger that you have been tasked with defeating.\n"
    )
    time.sleep(2)
    print(
        "Stories of a ferocious dragon, destroying surrounding villages, are spreading through the Kingdom like wildfire.\n"
    )
    time.sleep(2)
    print(
        "Will you help the people of the Everest Kingdom defeat this dragon and bring peace to the realm?\n"
    )
    time.sleep(2)
    input("[Press Enter to Continue]")
    os.system("clear")

    while not dead:
        # Storyline begins
        selectedArea = False
        command = (
            input(
                """Enter the [Kingdom] - Explore the [Forest] - Travel to the [Abyss]
> """
            )
            .lower()
            .strip()
        )
        if command in ["kingdom", "forest", "abyss"]:
            if command != "abyss" or abyssKey:
                os.system("clear")
            selectedArea = True
        if command == "kingdom":
            inKingdom = True
            print(
                """King Glen Evans: \"The Everest Kingdom is delighted to have you in our presence!\" 

What would you like to do?"""
            )
            while inKingdom:
                command = (
                    input(
                        """Enter the [Shop] - Enter the [Dungeon] - [Rest] in town - [Back] to area select
> """
                    )
                    .lower()
                    .strip()
                )
                if command == "shop":
                    potions = shop.get_potions()
                    for potion in potions:
                        print(
                            f"{potion.name} ({potion.type} + {potion.amount}): {potion.price} gold"
                        )
                    purchase_item(player)

                elif command == "dungeon":
                    if not dungeonKey:
                        print("You need a key to enter the dragon's keep!")
                    else:
                        os.system("clear")
                        boss = Enemies(
                            "Kryos",
                            "Physical",
                            "Magic",
                            200,
                            100,
                            """It's a huge dragon. 
It seems to change its stance frequently...
Maybe I should change my approach as well?""",
                        )
                        print(
                            "As you enter the key to the dungeon, the door swings open violently."
                        )
                        time.sleep(2)
                        print(
                            "\nThe great dragon, Kryos, reveals itself before you. You must best it in combat in order to escape."
                        )
                        time.sleep(1)

                        dead = battleFunction(BattleInfo, boss)
                        inKingdom = False

                elif command == "rest":
                    print("You set up camp for the night")
                    while command != "sleep":
                        command = (
                            input(
                                """\nWould you like to use an [Item] or [Sleep]
> """
                            )
                            .lower()
                            .strip()
                        )
                        if command == "item":
                            Health = False
                            Mana = False
                            Stamina = False
                            print("Which item would you like to use?")

                            if (
                                BattleInfo.player.inventory.lesserHealing > 0
                                or BattleInfo.player.inventory.greaterHealing > 0
                            ):
                                print("[  HEALTH  ]")
                                Health = True
                            if (
                                BattleInfo.player.inventory.lesserMana > 0
                                or BattleInfo.player.inventory.greaterMana > 0
                            ):
                                print("[   MANA   ]")
                                Mana = True
                            if (
                                BattleInfo.player.inventory.lesserStamina > 0
                                or BattleInfo.player.inventory.greaterStamina > 0
                            ):
                                print("[  STAMINA ]")
                                Stamina = True
                            choice2 = (
                                input(
                                    """[   BACK   ]
> """
                                )
                                .lower()
                                .strip()
                            )
                            if choice2 == "health" and Health:
                                if BattleInfo.player.inventory.greaterHealing > 0:
                                    print("[  GREATER ]")
                                if BattleInfo.player.inventory.lesserHealing > 0:
                                    print("[  LESSER  ]")
                                choice3 = (
                                    input(
                                        """[   BACK   ]
> """
                                    )
                                    .lower()
                                    .strip()
                                )
                                if (
                                    choice3 == "greater"
                                    and BattleInfo.player.inventory.greaterHealing > 0
                                ):
                                    BattleInfo.player.inventory.greaterHealing -= 1
                                    BattleInfo.player.health += 50
                                elif (
                                    choice3 == "lesser"
                                    and BattleInfo.player.inventory.lesserHealing > 0
                                ):
                                    BattleInfo.player.inventory.lesserHealing -= 1
                                    BattleInfo.player.health += 20
                                if (
                                    BattleInfo.player.inventory.greaterHealing == 0
                                    and BattleInfo.player.inventory.lesserHealing == 0
                                ):
                                    Health = False
                            elif choice2 == "mana" and Mana:
                                if BattleInfo.player.inventory.greaterMana > 0:
                                    print("[  GREATER ]")
                                if BattleInfo.player.inventory.lesserMana > 0:
                                    print("[  LESSER  ]")
                                choice3 = (
                                    input(
                                        """[   BACK   ]
> """
                                    )
                                    .lower()
                                    .strip()
                                )
                                if (
                                    choice3 == "greater"
                                    and BattleInfo.player.inventory.greaterMana > 0
                                ):
                                    BattleInfo.player.inventory.greaterMana -= 1
                                    BattleInfo.player.mana += 50
                                elif (
                                    choice3 == "lesser"
                                    and BattleInfo.player.inventory.lesserMana > 0
                                ):
                                    BattleInfo.player.inventory.lesserMana -= 1
                                    BattleInfo.player.mana += 20
                                if (
                                    BattleInfo.player.inventory.greaterMana == 0
                                    and BattleInfo.player.inventory.lesserMana == 0
                                ):
                                    Mana = False
                            elif choice2 == "stamina" and Stamina:
                                if BattleInfo.player.inventory.greaterStamina > 0:
                                    print("[  GREATER ]")
                                if BattleInfo.player.inventory.lesserStamina > 0:
                                    print("[  LESSER  ]")
                                choice3 = (
                                    input(
                                        """[   BACK   ]
> """
                                    )
                                    .lower()
                                    .strip()
                                )
                                if (
                                    choice3 == "greater"
                                    and BattleInfo.player.inventory.greaterStamina > 0
                                ):
                                    BattleInfo.player.inventory.greaterStamina -= 1
                                    BattleInfo.player.stamina += 50
                                    turn = False
                                elif (
                                    choice3 == "lesser"
                                    and BattleInfo.player.inventory.lesserStamina > 0
                                ):
                                    BattleInfo.player.inventory.lesserStamina -= 1
                                    BattleInfo.player.stamina += 20
                            statCutoffChecks(BattleInfo)
                        elif command == "sleep":
                            print("\nYou slept through the night by the warm fire.")
                            print("\nYou woke up feeling well rested.")
                            BattleInfo.player.health += 10
                            if BattleInfo.player.health >= 100:
                                BattleInfo.player.health = 100
                        else:
                            print("Please enter a valid command.")

                elif command == "back":
                    inKingdom = False
                    os.system("clear")

                else:
                    print(
                        'King Glen Evans: "I apologize, but we have yet to develop that..."\n'
                    )

        # Forest battle area
        if command == "forest":
            forestBattle = True
            forestWinCounter = 0
            while forestBattle and not dead:
                currentArea = command
                spawnEnemy = enemyRandomizer(currentArea)
                print(battleProgression(currentArea))
                print(battleDialogueRandomizer(currentArea, spawnEnemy))
                invalidInput = True
                while invalidInput:
                    startBattle = (
                        input(
                            """[FIGHT]
[ RUN ]
> """
                        )
                        .lower()
                        .strip()
                    )
                    if startBattle == "fight" or startBattle == "run":
                        invalidInput = False
                    else:
                        print(
                            "I should not mess around right now, I do not want to get lost in this forest...\n"
                        )
                if startBattle == "fight":
                    dead = battleFunction(BattleInfo, spawnEnemy)
                    if not dead and not BattleInfo.escaped:
                        forestWinCounter += 1
                        if forestWinCounter == 3:
                            abyssKey = True
                            print(
                                "While traveling, you happened to stumble upon a key."
                            )
                            print(
                                '\nUpon further inspection, you notice the word "Abyss" engraved along it.\n'
                            )
                            invalidInput = True
                            while invalidInput:
                                leaveOrStay = (
                                    input(
                                        """Would you like to return to the kingdom or stay and battle?
[  STAY  ]
[ RETURN ]
> """
                                    )
                                    .lower()
                                    .strip()
                                )
                                print()
                                if leaveOrStay in ["stay", "return"]:
                                    invalidInput = False
                                if leaveOrStay == "stay":
                                    pass
                                elif leaveOrStay == "return":
                                    forestBattle = False
                                    os.system("clear")
                                else:
                                    print("I fear I do not know what that means..")
                    else:
                        continue
                elif startBattle == "run":
                    forestBattle = False

        # Abyss battle area
        elif command == "abyss":
            if not abyssKey:
                print("You cannot enter the abyss without a key!\n")
            else:
                abyssBattle = True
                abyssWinCounter = 0
                while abyssBattle and not dead:
                    currentArea = command
                    spawnEnemy = enemyRandomizer(currentArea)
                    print(battleProgression(currentArea))
                    print(battleDialogueRandomizer(currentArea, spawnEnemy))
                    invalidInput = True
                    while invalidInput:
                        startBattle = (
                            input(
                                """[FIGHT]
[ RUN ]
> """
                            )
                            .lower()
                            .strip()
                        )
                        if startBattle == "fight" or startBattle == "run":
                            invalidInput = False
                        else:
                            print(
                                "Now is not the time for that! This place is dangerous...\n"
                            )
                    if startBattle == "fight":
                        dead = battleFunction(BattleInfo, spawnEnemy)
                        if not dead and not BattleInfo.escaped:
                            abyssWinCounter += 1
                            if abyssWinCounter == 3:
                                dungeonKey = True
                                print("Along the way you spot a key on the ground.\n")
                                print(
                                    'Taking a closer look reveals the word "Dungeon" engraved on it.\n'
                                )
                                invalidInput = True
                                while invalidInput:
                                    leaveOrStay = (
                                        input(
                                            """Would you like to return to the kingdom or stay and battle?
[  STAY  ]
[ RETURN ]
> """
                                        )
                                        .lower()
                                        .strip()
                                    )
                                    if leaveOrStay in ["stay", "return"]:
                                        invalidInput = False
                                    if leaveOrStay == "stay":
                                        pass
                                    elif leaveOrStay == "return":
                                        abyssBattle = False
                                        os.system("clear")
                                    else:
                                        print("I fear I do not know what that means..")
                        else:
                            continue
                    elif startBattle == "run":
                        abyssBattle = False

        elif not selectedArea:
            print("I do not know where that is, sorry...\n")

        if dead:
            print("[GAME OVER]")
            continue


if __name__ == "__main__":
    main()
