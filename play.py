from __future__ import print_function
import cmd, textwrap, sys, os, time, string, platform, copy
from random import seed, randint, randrange, choice, sample
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
from termcolor import colored 
from terminaltables import AsciiTable, DoubleTable, SingleTable

from character.gamemonsters import gameMonsters
from character.movelist import moveList
from character.breed import Breed, breedList
from items.gameitems import Item, gameItems
from world.worldmap import Room, worldMap, Event, NPC, npcList
#from world.npc import NPC

# todo:
# NPCS, quests, riddles, attitudes, keep away?

init(autoreset=True)
# colored_text = colored('Title Screen', 'green', 'on_red')

### Utility functions
screen_width=79
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

def speak(words, speed = 0.01, wait=0.25):
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

def print_msg_box(msg, indent=1, width=screen_width-4, title=""):
    print("・━━━━━♡━☆★ " + title + " ★☆━♡━━━━━・\n")
    msg = text_wrapper.fill(msg)
    print(msg)

### Base Character Class
class Character:
  def __init__(self, name='', hp=0, fer=2, acr=2, cur=2, moves=[], **kwargs):
    self.name = name
    self.hp = hp
    self.max_hp = self.hp
    self.ferocity = fer # str
    self.acrobatics = acr # dex
    self.curiosity = cur # luck
    self.moves = moves
  def attack(self, other, move):
      attack_time = 1
      move_desc = choice(move.verbs)
      hr()
      print(move_desc.format(self.name, other.name)) # describe attack
      hr()
      # for each time the move can hit (move.times)
      for _ in range(move.times[0], move.times[1]):

        # roll dice, add mods
        d20 = randint(1,20)     
        dmg_string = ""
        hit_mod = move.hit
        base_dmg = randrange(move.dmg[0], move.dmg[1]) # 
        dmg = 0 # holds the total dmg
        hit = d20+self.acrobatics+hit_mod # THAC0
        target = 10+other.acrobatics # AC
        print("DEBUG: MOVE HIT:{} -- BASE_DMG:{}".format(hit_mod, base_dmg))
        print("DEBUG: ATTACK #{} -- HIT ROLL: {}({}) -- TARGET AC: {} ".format(attack_time,hit,d20,target))
        attack_time += 1

        if(d20 == 20):
          #crit
          dmg = self.ferocity+move.dmg[1] # do the max dmg of the move + ferociy
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
            dmg_string += "\nIt barely hurts.\n"
            dmg = randint(0,1)
          #print("Deals {} damage".format(dmg))
          dmg_string += "Deals {} damage".format(dmg)
          other.hp -= dmg
        else:
          # miss
          # print(self.name + " missed!")
          dmg_string += "{} missed!".format(self.name)
      speak(dmg_string)
      time.sleep(0.25)

class Enemy(Character):
  def __init__(self, hp=0, xp_given=1, **kwargs):
    super().__init__(**kwargs)
    self.max_hp = hp
    self.hp = hp
    self.xp_given = xp_given




### Player Character
class Player(Character):
  def __init__(self, breed = '', items = [], **kwargs):
    super().__init__(**kwargs)
    self.breed = breed
    self.location = "fyard1"
    self.attitude = None # weapon slot
    self.hat = None # armor slot
    self.level = 1
    self.xp = 0
    self.hp = 36
    self.max_hp = 36
    self.items = items
    self.kills = {}
    self.quest_monsters = []
    self.quest_items = []
  def required_xp(self):
    req = (self.level * 5)+self.level-1
    return req
  def give_quest(self,quest_type,quest_thing):
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
  def remove_items(self,items):
    for item in items:
      self.items.remove(item)
    
  def equip(self,item=""):
    if(item == ""):
      print("What are you trying to equip?")
      return
    print("DEBUG Current items:\n{}".format(self.list_items()))
    print("DEBUG Item name to equip:{} ".format(item))
    item = gameItems[item]
    if(item not in self.items):
      print("You don't have that item")
    elif(item.item_type != "hat"):
      print("How would a cat equip that?")
    else:
      self.items.remove(item)
      if(self.hat != None):
        print("You remove your {} and put it back in your inventory.".format(self.hat.name))
        self.items.append(self.hat)
      self.apply_item(item)
      print("You put on the {}".format(item.name))
  def apply_item(self,item):
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
    self.ferocity += item.fer
    self.acrobatics += item.acr
    self.curiosity += item.cur
    self.max_hp += item.max_hp

  def list_items(self):
    _items = ""
    for i in range(len(self.items)):
      _items += self.items[i].name + "\n"
    return _items
  def list_attacks(self):
    _attacks = ""
    for i in range(len(self.moves)):
      _attacks += str(i+1) + ") " + self.moves[i].name + "\n"
    return _attacks
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
  def show_status(self):
    cls()
    title = "{} the {}\n".format(self.name.capitalize(), self.breed)
    status = "Level: {}\n".format(self.level)
    status += "Attitude: {}\tHat: {}\n".format(self.get_attitude(), self.get_hat())
    status += "HP: {}/{}\tXP: {}/{}\n".format(self.hp,self.max_hp,self.xp, self.required_xp())
    status += "Ferocity: {}\tAcrobatics: {}\tCuriosity: {}\n".format(self.ferocity, self.acrobatics, self.curiosity)
    status += "Move List:\n{}\n".format(self.list_attacks())
    status += "Item List:\n{}\n".format(self.list_items())
    status += "Quest Items:{}\nQuest Monsters:{}\nQuest Kills:{}\n".format(self.quest_items,self.quest_monsters,self.kills)
    print(title)
    print(status)
    
  def try_move(self,curRoom,direction):
    # dirs = { 0:"North", 1:"East", 2:"South", 3:"West" }
    if(curRoom.exits[direction] != False):
      new_room = worldMap[curRoom.exits[int(direction)]]
      self.enter(new_room)
    else:
      print("You can't go that way")
      return False
  def enter(self,room):
    if(type(room) == str):
      room = worldMap[room]
    self.location=room.id
    tickmap = copy.deepcopy(worldMap)
    for i in tickmap:
      i = tickmap[i]
      if(i.npc != ""):
        print("{} is moving".format(i.npc))
        npcList[i.npc].tick()
    room.describe()

  # rest your weary head  
  def rest(self):
    print("You will lose up to {} XP when resting.  You won't lose any levels or stats.\nAll of your HP will be restored.".format(self.level))
    print("Rest? (y/n)")
    action = input("?> ")
    action = str(action).lower()
    if(action in ["yes","y","no","n"]):
      if(action in ["yes","y"]):
        self.hp = self.max_hp
        loss = randint(0,self.level)
        self.xp -= loss
        if(self.xp < 0):
          self.xp = 0
        print("You lost {} XP.  Your total XP is now: {}".format(loss,self.xp))
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
      enemy = Enemy(name=e["name"],hp=e["hp"],moves=e["moves"])
      cls()
      encounter = ["You spot a {}!", "You encounter a {}!", "You come upon a {}!"]
      speak(choice(encounter).format(enemy.name))
      time.sleep(1)
      if(self.battle(enemy)):
        victory = ["Victory!", "You are the ultimate hunter!", "You have emerged victorious!", "You are master of the hunt!"]
        print(choice(victory))
      else:
        print("You are too tired for hunting now. You need to rest.")
      del enemy
    else:
      print("There doesn't seem to be anything to hunt around here.")
  def level_up(self):
    print("DING!  Level up!  GRATTIES!")
    print("Choose an attribute to level up:")
    print("1. Ferocity: {}\n2. Acrobatics: {}\n3. Curiosity: {}".format(self.ferocity, self.acrobatics, self.curiosity))
    stat = int(input("?> "))
    if(stat == ""):
      print("Try that again. (1,2,3)")
      self.level_up()
    if(stat in [1,2,3]):
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
      hp_increase = randint(1,8)+2
      self.max_hp += hp_increase
      print("Your max HP also went up by {} points (now {})".format(hp_increase,self.max_hp))
    else:
      print("Try that again...")
      self.level_up()
    
  def battle(self,enemy):
    cls()
    victory = False
    turn = 1
    initiative = randint(0,1)
    if(initiative == 0):
      speak("They go first")
    else:
      speak("You go first")
    time.sleep(0.33)
    cls()

    while(self.hp > 0):
      # do player stuff
      # debug
      #print("Turn #{} -- PHP: {} -- EHP: {}".format(turn,self.hp,enemy.hp))
      if(enemy.hp < 0):
        enemy.hp = 0
      combat_data = "Your HP: "
      combat_data += colored(str(self.hp), 'green')
      combat_data += "\n"
      combat_data += "Enemy HP: "
      combat_data += colored(str(enemy.hp), 'red')
      combat_data += "\n"
      title = "Turn: {}".format(turn)
      print_msg_box(combat_data, title)


      if(initiative == 0 and enemy.hp > 0):
        enemy.attack(self,choice(enemy.moves))
      
      # player turn
      if(enemy.hp > 0):
        print(self.list_attacks())
        attack_choice = input("?> ") # 1 or 2 or 3
        while(attack_choice.isdigit() == False):
          print("Try that again")
          attack_choice = input("?> ") # 1 or 2 or 3
        self.attack(enemy,self.moves[int(attack_choice)-1])
      else:
        # kill enemy
        victory = True
        self.xp += enemy.xp_given
        print("You earned {} xp!".format(enemy.xp_given))
        if(enemy.name.lower() in self.quest_monsters):
          self.kills[enemy.name.lower()] += 1
        if(self.xp >= self.required_xp()):
          self.level_up()
        return victory
      if(initiative == 1 and enemy.hp > 0):
        enemy.attack(self,choice(enemy.moves))
      turn += 1
    enemy = None
    del enemy
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
    self.acceptable_verbs = ["move", "go", "look", "inspect", "examine", "hunt", "sniff", "smell", "equip", "status", "rest", "sleep", "climb", "help", "talk", "speak"]
    self.up_dir = ["up","u","n","north"]
    self.down_dir = ["down","d","s","south"]
    self.left_dir = ["left","l","w","west"]
    self.right_dir = ["right","r","e","east"]
    self.title_choices = ["play", "quit", "help"]
    self.disallowed_names = ["momo", "mochi", "mika", "morty", "mortimer", "mori", "moriko", "dorian", "moreau", "mermo"]
    if(isinstance(self.player, Player)):
      print("Pre-loaded character...")
      self.exit()
    else:
      self.start_game()
      
  def prompt(self):
    print("┍━━━━━━━━━━━━━━✿━━━━━━━━━━━━━━━┑")
    print("  What would you like to do?")
    print("  (move, look, status, help...)")
    print("┕━━━━━━━━━━━━━━✿━━━━━━━━━━━━━━━┙")
    action = input("?> ") or ""
    self.parse_input(action.lower())
    self.prompt() # loopback
  def parse_input(self,action):
    if(action == ""):
      print("Invalid action")
      pass
    else:
      action = action.split()
      stopwords = ['at', 'the', 'my', 'a', 'to']
      verb = action[0]
      room_events = worldMap[self.player.location].get_event_list()

      if(len(action) == 1):
        noun = ""
      elif(len(action) > 1):
        action.remove(verb)
        for word in list(action):
          if word in stopwords:
            action.remove(word)
        noun = " ".join(action)

      if verb in self.acceptable_verbs:
        # handle specific verbs
        self.turn += 1  # eh, lets do it here
        if(verb in ["rest","sleep"]):
          self.player.rest()
          pass
        if(verb == "help"):
          self.show_help_screen(True)
          pass
        if(verb in ["move", "go"] and noun == ""):
          print("Try typing 'move north' or 'go east'")
          pass
        if(verb in ["move","go"] and noun != ""):
            if noun.lower() in self.up_dir:
              direction = 0
            elif noun.lower() in self.right_dir:
              direction = 1 
            elif noun.lower() in self.down_dir:
              direction = 2
            elif noun.lower() in self.left_dir:
              direction = 3
            self.player.try_move(worldMap[self.player.location], direction)
        if(verb in ["look", "inspect", "examine","sniff", "smell", "climb", "take", "hit", "paw", "push"]):
          # todo: take, hit, push
          if(noun not in room_events or noun == ""):
            if(verb in ["look","inspect","examine"]):
              worldMap[self.player.location].describe()
            else:
              print("There isn't a {} around here to {}?".format(noun,verb))
          else:
            worldMap[self.player.location].events[noun].fire(noun, verb, self.player)
          pass
        if(verb == "equip"):
          self.player.equip(noun)
          pass
        if(verb == "hunt"):
          self.player.hunt(worldMap[self.player.location])
          pass
        if(verb == "status"):
          self.player.show_status()
          pass
        if(verb in ["talk","speak"]):
          if(worldMap[self.player.location].npc == ""):
            print("There's no one to talk to here.")
          else:
            worldMap[self.player.location].handle_npc(self.player)
          pass
      else:
        print("Not a proper command! Try again")
    self.prompt() # loop back
  def start_game(self):
    self.show_title_screen()
  def exit(self):
    sys.exit()
  def show_help_screen(self, prompt=False):
    cls()
    print("= Help =")
    print(" In this game, you are a cat. ")
    print(" Your goal is to find and befriend all 7 cats in the neighborhood. ")
    print(" Navigate by typing \"move east\" or \"go north\"" )
    print(" You can just use the letters \"n e s w\" instead of the whole diretion ")
    print(" Type \"look\" to get a description of the area you're in ")
    print(" Type \"look tree\" to look at a tree in the area" )
    print(" There are some other actions to discover too:  sniff, climb, hit... ")
    print(" Type \"hunt\" to hunt for local wildlife and raise your skills!")
    print(" Level up your stats to unlock more stuff! ")
    print(" Type \"status\" to view your status ")
    print(" Collect fun hats and \"equip\" them! Even though you don't have thumbs. ")
    print(" Your attitude can change as well, just like a real cat. ")
    print(" Type \"rest\" if your HP is low or 0. You will lose XP equal to your level (but you won't lose levels)")
    print(" Making a map on paper is recommended! ")
    anykey()
    if(prompt):
      self.prompt()
    else:
      self.show_title_screen()
  def show_title_screen(self):
    cls()
    custom_fig = Figlet(font='univers')
    print(custom_fig.renderText('Meow'))
    self.title_screen_select()
  def title_screen_select(self):
    print_msg_box("Type: play, help or quit", indent=2, title="Make a choice")
    action = str(input("?> "))
    action = action.lower()
    if(action in self.title_choices):
      if action == "play":
        print("Here it goes")
        self.character_creation()
      if action == "quit":
        self.exit()
      if action == "help":
        self.show_help_screen()
    else:
      print("Invalid action")
      self.title_screen_select()

  ### Select breed for character creation        
  def breed_choice(self):
    print("Pick a Breed:")  
    breed_data = ""
    for i in range(len(breedList)):
      breed_data += "{}  {} - {}\n".format(str(i+1), breedList[i].name, breedList[i].desc)
      #breed_choice_text += "{}: {} - {}\n".format(i+1, breedList[i].name, breedList[i].desc)
    #print_msg_box(breed_choice_text,1,screen_width-4,breed_choice_title)
    print(breed_data)
    print("\n")
    print("Type the corresponding number:")
    breed = str(input("?> "))
    if(breed.isdigit() == False):
      print("Invalid choice")
      self.breed_choice()
    while(int(breed) not in range(len(breedList)+1)):
      print("Invalid choice")
      self.breed_choice()
    else:
      return breedList[int(breed)-1]


  ### Init character creation
  def character_creation(self):
    name = input("What is your name? >")
    if(name.lower() in self.disallowed_names or name == ""):
      print("You can't use that name! Try again.")
      self.character_creation()
    else:
      breed = self.breed_choice()    
      breed_name = breed.name
      print("You are a {} named {}, is this good? Type yes, no, or quit".format(breed_name, name))
      confirm = input("?> ")
      if(confirm.lower() == "yes"):
        stats = breed.stats
        p = Player(
          breed=breed_name,
          name=name.capitalize(),
          fer=stats[0],
          acr=stats[1],
          cur=stats[2],
          moves=[moveList["kick"],moveList["bite"]],
          items=[gameItems["top hat"]]
        )
        self.player = p
        print(self.player.name + " is ready to play")
        self.player.show_status()
        anykey()
        self.enter_starting_location()
      elif(confirm.lower() == "no"):
        self.character_creation()
      else:
        self.show_title_screen()
  def enter_starting_location(self):
    self.player.enter(worldMap[self.starting_location])
    self.prompt()
 
game = Game()



















#p = Player("tabby", name="Test Cat", hp=100, moves=[moveList["claw"], moveList["bite"]])
# rest - heal hp, random chance?
# shop - trade g for items/stats/health

# special events based on breed

# sphynx: fast but takes more damage (3,1)
# persian: slow but takes less damage (1,3)
# tabby: balanced (2,2)
# all cats: 5 curiosity to start (npcs wont use)

# to hit: 1d20+dex vs. 10+dex (if 20 = crit?)
# damage: 1d10+str - STR   (cant go below 0)
# curiosty:  unlock new things in rooms if (cur > x)

# level up stats:
# - treats, toys, events
# every 10 xp = level up - choose a stat (ferocity, acrobatics, curiosity)
#  

# shop...?
# cat points = g / fish coins
# collars = 

# player class:  location, name, stats ... room fuctions (look move use show exits... )
# sphynx, persian, tabby ...tux
# hp 
# acrobatics (dex) - hit, speed, jumping
# ferocity (str) - clawing, biting, hissing, kicking
# cuteness (chr) - charming, manipulation
# curiosity (int) - secret detection, points









# game init
# global vars (state, create player...)


# during loop, move the boss around the map -- maybe every 3 player moves 


