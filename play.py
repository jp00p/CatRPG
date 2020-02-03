import cmd, textwrap, sys, os, time, string, platform
from random import seed, randint, randrange, choice, sample
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
from termcolor import colored 


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

def print_msg_box(msg, indent=1, width=screen_width-4, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    box = ''
    if not width:
        width = max(map(len, lines))
    if not title:
      box += f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    else:
      title = "╣ " + str(title) + " ╠"
      box += f'╔'
      box += title.center(width + indent * 2, "═")
      box += f'╗\n'  # upper_border       
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

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
        #print("ATTACK #{} -- HIT ROLL: {}({}) -- TARGET AC: {} ".format(attack_time,hit,d20,target))
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

# Enemy is just a basic Character right now
class Enemy(Character):
  def __init__(self, hp=0, **kwargs):
    super().__init__(**kwargs)
    self.max_hp = hp
    self.hp = hp

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
    self.hp = 50
    self.max_hp = 50
    self.items = items
  def required_xp(self):
    req = (self.level * 5)+self.level-1
    return req
  def equip(self,item=""):
    if(item == ""):
      print("What are you trying to equip?")
      return
    print("Current items:\n{}".format(self.list_items))
    print("Item name to equip:{} ".format(item))
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
      self.hat = item
      print("You put on the {}".format(item.name))
  def apply_attitude(self,item):
    # for when events apply items
    return
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
    title = "{} the {}".format(self.name.capitalize(), self.breed)
    status = "Level: {}\n".format(self.level)
    status += "Attitude: {}   Hat: {}\n".format(self.get_attitude(), self.get_hat())
    status += "HP: {}/{}  XP: {}\n".format(self.hp,self.max_hp,self.xp)
    status += "Required for next level: {}\n".format(self.required_xp())
    status += "Ferocity: {}  Acrobatics: {}  Curiosity: {}\n".format(self.ferocity, self.acrobatics, self.curiosity)
    status += "Move List: {}\n".format(self.list_attacks())
    status += "Item List: {}\n".format(self.list_items())
    print_msg_box(status,1,screen_width-4,title)
    
  def try_move(self,curRoom,direction):
    # dirs = { 0:"North", 1:"East", 2:"South", 3:"West" }
    if(curRoom.exits[direction] != False):
      new_room = worldMap[curRoom.exits[int(direction)]]
      self.enter(new_room,curRoom.exits[direction])
    else:
      print("You can't go that way")
      return False
  def enter(self,room,room_id):
    self.location=room_id
    room.describe()

  # rest your weary head  
  def rest(self):
    print("You will use some XP when resting.  You won't lose any levels or stats.\nAll of your HP will be restored.")
    print("Rest? (y/n)")
    action = input("?> ")
    action = str(action).lower()
    if(action in ["yes","y","no","n"]):
      if(action in ["yes","y"]):
        self.hp = self.max_hp
        loss = randint(0,3)
        self.xp -= loss
        if(self.xp < 0):
          self.xp = 0
        print("You lost {} XP.  Your total XP is now: {}".format(loss,self.xp))
      else:
        return
    else:
      print("Invalid action")

  def hunt(self, room):
    if(room.random_battle == True):
      e = gameMonsters[choice(room.enemies)]
      enemy = Enemy(name=e["name"],hp=e["hp"],moves=e["moves"])
      cls()
      speak("You spot a {}!".format(enemy.name))
      time.sleep(1)
      if(self.battle(enemy)):
        print("You are master of the hunt!")
      else:
        print("You need to rest.")
      del enemy
    else:
      print("There doesn't seem to be anything to hunt around here.")
  def level_up(self):
    print("Level up!")
    print("Choose an attribute to level up:")
    print("1. Ferocity: {}\n2. Acrobatics: {}\n3. Curiosity: {}".format(self.ferocity, self.acrobatics, self.curiosity))
    stat = input("?> ")
    while(stat.isdigit() == False):
      print("Try that again.")
      self.level_up()
    if(stat in [1,2,3]):
      if(stat == 1):
        self.ferocity += 1
      if(stat == 2):
        self.acrobatics += 1
      if(stat == 3):
        self.curiosity += 1
      self.level += 1
      hp_increase = randint(1,8)
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
      combat_data = "Your HP: "
      combat_data += colored(str(self.hp), 'green')
      combat_data += "\n"
      combat_data += "Enemy HP: "
      combat_data += colored(str(enemy.hp), 'red')
      combat_data += "\n"
      print("Turn: {}".format(turn))
      print_msg_box(combat_data)
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
        self.xp += 1
        if(self.xp >= self.required_xp()):
          self.level_up()
        return victory

      if(initiative == 1 and enemy.hp > 0):
        enemy.attack(self,choice(enemy.moves))
      turn += 1
    enemy = None
    del enemy
    return victory



# an attack move
class Move:
  def __init__(self, name="", verbs=[], dmg=[], hit=0, targets=[1,1], times=[0,1], **kwargs):
    self.name = name
    self.verbs = verbs
    self.dmg = dmg
    self.hit = hit
    self.targets = targets
    self.times = times

moveList = {
  "claw" : Move(
    name="Claw",
    verbs=['{} swipes at {} with their claws!', '{} slashes with their claws!'],
    dmg = [1,6],
    times = [0,2]
  ),
  "bite" : Move(
    name="Bite",
    verbs=['{} chomps on {}!', '{} bites {}!', '{} gives {} a little nibble.'],
    dmg = [0,1],
    hit = -1,
  ),
  "peck" : Move(
    name="Peck",
    verbs=['{} pecks at {}!', '{} dives at {} with their beak!'],
    dmg = [1,2],
    times = [0,4]
  ),
  "kick" : Move(
    name="Kick",
    verbs=['{} does a crazy kick!', '{} kicks {}!'],
    dmg=[10,15],
    times = [0,1]
  ),
  "slap" : Move(
    name="Slap",
    verbs=['{} does a powerful multi-slap!'],
    dmg=[2,4],
    times = [0,3]
  ),
  "tailgrab" : Move(
    name="Tail Grab",
    verbs = ['{} grabs {}\'s tail!'],
    dmg=[4,6],
    times=[0,1],
    hit=-2
  ),
  "backrub" : Move(
    name="Backwards Fur Rub",
    verbs = ['{} rubs {}\'s backwards!'],
    dmg=[1,2],
    times=[0,2]
  )
}
 
#  ###################  #
#  MONSTER FACTORY !!!  #
#  ###################  #
def makeMonster(name, moves, hp):
  monster = Enemy(name=name,moves=moves,max_hp=hp)
  return monster

gameMonsters = {
  "bird" : {
    "name" : "Bird",
    "moves" : [moveList["peck"]],
    "hp" : 20
  },
  "squirrel" : {
    "name" : "Squirrel",
    "moves" : [moveList["bite"],moveList["claw"]],
    "hp" : 12
  }
  # "mouse" : makeMonster("Mouse"),
  # "alleycat" : makeMonster("Alleycat"),
  # "child" : makeMonster("Human Child")
}
mlist = gameMonsters.keys()
# random battle with random monster example:
#
# v = game.battle(p, gameMonsters[choice(list(mlist))])
#
#

class Item():
  def __init__(self, name="",fer=0,acr=0,cur=0,max_hp=0,item_type="", **kwargs):
    self.name = name
    self.fer = fer
    self.acr = acr
    self.cur = cur
    self.max_hp = max_hp
    self.item_type = item_type
    return

gameItems = {
  "grumpy" :      Item("Grumpy", 0,0,0,0, item_type="attitude"),
  "zoomy" :       Item("Zoomy", 0,0,0,0, item_type="attitude"),
  "inquisitive" : Item("Inquisitive", 0,0,0,0, item_type="attitude"),
  "sleepy" :      Item("Sleepy", 0,0,0,0, item_type="attitude"),
  "top hat" :      Item("Top Hat", 0,0,0,0, item_type="hat"),
  "bunny ears"  :      Item("Bunny Ears", 1,1,1,1, item_type="hat")
}



class Event:
  def __init__(self, reqs={}, descs={}, trigger_text="", remove_self=False, on_trigger=[], e_type="",**kwargs):
    self.reqs = reqs
    self.descriptions = descs
    self.trigger_text = trigger_text
    self.remove_self = remove_self
    self.on_trigger = on_trigger
    self.e_type = e_type
  def fire(self, noun, verb, player):
    print("Debug: Required {}: {} - Yours is {}\nTriggered on {}".format(
      self.reqs["stat"],
      self.reqs["value"],
      getattr(player,self.reqs["stat"]),
      self.reqs["trigger"]
    ))
    if(self.descriptions[verb] != False):
      print(self.descriptions[verb])
    if((getattr(player,self.reqs["stat"]) >= self.reqs["value"]) and (verb == self.reqs["trigger"])):
      print(self.trigger_text)
      if(self.on_trigger):
        obj = self.on_trigger[0]
        method = self.on_trigger[1]
        value = self.on_trigger[2]
        if(obj == "room"):
          call = getattr(worldMap[player.location],method)
        if(obj == "player"):
          call = getattr(player,method)
        call(value) # def need some error handling here
      if(self.remove_self):
        worldMap[player.location].events.pop(noun)

      





class Room:
  def __init__(self, name='', area='', description = '', room_type = '',\
               enemies = [], items = [], exits = [],\
               random_battle = False, state=0, states = {}, events = {}, **kwargs):
    self.room_type = room_type
    self.name = name
    self.area = area
    self.description = description # evergreen description
    self.states = states # list of states
    self.state = state # which state is the room in
    self.items = items # list of obtainable items (using get verb)
    self.events = events
    self.enemies = enemies # maybe...
    self.exits = exits # which exits does this room have
    self.random_battle = random_battle
  def show_exits(self):
    dirs = {0:"North", 1:"East", 2:"South", 3:"West"}
    for dirkey in list(dirs.keys()):
      if(self.exits[dirkey] is not False):
        return("{}: {}\n".format(dirs[dirkey],worldMap[str(self.exits[dirkey])].name))
  def get_event_list(self):
    elist = self.events.keys()
    return elist
  def describe(self):
    cls()
    centered("Area: "+self.area)
    print("\n")
    area_text = self.description + "\n"
    if(self.states):
      area_text += self.states[self.state]+"\n"
    area_text += "Exits".center(screen_width-4,"-")
    area_text += "\n"
    area_text += self.show_exits()
    print_msg_box(area_text,title=self.name)
    time.sleep(0.33)
  def setState(self, state):
    self.state = state

worldMap = {
  "fyard1" : Room(
    name="A Bushy Corner",
    area="Front Yard",
    description="A corner of the yard full of bushes. You see a note pinned to a tree.",
    items=[],
    exits=["porch1","fyard2",False,False],
    enemies=["bird", "squirrel"],
    random_battle=True,
    state=1,
    states={
      0:"Nothing is going on around here right now",
      1:"There's a fire!",
      2:"Notes are fun to read."
    },
    events={
      "catnip" : Event(
        reqs={ 
          "stat" : "curiosity", 
          "value": 1, 
          "trigger":"sniff" 
        },
        descs={ "sniff": "Smells a little funny.", "look" : "Almost looks illegal." },
        trigger_text="You get a little high from sniffing the nip.", 
        remove_self=True,
        on_trigger=["room", "setState", 0],
        e_type="text"
      ),
      "note" : Event(
        reqs={ 
          "stat" : "curiosity", 
          "value": 2, 
          "trigger":"look" 
        },
        descs={ "sniff": "Smells like paper and ink.", "look" : "You can barely make out the words." },
        trigger_text="The note says \"Wow this works great.\"", 
        remove_self=False,
        on_trigger=["room", "setState", 2],
        e_type="text"
      )
    }
  ),
  "fyard2" : Room(
    name="Grassy Lounging Area",
    area="Front Yard",
    description="A nice, grassy area to relax in.",
    exits=["porch1", False, False, "fyard1"]
  ),
  "porch1" : Room(
    name="Secretive Porch",
    area="House (Outside)",
    description="A nice hiding spot",
    exits=["house1", False, False, "fyard1"]
  ),
  "house1" : Room(
    name="Food cave",
    area="House (Inside)",
    description="This where the food is",
    exits=[False,False,"porch1",False]
  )
}

class Breed():
  def __init__(self, name="", stats=[], desc="", **kwargs):
    self.name = name
    self.stats = stats # fer,acr,cur
    self.desc = desc

breedList = [
  Breed("Debug Cat", [50,50,50], "GOD MODE"),
  Breed("Domestic Shorthair", [2,2,1], "Average and curious"),
  Breed("Persian", [3,1,0], "Slow but fluffy"),
  Breed("Sphynx", [1,3,0], "Quick and lightweight"),
  Breed("Tuxedo", [2,0,2], "Well-dressed and inquisitve"),
  Breed("Maine Coon", [4,0,0], "Super big and beautiful"),
  Breed("Abyssinian", [0,4,0], "Lean and super acrobatic"),
  Breed("Scottish Fold", [0,0,4], "Super curious explorer")
]

# main game class/functions
class Game():
  def __init__(self, player=None):
    self.state = 0
    self.location = "house1"
    self.starting_location = "fyard1"
    self.boss_location = "alley6"
    self.name = "Cat Game"
    self.player = player
    self.score = 0
    self.turn = 0
    self.acceptable_verbs = ["move", "go", "look", "hunt", "sniff", "equip", "status", "rest"]
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
    print_msg_box("What would you like to do? (move, look, sniff, status, help...)")
    action = input("?> ") or ""
    self.parse_input(action.lower())
    self.prompt() # loopback
  def parse_input(self,action):
    if(action == ""):
      print("Invalid action")
      pass
    else:
      action = action.split()
      stopwords = ['at', 'the', 'my', 'a']
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
        if(verb == "rest"):
          self.player.rest()
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
        if(verb in ["look", "sniff"]):
          if(noun not in room_events or noun == ""):
            worldMap[self.player.location].describe()
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
      else:
        print("Not a proper command! Try again")
    self.prompt() # loop back
  def start_game(self):
    self.show_title_screen()
  def exit(self):
    sys.exit()
  def show_help_screen(self):
    print("Help screen goes here")
    anykey()
    self.show_title_screen()
  def show_title_screen(self):
    cls()
    custom_fig = Figlet(font='univers')
    print(custom_fig.renderText('Meow'))
    self.title_screen_select()
  def title_screen_select(self):
    print_msg_box("Type: play, help or quit", indent=2, title="Make a choice")
    action = input("?> ")
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
    breed_choice_text = ""
    breed_choice_title = "Pick a Breed"
    for i in range(len(breedList)):
      # show list like 1: BreedName...
      breed_choice_text += "{}: {}\n".format(i+1, breedList[i].name)
    print_msg_box(breed_choice_text,1,screen_width-4,breed_choice_title)
    print("Type the corresponding number:")
    breed = input("?> ")
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
    self.player.enter(worldMap[self.starting_location], self.starting_location)
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


