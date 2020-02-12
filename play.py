from __future__ import print_function, division
import cmd
import textwrap
import sys
import os
import time
import string
import platform
import copy


from random import seed, randint, randrange, choice, sample
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
from termcolor import colored

from asciimatics.effects import Scroll, Mirage, Wipe, Cycle, Matrix, \
    BannerText, Stars, Print
from asciimatics.particles import DropScreen
from asciimatics.renderers import FigletText, SpeechBubble, Rainbow, Fire
from asciimatics.scene import Scene
from asciimatics.screen import Screen

import world
import character
import items

moveList = character.moveList
gameItems = items.gameItems
worldMap = world.worldMap
breedList = character.breedList
npcList = world.npcList
gameMonsters = character.gameMonsters


init(autoreset=True)


class COLORS:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Utility functions
screen_width = 79
text_wrapper = textwrap.TextWrapper(width=screen_width-4)
# works in IE6


def cls():
    operating_system = platform.system()
    if operating_system != 'Win64' and operating_system != 'Windows':
        os.system('clear')
    else:
        os.system('cls')


def anykey():
    input("Press enter key to continue")


def hr():
    print("="*20)


def speak(words, speed=0.01, wait=0.25):
    # typewriter like effect
    words = text_wrapper.fill(words)
    for character in words:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)
    print("\n")
    if(wait > 0):
        time.sleep(wait)


def centered(text):
    # prints centered text
    lines = textwrap.wrap(text, screen_width)
    final = "\n".join(line.center(screen_width) for line in lines)
    print(final)


def print_msg_box(content, title="", align="center", ret=False, width=screen_width, joinchar="\n", format=True):
    if(title != ""):
        title = (" "+COLORS.BOLD+title+COLORS.END+" ")

    title_len = len(title)
    leftover_space = (width+6)-title_len  # adding 6 for the BOLD

    tspacer = "-"*round(leftover_space/2)

    tl = "+"
    tc = title
    tr = "+"

    spacel = "|"
    spacec = " "*(width-2)
    spacer = "|"
    space = ("\n"+spacel+spacec+spacer+"\n")

    lines = textwrap.wrap(content, width-8)

    if(format != True):
        cc = content
    else:
        if(align == "center"):
            cc = joinchar.join(line.center(width-2) for line in lines)
        elif(align == "left"):
            cc = joinchar.join(textwrap.indent(line, "    ") for line in lines)

        elif(align == "none"):
            cc = content

    bl = "+"
    bc = "-"*(width-2)
    br = "+"

    box = (tl+tspacer+tc+tspacer+tr+space+cc+space+bl+bc+br)

    if(ret == True):
        return (box)
    else:
        print(box)

# Base Character Class


class Character:
    def __init__(self, name='', hp=0, fer=1, acr=1, cur=1, moves=[], **kwargs):
        self.name = name
        self.hp = hp
        self.max_hp = self.hp
        self.ferocity = fer  # str
        self.acrobatics = acr  # dex
        self.curiosity = cur  # luck
        self.moves = moves

    def attack(self, other, move):
        if(type(move) == str):
            move = character.moveList[move]
        attack_time = 1
        # for each time the move can hit (move.times)
        cls()
        time.sleep(1)
        for _ in range(0, move.times):
            move_desc = choice(move.verbs)
            speak(move_desc.format(self.name, other.name))  # describe attack
            # roll dice, add mods
            d20 = randint(1, 20)
            hit_mod = move.hit
            base_dmg = randint(move.dmg[0], move.dmg[1])
            dmg = 0  # holds the total dmg
            hit = d20+self.acrobatics+hit_mod  # THAC0
            target = 10+other.acrobatics  # AC
            # print("DEBUG: MOVE HIT:{} -- BASE_DMG:{}".format(hit_mod, base_dmg))
            # print("DEBUG: ATTACK #{} -- HIT ROLL: {}({}) -- TARGET AC: {} ".format(
            #     attack_time, hit, d20, target))
            attack_time += 1
            dmg_string = ""

            if(d20 == 20):
                # crit
                # do the max dmg of the move + ferociy
                dmg = self.ferocity+move.dmg[1]
                print("CRIT! Deals {} damage".format(dmg))
                print(colored(Style.BRIGHT+"CRITICAL HIT!", "red", "on_white"))
                dmg_string += "\n"
                dmg_string += "Deals {} damage!".format(dmg)
                other.hp -= dmg
            elif(hit >= target):
                # normal hit
                dmg = (base_dmg+self.ferocity) - other.acrobatics
                if(dmg < 0):
                    # dmg mitigated by armor?
                    dmg_string += "It barely hurts.\n"
                    dmg = randint(0, 1)
                #print("Deals {} damage".format(dmg))
                dmg_string += "Deals {} damage".format(dmg)
                other.hp -= dmg
            else:
                # miss
                # print(self.name + " missed!")
                dmg_string += "{} missed!".format(self.name)
            speak(dmg_string)
        time.sleep(0.5)
        cls()


class Enemy(Character):
    def __init__(self, hp=0, xp_given=1, drop=False, **kwargs):
        super().__init__(**kwargs)
        self.max_hp = hp
        self.hp = hp
        self.xp_given = xp_given
        self.drop = drop  # ["item", int(rate%)]


# Player Character
class Player(Character):
    def __init__(self, breed='', items=[], **kwargs):
        super().__init__(**kwargs)
        self.breed = breed
        self.location = "fyard1"
        self.attitude = None  # weapon slot
        self.hat = None  # armor slot
        self.level = 1
        self.xp = 0
        self.hp = 25
        self.max_hp = 25
        self.items = items
        self.kills = {}
        self.quest_monsters = []
        self.quest_items = []
        self.learned_moves = {
            2: moveList["slap"],
            4: moveList["doubleclaw"],
            6: moveList["pounce"],
        }

    def hp_max(self, SET_MAX=False):
        # make sure you dont go over max hp
        # or just set it to max
        if(self.hp > self.max_hp or SET_MAX):
            self.hp = self.max_hp

    def give_hp(self, hp):
        self.hp += hp
        self.hp_max()

    def required_xp(self):
        req = (self.level * 5)+self.level-1
        return req

    def give_quest(self, quest_type, quest_thing):
        if(quest_type == "monster"):
            self.quest_monsters.append(quest_thing)
            self.kills[quest_thing] = 0
        else:
            self.quest_items.append(quest_thing)

    def remove_quest(self, quest_type, quest_thing):
        if(quest_type == "monster"):
            print("removing monster: {}".format(quest_thing))
            self.quest_monsters.remove(quest_thing)
        else:
            self.quest_items.remove(quest_thing)

    def give_move(self, move):
        if(type(move) == str):
            move = moveList["move"]
        if(move not in self.moves):
            self.moves.append(move)
            print("You learned: {}".format(move.name))

    def remove_items(self, items):
        for item in items:
            self.items.remove(item)

    def give_items(self, items):
        for item in items:
            if(type(item) == str):
                item = gameItems[item]
            print("You got a {}".format(item.name))
            if(item.item_type == "hat" and item in self.items):
                print("You don't need two of those!")
            else:
                self.items.append(item)

    def equip(self, item=""):
        # handle a player trying to equip an item by typing the name
        if(item == ""):
            print("What are you trying to equip?")
            return
        print("DEBUG Current items:\n{}".format(self.list_items()))
        print("DEBUG Item name to equip:{} ".format(item))
        
        if(item not in list(gameItems.keys())):
            print("That's not an item!")
        elif(item not in self.items):
            print("You don't have that item")
        elif(item.item_type != "hat"):
            print("Hmm... How would a cat equip that?")
        else:
            item = gameItems[item]
            self.items.remove(item)
            if(self.hat != None):
                print("You remove your {} and put it back in your inventory.".format(
                    self.hat.name))
                self.items.append(self.hat)
            self.apply_item(item)
            print("You put on the {}".format(item.name))

    def apply_item(self, item):
        if(type(item) == str):
            item = gameItems[item]
        if(item.item_type == "hat"):
            old_item = self.hat
            self.hat = item
        elif(item.item_type == "attitude"):
            old_item = self.attitude
            self.attitude = item
        if(old_item != None):
            self.ferocity -= old_item.fer
            self.acrobatics -= old_item.acr
            self.curiosity -= old_item.cur
            self.max_hp -= old_item.max_hp
            if(old_item.move != False):
                self.moves.remove(moveList[old_item.move])
        self.ferocity += item.fer
        self.acrobatics += item.acr
        self.curiosity += item.cur
        self.max_hp += item.max_hp
        if(item.move != False):
            self.moves.append(moveList[item.move])

    def list_items(self):
        _items = ""
        numitems = {}
        for i in set(self.items):
            numitems[i.name] = self.items.count(i)
            _items += "{} x{}, ".format(i.name, self.items.count(i))
        # for i in list(numitems.keys):
            #_items += "{}({}), ".format(gameItems[i].name, numitems[i])
        return _items  # [:-2]

    # for battle screen input
    def list_attacks(self):
        _attacks = ""
        for i in range(len(self.moves)):
            _attacks += str(i+1) + ") " + self.moves[i].name + "\n"
        return _attacks

    def get_moves(self):
        _moves = ""
        for move in self.moves:
            _moves += move.name + ", "
        return _moves[:-2]

    def get_hat(self):
        if(self.hat == None):
            return "None"
        else:
            return self.hat.name

    def get_attitude(self):
        if(self.attitude == None):
            return "None"
        else:
            return self.attitude.name

    def clear_attitude(self):
        attitude = self.attitude
        self.attitude = None
        self.ferocity -= attitude.fer
        self.acrobatics -= attitude.fer
        self.curiosity -= attitude.cur
        self.max_hp -= attitude.max_hp
        self.hp_max()

    def show_status(self):
        cls()
        title = "{} the {}".format(self.name.capitalize(), self.breed)
        status = "    Level: {}\n".format(self.level)
        status += "    Attitude: {:12}\tHat: {:12}\n".format(
            self.get_attitude(), self.get_hat())
        status += "    HP: {}/{}\tXP: {}/{}\n".format(
            self.hp, self.max_hp, self.xp, self.required_xp())
        status += "    Ferocity: {:2d}    Acrobatics: {:2d}    Curiosity: {:2d}\n".format(
            self.ferocity, self.acrobatics, self.curiosity)
        status += "    Moves: {}\n".format(self.get_moves())
        status += "    Items: {}".format(self.list_items())
        print_msg_box(status, title, align="none")
        #print("DEBUG:Quest Items:{}\nQuest Monsters:{}\nQuest Kills:{}\n".format(self.quest_items, self.quest_monsters, self.kills))

    def add_stat(self, give=["cur", 0]):
        if(give[0] == "cur"):
            self.curiosity += give[1]
        if(give[0] == "acr"):
            self.acrobatics += give[1]
        if(give[0] == "fer"):
            self.ferocity += give[1]

    def try_move(self, curRoom, direction):
        # dirs = { 0:"North", 1:"East", 2:"South", 3:"West" }
        if(curRoom.exits[direction] != False):
            self.enter(world.worldMap[curRoom.exits[int(direction)]])
        else:
            print("You can't go that way")
            return False

    def enter(self, room="dummy"):
        if(type(room) == str):
            room = worldMap[room]
        self.location = room.id
        # tick the npcs each time you move
        # don't iterate the current map, we'll get duplicate npcs
        tickmap = copy.deepcopy(world.worldMap)
        for i in tickmap:
            i = tickmap[i]
            if(i.npc != ""):
                npcList[i.npc].tick(worldMap)
        self.look(worldMap[self.location])

    def look(self, room):
        exit_dirs = {0: "North", 1: "East", 2: "South", 3: "West"}
        describe = world.worldMap[self.location].describe(
            worldMap, npcList, self)
        print(centered("    "+COLORS.PURPLE+describe["area"]+COLORS.END+"    "))
        print_msg_box(describe["desc"], describe["title"], align="left")
        if(describe["exits"] != False):
            exits = ""
            for dir in list(exit_dirs.keys()):
                if(describe["exits"][dir] is not False):
                    exits += "    {}: {}\n".format(
                        exit_dirs[dir], world.worldMap[describe["exits"][dir]].name)
            print_msg_box(exits[:-1], "Exits", align="none", width=41)

    def rest(self):
        if(self.location == "start4"):  # free rest at the starting area
            self.hp = self.max_hp
            cls()
            speak("You take a nice nap in the comfort of your own yard.")
            speak("Your HP is refilled!")
            time.sleep(1)
            return
        else:
            print("You will lose up to {} XP when resting outside of your own yard. Your attitude will also be reset to normal. You won't lose any levels or stats.\nAll of your HP will be restored.".format(self.level))
            print("Rest? (y/n)")
            action = input("?> ")
            action = str(action).lower()
            if(action in ["yes", "y", "no", "n"]):
                if(action in ["yes", "y"]):
                    self.hp = self.max_hp
                    loss = randint(0, self.level)
                    self.xp -= loss
                    if(self.xp < 0):
                        self.xp = 0
                    self.clear_attitude()
                    print("Your HP is refilled!\nHowever, you lost {} XP.  Your total XP is now: {}".format(
                        loss, self.xp))
                else:
                    return
            else:
                print("Invalid action")
                return

    def hunt(self, room):
        if(self.hp <= 0):
            print("You are too tired for hunting now. You need to rest.")
            return
        if(room.random_battle == True):
            e = gameMonsters[choice(room.enemies)]
            enemy = Enemy(name=e["name"], hp=e["hp"],
                          moves=e["moves"], xp_given=e["xp_given"], drop=e["drop"], fer=e["fer"], acr=e["acr"])
            cls()
            encounter = ["You spot a {}!",
                         "You encounter a {}!", "You come upon a {}!"]
            speak(choice(encounter).format(enemy.name))
            anykey()
            if(self.battle(enemy)):
                cls()
                victory = ["Victory!", "You are the ultimate hunter!",
                           "You have emerged victorious!", "You are master of the hunt!", "Your prey runs away scared!"]
                speak(choice(victory))
                anykey()
            else:
                cls()
                speak("You run away embarassed! You should rest.")
                anykey()
            del enemy
        else:
            print("There doesn't seem to be anything to hunt around here.")
            anykey()
            time.sleep(1)

    def use_item(self, item):
        if(type(item) is str):
            if(item in list(items.gameItems.keys())):
                item = items.gameItems[item]
            else:
                print("You can't just type anything you want!")
                return
        if(item not in self.items):
            print("You don't have that!")
            return
        elif(item.item_type != "usable"):
            print("You can't use that!")
            return
        else:
            item.use(self, world.worldMap)
            self.items.remove(item)
            print(item.use_text)

    def level_up(self):
        cls()
        print("DING!  Level up!  GRATTIES!")
        print("Choose an attribute to level up:")
        print("1. Ferocity: {}\n2. Acrobatics: {}\n3. Curiosity: {}".format(
            self.ferocity, self.acrobatics, self.curiosity))
        stat = int(input("?> "))
        if(stat == ""):
            print("Try that again. (1,2,3)")
            self.level_up()
        if(stat in [1, 2, 3]):
            if(stat == 1):
                self.ferocity += 1
                print("Your ferocity is now {}".format(self.ferocity))
            if(stat == 2):
                self.acrobatics += 1
                print("Your acrobatics is now {}".format(self.acrobatics))
            if(stat == 3):
                self.curiosity += 1
                print("Your curiosity is now {}".format(self.curiosity))
            self.level += 1
            hp_increase = randint(1, 8)+2
            self.max_hp += hp_increase
            print("Your max HP also went up by {} points (now {})".format(
                hp_increase, self.max_hp))
            if(self.level in list(self.learned_moves.keys())):
                self.give_move(self.learned_moves[self.level])
        else:
            print("Try that again...")
            self.level_up()

    def battle(self, enemy):
        '''
        Battle time!
        '''
        
        if(type(enemy) == str):
            enemydata = gameMonsters[enemy]
            enemy = Enemy(
                name=enemydata["name"],
                moves=enemydata["moves"],
                hp=enemydata["hp"],
                xp_given=enemydata["xp_given"],
                drop=enemydata["drop"],
                fer=enemydata["fer"],
                acr=enemydata["acr"]
            )
        
        cls()
        victory = True
        turn = 1

        _battle_screen = '''
Your prey is: {}

+---------+  +---------+   
| Your HP |  |  Prey   | 
    {:<2}           {:<2} 
+---------+  +---------+

+-------- Moves -------+
{}========================
'''

        while(self.hp > 0 and enemy.hp > 0):
            player_hp_str = colored(str(self.hp), 'green')
            enemy_hp_str = colored(str(enemy.hp), 'red')
            print(_battle_screen.format(enemy.name, player_hp_str,
                                        enemy_hp_str, self.list_attacks()))

            # player turn
            if(enemy.hp > 0):
                # print(self.list_attacks())
                attack_choice = input("?> ")
                while(attack_choice.isdigit() == False or int(attack_choice) > len(self.moves)):
                    print("Try that again")
                    attack_choice = input("?> ")
                self.attack(enemy, self.moves[int(attack_choice)-1])

            if(enemy.hp > 0):
                enemy.attack(self, choice(enemy.moves))
                if(self.hp <= 0):
                    return False
                    # END OF COMBAT
            turn += 1
        time.sleep(1)
        cls()
        victory = True
        self.xp += enemy.xp_given
        d100 = randint(1, 100)
        if(enemy.drop != False):
            print("DEBUG Loot roll: {}".format(d100))
            if(d100 <= enemy.drop[1]):
                self.give_items([gameItems[enemy.drop[0]]])
        print("You earned {} xp!".format(enemy.xp_given))
        if(enemy.name.lower() in self.quest_monsters):
            self.kills[enemy.name.lower()] += 1
        if(self.xp >= self.required_xp()):
            self.level_up()
        return victory


# random battle with random monster example:
#
# v = game.battle(p, gameMonsters[choice(list(mlist))])
#
#


# main game class/functions
class Game():
    def __init__(self, player=None):
        self.state = 0
        self.starting_location = "start4"
        self.boss_location = "alley6"
        self.name = "Cat Game"
        self.player = player
        self.score = 0
        self.turn = 0
        self.exit_dirs = {0: "North", 1: "East", 2: "South", 3: "West"}
        self.acceptable_verbs = ["move", "go", "look", "inspect", "lay", "lie", "examine", "hunt",
                                 "sniff", "smell", "equip", "status", "rest", "sleep", "climb", "help",
                                 "talk", "speak", "hit", "paw", "push", "use", "take", "get", "grab"]
        self.up_dir = ["up", "u", "n", "north"]
        self.down_dir = ["down", "d", "s", "south"]
        self.left_dir = ["left", "l", "w", "west"]
        self.right_dir = ["right", "r", "e", "east"]
        self.title_choices = ["play", "quit", "help"]
        self.disallowed_names = ["momo", "mochi", "mika", "morty",
                                 "mortimer", "mori", "moriko", "dorian", "moreau", "mermo"]
        if(isinstance(self.player, Player)):
            print("Pre-loaded character...")
            self.exit()
        else:
            self.start_game()

    def prompt(self):
        if(self.turn == 999):
            self.game_over()
            return
        print(" {:2d}                           ".format(self.turn))
        print("┍━━━━━━━━━━━━━━✿━━━━━━━━━━━━━━━┑")
        print("  What would you like to do?")
        print("  (move, look, status, help...)")
        print("┕━━━━━━━━━━━━━━✿━━━━━━━━━━━━━━━┙")
        action = input("?> ") or ""
        self.parse_input(action.lower())
        self.prompt()  # loopback

    def game_over(self):
        cls()
        custom_fig = Figlet(font='univers')
        print(custom_fig.renderText('Game Over'))
        print("You took too long to make friends!")
        time.sleep(1)
        anykey()
        self.show_title_screen()

    def parse_input(self, action):
        if(action == ""):
            print("Invalid action")
            pass
        else:

            action = action.split()
            stopwords = ['at', 'the', 'my', 'a', 'to', 'up', 'down', 'on']
            verb = action[0]
            room_events = world.worldMap[self.player.location].get_event_list()

            if(len(action) == 1):
                noun = ""
            elif(len(action) > 1):
                action.remove(verb)
                for word in list(action):
                    if word in stopwords:
                        action.remove(word)
                noun = " ".join(action)
            if(verb == "teleport"):
                self.player.enter(noun)
                pass
            elif (verb in self.acceptable_verbs):
                # handle specific verbs
                cls()
                self.turn += 1
                if(verb in ["rest", "sleep"]):
                    self.player.rest()
                    pass
                if(verb == "help"):
                    self.show_help_screen(True)
                    pass
                if(verb in ["move", "go"] and noun == ""):
                    print("Try typing 'move north' or 'go east'")
                    pass
                if(verb in ["move", "go"] and noun != ""):
                    if noun.lower() in self.up_dir:
                        direction = 0
                    elif noun.lower() in self.right_dir:
                        direction = 1
                    elif noun.lower() in self.down_dir:
                        direction = 2
                    elif noun.lower() in self.left_dir:
                        direction = 3
                    self.player.try_move(
                        world.worldMap[self.player.location], direction)
                if(verb in ["look", "inspect", "examine", "lay", "lie", "sniff", "smell", "climb", "take", "get", "grab", "hit", "paw", "push"]):
                    if(verb in ["hit", "push", "paw"]):
                        verb = "hit"
                    if(verb in ["sniff", "smell"]):
                        verb = "sniff"
                    if(verb in ["lay", "lie"]):
                        verb = "lay"
                    if(verb in ["take", "get"]):
                        verb = "take"
                    if(verb in ["look", "inspect", "examine"]):
                        verb = "look"

                    if(noun not in room_events and noun == ""):
                        if(verb == "look"):
                            self.player.look(
                                world.worldMap[self.player.location])
                            pass
                    elif(noun not in room_events and noun != ""):
                        print(
                            "There isn't anything like that around here.")
                        pass
                    elif(noun in room_events and noun != ""):
                        world.worldMap[self.player.location].events[noun].fire(
                            noun, verb, self.player, world.worldMap)
                        pass
                    pass
                if(verb == "equip"):
                    self.player.equip(noun)
                    pass
                if(verb == "hunt"):
                    self.player.hunt(world.worldMap[self.player.location])
                    self.player.look(world.worldMap[self.player.location])
                    pass
                if(verb == "status"):
                    self.player.show_status()
                    pass
                if(verb == "use"):
                    self.player.use_item(noun)
                    pass
                if(verb in ["talk", "speak"]):
                    if(world.worldMap[self.player.location].npc == ""):
                        print("There's no one to talk to here.")
                    else:
                        world.worldMap[self.player.location].handle_npc(
                            self.player, world.npcList, items.gameItems)
                    pass
            else:
                print("Not a proper command! Try again")
        self.prompt()  # loop back

    def start_game(self):
        self.show_title_screen()

    def exit(self):
        sys.exit()

    def show_help_screen(self, prompt=False):
        cls()
        help_str = ""
        help_str += "In this game, you are a cat. "
        help_str += "This is the complete list of of verbs allowed in this game (some are synonyms):\n {}".format(", ".join(self.acceptable_verbs))
        print_msg_box(help_str, "Game Help", align="left")
        anykey()
        if(prompt):
            self.prompt()
        else:
            self.show_title_screen()

    def title_screen_graphics(self, screen):
        effects = [
            Cycle(
                screen,
                FigletText("Cat", font='univers'),
                screen.height // 2 - 8),
            Cycle(
                screen,
                FigletText("Quest", font='univers'),
                screen.height // 2 + 3),
            Stars(screen, (screen.width + screen.height) // 2)
        ]
        screen.play([Scene(effects, 66)], repeat=False)

    def show_title_screen(self):
        cls()
        Screen.wrapper(self.title_screen_graphics)
        self.title_screen_select()

    def intro_screen(self, screen):
        scenes = []
        effects = [
            Scroll(screen, 3),
            Mirage(
                screen,
                FigletText("A long time ago...", font='starwars'),
                screen.height,
                Screen.COLOUR_YELLOW),
            Mirage(
                screen,
                FigletText("In a yard far, far away", font='starwars'),
                screen.height + 8,
                Screen.COLOUR_YELLOW),
        ]
        scenes.append(Scene(effects, (screen.height + 104) * 3))
        effects = [
            Scroll(screen, 3),
            Print(screen, SpeechBubble("Press X to continue"),
                  screen.height+12, Screen.COLOUR_CYAN)
        ]
        scenes.append(Scene(effects, 300, clear=True))
        screen.play(scenes, stop_on_resize=True, )

    def title_screen_select(self):
        print_msg_box("Type: play, help or quit", "Make your choice meow")
        action = str(input("?> "))
        action = action.lower()
        if(action in self.title_choices):
            if action == "play":
                # Screen.wrapper(self.intro_screen)
                cls()
                print_msg_box("Lorem ipsum intro text can go here.",
                              "Title Goes here", align="center")
                anykey()
                cls()
                self.character_creation()
            if action == "quit":
                self.exit()
            if action == "help":
                self.show_help_screen()
        else:
            print("Invalid action")
            self.title_screen_select()

    # Select breed for character creation
    def breed_choice(self):
        cls()
        breed_data = "\n"
        for i in range(len(breedList)):
            breed_data += "    {}  {} - {}\n".format(str(i+1),
                                                     breedList[i].name, breedList[i].desc)
        print_msg_box(breed_data, "Pick a Breed", align="none")
        print("\n")
        print("Type the corresponding number:")
        try:
            breed = int(input("?>"))
            print("You typed {}".format(breed))
        except ValueError:
            print("Invalid choice")
            return None
        else:
            if(breed in range(len(breedList))):
                return breedList[int(breed)-1]
        return None

    # Init character creation

    def character_creation(self):
        cls()
        name = input("What is your name? >")
        if(name.lower() in self.disallowed_names or name == ""):
            print("You can't use that name! Try again.")
            self.character_creation()
        else:
            breed = None
            while(breed == None):
                breed = self.breed_choice()
            breed_name = breed.name
            cls()
            print("You are a {} named {}, is this what you want?\nType yes or no".format(
                breed_name, name))
            confirm = str(input("?> "))
            if(confirm.lower() in ["yes", "", "y"]):
                stats = breed.stats

                # NEW CHARACTER STATS
                p = Player(
                    breed=breed_name,
                    name=name.capitalize(),
                    fer=stats[0],
                    acr=stats[1],
                    cur=stats[2],
                    moves=[moveList["kick"], moveList["bite"]],
                    items=[gameItems["top hat"],
                           gameItems["potion"], gameItems["gold star"]]
                )
                self.player = p
                print(self.player.name + " is ready to play")
                self.player.show_status()
                anykey()
                self.enter_starting_location()
            else:
                self.character_creation()

    def enter_starting_location(self):
        cls()
        self.player.enter(worldMap[self.starting_location])
        self.prompt()


game = Game()
