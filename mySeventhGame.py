import json
from time import sleep
from random import randint
from atexit import register

class Narrator:

    def text_delay(self,text,delay=.0435):
        for letter in text:
            print(letter,end='')
            sleep(delay)

class Characters:

    def __init__(self,name,my_type,health,power,moves):
        self.name = name
        self.hp = health
        self.power = power
        self.defense = 0
        self.moves = moves
        self.copied_moves = []
        self.my_type = my_type
    
    def ability_used(self,ability):
        with open('ability_list.json','r') as f:
            enemy_moves = json.load(f)
            enemy_moves = enemy_moves[0]
            used = enemy_moves[self.my_type][ability.upper()]
            return (self.power * used) // 1

class Player(Characters):
    def __init__(self,username,password):
        self.hp = 0
        self.mp = 0
        self.gold = 50
        self.power = 0
        self.user = username
        self.pw = password
        self.mission = 0
        self.defense = 0
        self.name = self.user
        self.moves = []
        self.my_class = ''
        self.armor_dict = {
            'HELMET' : 'NONE',
            'CHEST' : 'NONE',
            'WEAPON' : 'NONE',
            'BOOTS' : 'NONE'
        }
        self.my_type = 'PLAYER'

    def level_up(self):
        narrator.text_delay("\nYou have leveled up!\n")
        self.power += 20
        self.hp += 30
        self.defense += 5
        self.gold += 25

    def add_armor(self,armor_name):
        with open('item_list.json','r') as f:
            items = json.load(f)
            if armor_name in player.armor_dict.values():
                narrator.text_delay("\nYou already have that item!\n")
                return
            if self.gold - items[0][armor_name]['GOLD'] >= 0:
                narrator.text_delay("\nYou have bought and equipped {}!\n".format(armor_name))
                a = self.armor_dict.copy()
                if 'HELMET' in armor_name:
                    a['HELMET'] = armor_name
                if 'CHEST' in armor_name:
                    a['CHEST'] = armor_name
                if 'WAND' in armor_name or 'STAFF' in armor_name or 'SWORD' in armor_name or 'KNIFE' in armor_name or 'STAR' in armor_name:
                    a['WEAPON'] = armor_name
                if 'BOOTS' in armor_name:
                    a['BOOTS'] = armor_name
                self.armor_dict.update(a)
                for obj in items:
                    if armor_name in obj.keys():
                        self.defense += obj[armor_name]['DEFENSE']
                        self.power += obj[armor_name]['POWER']
                        self.hp += obj[armor_name]['HEALTH']
                        self.mp += obj[armor_name]['MANA']
                        self.gold -= obj[armor_name]['GOLD']
                        
                narrator.text_delay("\nYour new gold count: {}\n".format(self.gold))        
            else:
                narrator.text_delay("\nYou do not have enough gold to buy that item!\n")

    def players_class(self,c):
        if c == 'warrior':
            self.hp = 125
            self.mp = 50
            self.power = 20
            self.defense = 15

        elif c == 'priest':
            self.hp = 110
            self.mp = 75
            self.power = 10
            self.defense = 5
        
        elif c == 'mage':
            self.hp = 100
            self.mp = 100
            self.power = 20
            self.defense = 3
        
        elif c == 'thief':
            self.hp = 115
            self.mp = 65
            self.power = 15
            self.defense = 7
        
        self.my_class = c


    def save_data(self):
        data = []
        with open('test1.json','r') as f:
            try:
                data = json.load(f)
            except:
                pass
            finally:
                with open('test1.json','w') as f:
                    players = {
                    'NAME':self.user,
                    'PASS':self.pw,
                    'HEALTH':self.hp,
                    'MANA':self.mp,
                    'GOLD':self.gold,
                    'POWER':self.power,
                    'MISSION':self.mission,
                    'DEFENSE':self.defense,
                    'MOVES' : self.moves,
                    'ARMOR' : self.armor_dict,
                    'CLASS' : self.my_class
                    }
                    
                    for obj in data:
                        if self.name in obj.values():
                            obj.update(players)
                        else:
                            data.append(players)
                            

                    if data == []:
                        data.append(players)
                    
                    json.dump(data,f,indent=2)

    def load_data(self):
        with open('test1.json','r') as f:
            data = json.load(f)
            for obj in data:
                if obj['NAME'] == self.name:
                    print("\n{}'s STATS:".format(self.name) + ' HEALTH : ' + str(obj['HEALTH']) + ',' + ' MANA : ' + str(obj['MANA']) + ',' + ' GOLD : ' + str(obj['GOLD']) + ',' + ' POWER : ' + str(obj['POWER']) + ',' + ' DEFENSE : ' + str(obj['DEFENSE']) + ',' + ' CLASS : ' + str(obj['CLASS']))
                    self.pw = obj['PASS']
                    self.hp = obj['HEALTH']
                    self.mp = obj['MANA']
                    self.gold = obj['GOLD']
                    self.power = obj['POWER']
                    self.mission = obj['MISSION']
                    self.defense = obj['DEFENSE']
                    self.moves = obj['MOVES']
                    self.my_class = obj['CLASS']
                    self.armor_dict = obj['ARMOR']
                    if obj['MISSION'] == 0:
                        character_creation()
                    elif obj['MISSION'] == 1:
                        first_mission()
                    elif obj['MISSION'] == 2:
                        second_mission()
                    elif obj['MISSION'] == 3:
                        third_mission()
                    elif obj['MISSION'] == 4:
                        fourth_mission()
                    elif obj['MISSION'] == 5:
                        fifth_mission()
                    break
                elif data[-1]['NAME'] != self.name:
                    narrator.text_delay("\nYour account has no saves in the database, starting new game....\n")
                    character_creation()

    def move_list(self):
        a = """
-----------------------------------------------------------------------------------
+                    Y  O  U  R      A  B  I  L  I  T  I  E  S                    +
-----------------------------------------------------------------------------------

                                   FORMAT
            ----------------------------------------------------
                 ability name: (ability damage, mana cost)

{}""".format(self.moves)
        return a

    def combat(self,enemy):
        with open("ability_list.json",'r') as f:
            data = json.load(f)
            for k,v in self.moves[0].items():
                v = [(v[0] * data[0]['PLAYER'][k.upper()]) // 1,v[1]]
                self.moves[0][k] = v
        global start_mp
        narrator.text_delay("\nYou have entered combat with '{}'!\n".format(enemy.name))
        start_mp = self.mp
        def combat_loop(enemy):
            while True:
                narrator.text_delay("\nIt's your turn! What ability would you like to use? If you would like to check your ability list, type in 'abilities'!",delay=0.0225)
                a = player_input(combat=True,foe=enemy)
                if a == 'player_dead':
                    return True
                elif a == 'enemy_dead':
                    return False
                else:
                    continue
        if combat_loop(enemy) == False:
            return True
        else:
            return False

def player_input(buy_item=False,sell_item=False,char_create=False,combat=False,foe=''):
    global global_commands
    global yes_commands
    global no_commands
    global_commands = ['inventory','items','character','help']
    binary_commands = ['yes','yeah','yep','yup','no','nope','nah']
    yes_commands = ['yes','yeah','yep','yup']
    no_commands = ['no','nope','nah']
    p_in = input("\n\n> ")
    p_in = p_in.lower()
    if p_in in global_commands[0:1]:
        player_inventory()
    elif p_in == 'character':
        player_character()
    elif p_in == 'help':
        narrator.text_delay("""\nAt anytime for the rest of the game, you may type in 'inventory' or 'items' to open up your inventory, and you may type 'character' in order to see what your character has equipped.

You may also type in 'help' to see the command list again.
""",0.025)

    if char_create == True:
        return p_in

    elif buy_item == True:
        return p_in.upper()

    elif combat == True:
        special_abilities = ['self heal','steal']
        global start_mp
        if p_in == 'abilities':
            print(player.move_list())
            sleep(.25)
        elif p_in in player.moves[0].keys():
            mana_cost = player.moves[0][p_in][1]
            ability_damage = player.moves[0][p_in][0]
            if start_mp - mana_cost >= 0:
                start_mp -= mana_cost
                narrator.text_delay("\nUsing ability....\n")
                sleep(.35)
                narrator.text_delay('\nYou used {}!\n'.format(p_in))
                if p_in not in special_abilities:
                    foe.hp -= ability_damage
                    if foe.hp < 0:
                        foe.hp = 0
                    narrator.text_delay("\n{}'s {} did {} damage, resulting in {}'s hp reducing to: {}!\n".format(player.name,p_in,ability_damage,foe.name,foe.hp))
                else:
                    if p_in == 'self heal':
                        start_hp = player.hp
                        player.hp += player.moves[0][p_in][0]
                        narrator.text_delay("\nYou have healed yourself for {}! Your new health is: {}\n".format(player.hp - start_hp,player.hp))
                    elif p_in == 'steal':
                        start_hp = player.hp
                        player.hp += player.moves[0][p_in][0]
                        foe.hp -= player.moves[0][p_in][0]
                        narrator.text_delay("\nYou have stolen {} health from {}! Your new health is: {}".format(player.hp - start_hp,foe.name,player.hp))

                narrator.text_delay("\nIt's {}'s turn! Lets wait and see what he decides to do...\n".format(foe.name))
                sleep(0.5)
                enemy_move_list = list(foe.moves[0].keys())
                enemy_move = randint(0,len(enemy_move_list) - 1)
                new_move_list = [*enemy_move_list]
                narrator.text_delay("\n{} used {}!\n".format(foe.name,new_move_list[enemy_move]))
                sleep(0.5)
                player.hp -= foe.ability_used(new_move_list[enemy_move])
                if player.hp <= 0:
                    player.hp = 0
                narrator.text_delay("\n{}'s {} did {} damage, resulting in {}'s hp reducing to: {}!\n".format(foe.name,new_move_list[enemy_move],foe.ability_used(new_move_list[enemy_move]),player.name,player.hp))

            else:
                narrator.text_delay("\nYou do not have enough mana for that ability!\n")
        else:
            narrator.text_delay("\nThat ability doesnt exist!\n")

        if player.hp <= 0:
            return 'player_dead'
        elif foe.hp <= 0:
            return 'enemy_dead'
        else:
            return True
                
    return p_in

def character_creation():
    class_list = ['warrior','priest', 'mage', 'thief']
    narrator.text_delay("\nWelcome to the character creation screen.\n")
    narrator.text_delay("\nCLASS OPTIONS\n")
    narrator.text_delay("------------------------")
    narrator.text_delay("\n[WARRIOR], [PRIEST], [MAGE], [THIEF]\n")
    narrator.text_delay("\nPlease select a class.")
    class_choice = player_input(char_create=True)
    while class_choice not in class_list:
        narrator.text_delay("\nThat is not a valid class! Please choice between [WARRIOR], [PRIEST], [MAGE], or [THIEF].")
        class_choice= player_input(char_create=True)
    if class_choice in class_list:
        if class_choice in class_list[0]:
            player.players_class('warrior')
            player.moves = [
                {
                    "light swing" : (player.ability_used('light swing'),0),
                    "guard break" : (player.ability_used('guard break'),15),
                    "heavy swing" : (player.ability_used('heavy swing'),30),
                }
            ]
        elif class_choice in class_list[1]:
            player.players_class('priest')
            player.moves = [
                {
                    "mana bolt" : (player.ability_used('mana bolt'),0),
                    "self heal" : (player.ability_used('self heal'),15),
                    "genesis" : (player.ability_used('genesis'),20),
                }
            ]
        elif class_choice in class_list[2]:
            player.players_class('mage')
            player.moves = [
                {
                    "energy bolt" : (player.ability_used('energy bolt'),0),
                    "ice blast" : (player.ability_used('ice blast'),15),
                    "fire storm" : (player.ability_used('fire storm'),50),
                }
            ]
        elif class_choice in class_list[3]:
            player.players_class('thief')
            player.moves = [
                {
                    "star shot" : (player.ability_used('star shot'),0),
                    "steal" : (player.ability_used('steal'),15),
                    "triple stab" : (player.ability_used('triple stab'),15),
                }
            ]
        narrator.text_delay("\nYou have selected '{}'! Good luck, {}, you'll need it...\n".format(class_choice.upper(),player.name))
        player.mission += 1
        first_mission()

def mysterious_man():
    hostage_man = Characters("Mysterious Man",'HUMANOID',50,20,[
            {
                'auto': 0,
                'punch' : 10,
                'shoot' : 20
            }
        ]
    )
    if player.combat(hostage_man) == True:
        narrator.text_delay("\nYou have survived combat with {}! As you run out of the cottage, you see a path that leads into the forest. Anything is better than where you just were, so you start following it...\n".format(hostage_man.name))
        player.mission += 1
        player.level_up()
        second_mission()
    else:
        narrator.text_delay("\nYou have died during combat with {}. You will be missed, {}.".format(hostage_man.name,player.name))
        player.__init__(player.user,player.pw)
        sleep(.75)

def player_died():
    narrator.text_delay("\nYou have died.",0.085)
    player.__init__(player.user,player.pw)
    sleep(.75)

def first_mission():
    narrator.text_delay("\nYou find yourself mysteriously waking up in an unfamiliar room while you hear knocking on the door...\n")
    narrator.text_delay("\nDo you wake up and open the door?")
    if player_input() in yes_commands:
        narrator.text_delay("\nAs you get up to open the door, you see a knife on the nightstand. Do you pick it up?")
        if player_input() in yes_commands:
            if player.power >= 5:
                narrator.text_delay("\nThe second you opened the door you stabbed the man and immediately start following a path away from the cottage.\n")
                player.mission += 1
                player.level_up()
                second_mission()
            else:
                narrator.text_delay("\nYou weren't strong enough to kill the mysterious man, and he shot you dead due to your hostility.")
        else:
            narrator.text_delay("\nAs you open the door he screams 'PUT YOUR HANDS UP NOW!'. Do you fight back?")
            if player_input() in yes_commands:
                mysterious_man()
                
            else:
                narrator.text_delay("\nYou put your hands up like the man asks, and he tells you to go to the balcony. Do you follow his instructions?")
                if player_input() in yes_commands:
                    narrator.text_delay("\nAs you walk to the balcony, you see a vase. Do you try to smash it on the mans head?")
                    if player_input() in yes_commands:
                        chance = randint(1,10)
                        if chance <= 5:
                            narrator.text_delay("\nYou were fast enough to smash the vase on his head, leaving him unconsious.\n")
                            narrator.text_delay("\nYou start running out of the house and start following a path into the woods. Anywhere is better than that cottage..")
                            player.mission += 1
                            player.level_up()
                            second_mission()
                        else:
                            narrator.text_delay("\nAs you were turning around to smash the vase on his head, he reacted quickly enough and shot you before you can hit him.\n")
                            player_died()
                    else:
                        narrator.text_delay("\nYou arrive at the balcony and the man instructs you to jump off. Do you follow his instructions?")
                        if player_input() in yes_commands:
                            narrator.text_delay("\nYou are completely suicidal and decide to jump off the balcony like an idiot.\n")
                            player_died()
                        else:
                            mysterious_man()
                else:
                    mysterious_man()
    else:
        narrator.text_delay("\nMAN: 'OPEN THE DOOR NOW OR I'LL OPEN IT MYSELF!'\n")
        narrator.text_delay("\nDo you follow his instructions and open the door?")
        if player_input() in yes_commands:
            narrator.text_delay("\nAs you open the door his bow and arrow is aimed at you and tells you to get on the ground.\n")
            narrator.text_delay("\nDo you do as he says?")
            if player_input() in yes_commands:
                narrator.text_delay("\nAs you go on the ground, he punches you in the face twice.\n")
                player.hp -= 20
                narrator.text_delay("\nYour new health: {}".format(player.hp))
                narrator.text_delay("\nThose punches really hurt... do you retaliate?")
                if player_input() in yes_commands:
                    mysterious_man()
                else:
                    narrator.text_delay("\nMAN: 'Hah, you really are a wussy. Get out of my game.\n'")
                    narrator.text_delay("\nThe man got upset that you were being a little girl and didnt fight him back, so he shot you dead. Nicely done.\n")
                    player_died()
            else:
                mysterious_man()
        else:
            narrator.text_delay("\nHe starts to pound the door and it seems to be loosening the door up.. Do you try to escape?")
            if player_input() in yes_commands:
                narrator.text_delay("\nYou get up and start searching the floor. You find a window. Do you break it and jump out?")
                if player_input() in yes_commands:
                    cut_hand = randint(1,10)
                    if cut_hand <= 5:
                        narrator.text_delay("\nWhile punching the window out, you hurt your hand.\n")
                        player.hp -= 10
                        narrator.text_delay("\nYour new health: {}".format(player.hp))
                    narrator.text_delay("\nYou were able to break the window and jump out.\n")
                    hurt_leg = randint(1,10)
                    if hurt_leg <= 5:
                        narrator.text_delay("\nWhile jumping out, you landed badly and hurt yourself.\n")
                        player.hp -= 20
                        narrator.text_delay("\nYour new health is: {}".format(player.hp))
                    narrator.text_delay("\nYou stabalize yourself and start to run on a random path that leads to the woods. Anywhere is better than that place..\n")
                    player.mission += 1
                    player.level_up()
                    second_mission()
                else:
                    narrator.text_delay("\nYou couldn't find anything useful to escape.\n")
                    narrator.text_delay("\nBOOM!\n",0.0675)
                    narrator.text_delay("\nYou turn around and see the man behind you, with his bow and arrow pointed straight at you.")
                    life_or_death = randint(1,25)
                    if life_or_death <= 5:
                        narrator.text_delay("\nThe man shot his arrow however you were quick enough to dodge it.\n")
                        mysterious_man()
                    else:
                        narrator.text_delay("\nThe man shot his arrow at you and it hit.\n")
                        player_died()
            else:
                narrator.text_delay("\nAs you sit there like an idiot not opening the door OR trying to escape, the man was able to barge into the room.\n")
                narrator.text_delay("\nMAN: 'You really just wanted to die, don't you? You suck at games, stick to something else...'\n")
                player_died()
            


def second_mission():
    narrator.text_delay("\nAfter a couple of hours of following the path, you see a village in the distance and approach it.\n")
    narrator.text_delay("\nVILLAGE GUARD: 'STOP! Where do you think you're going..?'\n")
    narrator.text_delay("\nI just escaped from a cottage southward, I don't remember much, however I think I may have been kidnapped..\n")
    narrator.text_delay("\nVILLAGE GUARD: 'The cottage southward...? You must mean 𝘩𝘪𝘮...\n")
    narrator.text_delay("\nI don't know who you're talking about, but he's dead now. He didn't know that I'm a {}.\n".format(player.my_class))
    narrator.text_delay("\nYou're a {}? Oh, please, do come into our village and help yourself to our services. As a thanks for taking care of him, here is +100 gold.\n".format(player.my_class))
    player.gold += 100
    items_for_sale = {
        "BASIC HELMET" : "+5 DEFENSE (50g)",
        "BASIC CHESTPLATE" : "+10 DEFENSE (75g)",
        "BASIC WEAPON" : "+15 POWER (100g)",
        "BASIC BOOTS" : "+3 DEFENSE (25g)",
    }
    class_items = items_for_sale
    if player.my_class == 'warrior':
        warrior_items = items_for_sale.copy()
        warrior_items['BASIC LONGSWORD'] = warrior_items.pop('BASIC WEAPON')
        warrior_items['BASIC LONGSWORD'] = '+10 POWER, +10 HEALTH (100g)'
        class_items = warrior_items
    elif player.my_class == 'priest':
        priest_items = items_for_sale.copy()
        priest_items['BASIC WAND'] = priest_items.pop('BASIC WEAPON')
        priest_items['BASIC WAND'] = '+10 POWER, +25 MANA (100g)'
        class_items = priest_items
    elif player.my_class == 'mage':
        mage_items = items_for_sale.copy()
        mage_items['BASIC STAFF'] = mage_items.pop('BASIC WEAPON')
        mage_items['BASIC STAFF'] = '+15 POWER (100g)'
        class_items = mage_items
    elif player.my_class == 'thief':
        thief_items = items_for_sale.copy()
        thief_items['BASIC KNIFE'] = thief_items.pop('BASIC WEAPON')
        thief_items['BASIC KNIFE'] = '+15 POWER (100g)'
        class_items = thief_items
    narrator.text_delay("\nAs you stroll through the village, a shop owner senses that you're an adventurer and tells you to come on over. Do you accept?")
    go_store = player_input()
    if go_store in yes_commands:
        narrator.text_delay("\nWelcome to my shop, {}. I can see that you're a {}. Check out what I have in stock for your class!\n\n".format(player.name,player.my_class))
        narrator.text_delay("\nWould you like to check out what he has?")
        buy = player_input()
        while buy in yes_commands:
            print('\n----------------------------------------------')
            for k,v in class_items.items():
                print(k, ':', v)
            print('----------------------------------------------')
            narrator.text_delay("\nWhat can I get for you {}?".format(player.name))
            item_choice = player_input(buy_item=True)
            if item_choice in list(class_items.keys()):
                player.add_armor(item_choice)
            else:
                narrator.text_delay("\nThat item does not exist!")
            narrator.text_delay("\nWould you like to buy another item?")
            buy = player_input()
        narrator.text_delay("\nGoodbye, adventurer, pleasure doing business with you.\n")
    else:
       narrator.text_delay("\nYour loss, adventurer... life won't be easy for long..\n")
    player.mission += 1
    player.level_up()
    third_mission()

def giganto_bear():
    bear = Characters("Giganto Bear",'ANIMAL',400,30,[
            {
                'bite': 0,
                'counter' : 10,
                'swipe' : 20
            }
        ]
    )
    if player.combat(bear) == True:
        narrator.text_delay("\nYou have survived combat with {}! After killing and eating the bear, you feel replenished and gain +20 hp.\n".format(bear.name))
        player.mission += 1
        player.hp += 20
        player.level_up()
        fourth_mission()
    else:
        narrator.text_delay("\nYou have died during combat with {}. You will be missed, {}.".format(bear.name,player.name))
        player.__init__(player.user,player.pw)
        sleep(.75)

def third_mission():
    narrator.text_delay('\nYou are aimlessly wandering through the woods, when you realize you find yourself hungry...\n')
    narrator.text_delay("\nYou then hear a disturbingly loud noise coming from your northwest. It sounds like an animal, you might be able to eat it... Do you run in the direction of the noise?")
    if player_input() in yes_commands:
        narrator.text_delay("\nAfter five minutes of sprinting, you find an ENORMOUS bear. You don't think you can kill it.. but you fear you may die of hunger if you don't attempt to eat it.\n")
        narrator.text_delay("\nDo you fight it?")
        if player_input() in yes_commands:
            giganto_bear()
        else:
            narrator.text_delay("\nYou have successfully ran away, however you're starving..\n")
            num_seconds = randint(1,10)
            narrator.text_delay("\nDue to your hunger, you will lose 20 health a second.\n")
            while player.hp != player.hp - (num_seconds * 10):
                player.hp -= 10
                if player.hp <= 0:
                    player.hp = 0
                narrator.text_delay("\nYour new health: {}\n".format(player.hp))
                sleep(1)
            if player.hp <= 0:
                player_died()
            else:
                narrator.text_delay("\nYou survived and were able to find a squirrel to eat.. but was it worth it?")
                player.mission += 1
                player.level_up()
                fourth_mission()
    else:
        narrator.text_delay("\nYou have successfully ran away, however you're starving..\n")
        num_seconds = randint(1,10)
        narrator.text_delay("\nDue to your hunger, you will lose 10 helth a second.\n")
        while player.hp != player.hp - (num_seconds * 10):
            player.hp -= 10
            if player.hp <= 0:
                player.hp = 0
            narrator.text_delay("\nYour new health: {}\n".format(player.hp))
            sleep(1)
        if player.hp <= 0:
            player_died()
        else:
            narrator.text_delay("\nYou survived and were able to find a squirrel to eat.. but was it worth it?")
            player.mission += 1
            player.level_up()
            fourth_mission()
def witch():
    witch = Characters("The Witch",'MYTHICAL',350,45,[
            {
                'LIFE DRAIN': 0,
                'DARK MATTER BOLT' : 10,
                'BLACK HOLE' : 20
            }
        ]
    )
    if player.combat(witch) == True:
        narrator.text_delay("\nYou have survived combat with {}! As you run out of the cottage, you see a path that leads into the forest. Anything is better than where you just were, so you start following it...\n".format(witch.name))
        player.mission += 1
        player.level_up()
        second_mission()
    else:
        narrator.text_delay("\nYou have died during combat with {}. You will be missed, {}.".format(witch.name,player.name))
        player.__init__(player.user,player.pw)
        sleep(.75)

def fourth_mission():
    narrator.text_delay("\nAs you find your way out of the woods, you see a huge village. Do you approach it?")
    b = player_input()
    if b in yes_commands:
        narrator.text_delay("\nYou start walking towards the village where you encounter a beggar asking for gold. Do you give her some?")
        if player_input() in yes_commands:
            give_beggar = randint(1,player.gold)
            narrator.text_delay("\nYou gave the beggar {} gold.\n".format(give_beggar))
            narrator.text_delay("\nBeggar: 'Thank you so much traveler.. May the Gods bless your soul..'\n")
            new_health = player.hp + 10 * (player.gold // 30)
            player.hp = new_health
            narrator.text_delay("\nDue to the beggars blessings, you have gained {} health! Kind deeds do not go unnoticed..\n".format(player.hp))
            player.mission += 1
            fifth_mission()
        else:
            narrator.text_delay("\nThe beggar reveals herself as a witch and curses you out for not giving her gold.\n")
            narrator.text_delay("\nOh no! It seems like the witches curses came true. You start to feel sick and lose -20 health.\n")
            if player.hp - 20 > 0:
                player.hp -= 20
                player.mission += 1
                fifth_mission()
            if player.hp >= 50:
                narrator.text_delay("\nThe witch is pissed at the fact that you survived,and is prepared to fight you.\n")
                witch()
            else:
                narrator.text_delay("\nYou are now below 50% hp and terrified of whats to come..\n")
                
    elif b in no_commands:
        narrator.text_delay("\nYou debated on whether or not to enter the village, but eventually decided not to... will this decision be your reckoning..?\n")
        narrator.text_delay("\nYou walk around the village and follow a path that leads from the village northward.\n")
        narrator.text_delay("\nAs you follow the path, you see a peddler coming towards you where he offers you some of his goods.\n")
        narrator.text_delay("\nDo you accept his offer?")
        if player_input() in yes_commands():
            items_for_sale = {
            "BASIC HELMET" : "+5 DEFENSE (50g)",
            "BASIC CHESTPLATE" : "+10 DEFENSE (75g)",
            "BASIC WEAPON" : "+15 POWER (100g)",
            "BASIC BOOTS" : "+3 DEFENSE (25g)",
            }
            class_items = items_for_sale
            if player.my_class == 'warrior':
                warrior_items = items_for_sale.copy()
                warrior_items['BRONZE LONGSWORD'] = warrior_items.pop('BASIC WEAPON')
                warrior_items['BRONZE LONGSWORD'] = '+20 POWER, +20 HEALTH (150g)'
                class_items = warrior_items
            elif player.my_class == 'priest':
                priest_items = items_for_sale.copy()
                priest_items['METAL WAND'] = priest_items.pop('BASIC WEAPON')
                priest_items['METAL WAND'] = '+20 POWER, +50 MANA (150g)'
                class_items = priest_items
            elif player.my_class == 'mage':
                mage_items = items_for_sale.copy()
                mage_items['WOODEN STAFF'] = mage_items.pop('BASIC WEAPON')
                mage_items['WOODEN STAFF'] = '+35 POWER (150g)'
                class_items = mage_items
            elif player.my_class == 'thief':
                thief_items = items_for_sale.copy()
                thief_items['BUTTERFLY KNIFE'] = thief_items.pop('BASIC WEAPON')
                thief_items['BUTTERFLY KNIFE'] = '+35 POWER (150g)'
                class_items = thief_items
            go_store = player_input()
            if go_store in yes_commands:
                narrator.text_delay("\nWelcome to my shop, {}. I can see that you're a {}. Check out what I have in stock for your class!\n\n".format(player.name,player.my_class))
                narrator.text_delay("\nWould you like to check out what he has?")
                buy = player_input()
                while buy in yes_commands:
                    print('\n----------------------------------------------')
                    for k,v in class_items.items():
                        print(k, ':', v)
                    print('----------------------------------------------')
                    narrator.text_delay("\nWhat can I get for you {}?".format(player.name))
                    item_choice = player_input(buy_item=True)
                    if item_choice in list(class_items.keys()):
                        player.add_armor(item_choice)
                    else:
                        narrator.text_delay("\nThat item does not exist!")
                    narrator.text_delay("\nWould you like to buy another item?")
                    buy = player_input()
                narrator.text_delay("\nGoodbye, adventurer, pleasure doing business with you.\n")
            else:
                narrator.text_delay("\nYour loss, adventurer... life won't be easy for long..\n")


def fifth_mission():
    narrator.text_delay("\nHello puss wusses\n")
def user_validator(user):
    data = []
    a = True
    try:
        with open('test1.json','r') as f:
            data = json.load(f)
            for obj in data:
                if user == obj["NAME"]:
                    a = False
    finally:
        return a

def pass_validator(user,password):
    data = []
    b = True
    try:
        with open('test1.json','r') as f:
            data = json.load(f)
            for obj in data:
                if password == obj['PASS'] and user == obj['NAME']:
                    b = False
    finally:
        return b

        

def exit_handler():
    player.save_data()
    sleep(.25)
    print("\nThanks for playing! Come again soon..")

def create_account():
    user_name = str(input("\nType in what you would like your username to be: "))
    if user_validator(user_name) == False:
        print('\nThat account already exists!')
        sleep(.25)
        create_account()
    else:
        global player
        pass_word = str(input("\nEnter a password: "))
        player = Player(user_name,pass_word)
        narrator.text_delay("\nSending you to character creation screen....\n")
        sleep(.35)
        character_creation()


def login():
    username = str(input("\nEnter the account you would like to login to: "))
    if user_validator(username) == False:
        narrator.text_delay("\nUser validation successful....\n")
        sleep(.25)
    else:
        narrator.text_delay("\nChecking data base for '{}'....\n".format(username))
        print("\nUsername does not exist. Try again.")
        login()
    password = str(input("\nEnter the password of that account: "))
    if pass_validator(username,password) == False:
        narrator.text_delay("\nPassword validation successful....\n")
        sleep(.25)
    else:
        print('\nIncorrect password, try to remember it and try again.')
        login()
    global player
    player = Player(username,password)
    player.load_data()


def main():
    global narrator
    run_once = False
    narrator = Narrator()
    narrator.text_delay("\nWELCOME TO NARNIA\n")
    narrator.text_delay("\nDo you already have an account?")
    create_login = player_input()
    if create_login in yes_commands:
        narrator.text_delay("\nDirecting you to login screen....\n")
        run_once = True
        sleep(.35)
        login()
    elif create_login in no_commands:
        narrator.text_delay("\nDirecting you to account creation screen....\n")
        run_once = True
        sleep(.35)
        create_account()
    else:
        narrator.text_delay("\nThat wasn't an option imbecile. Try again.\n")
        main()
    while run_once == True:
        register(exit_handler)
        break

if __name__ == "__main__":
    main()
    