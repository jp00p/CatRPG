import time
#from play import print_msg_box, cls
from items.gameitems import gameItems

class Event:
  def __init__(self, reqs={}, descs={}, trigger_text="", remove_self=False, on_trigger=[], e_type="",**kwargs):
    self.reqs = reqs
    self.descriptions = descs
    self.trigger_text = trigger_text
    self.remove_self = remove_self
    self.on_trigger = on_trigger
    self.e_type = e_type
  def fire(self, noun, verb, player):
    print("\nDebug: Required {}: {} - Yours is {}\nTriggered on {}\n".format(
      self.reqs["stat"],
      self.reqs["value"],
      getattr(player,self.reqs["stat"]),
      self.reqs["trigger"]
    ))
    if((getattr(player,self.reqs["stat"]) >= self.reqs["value"]) and (verb == self.reqs["trigger"])):
      print(self.trigger_text)
      if(self.on_trigger):
        for i in self.on_trigger:
          trigger = i
          obj = trigger[0]
          method = trigger[1]
          value = trigger[2]
          if(obj == "room"):
            call = getattr(worldMap[player.location],method) # call = function of Room
          if(obj == "player"):
            call = getattr(player,method) # call = function of player
          call(value) # def need some error handling here
        if(self.remove_self):
          worldMap[player.location].events.pop(noun)
    elif(self.descriptions[verb] != False):
      print(self.descriptions[verb])


class Room:
  def __init__(self, room_id='', name='', area='', description = '', room_type = '',\
               enemies = [], items = [], exits = [],\
               random_battle = False, state=0, states = {}, events = {}, npc="", **kwargs):
    self.room_type = room_type
    self.id = room_id
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
    self.npc = npc
  def show_exits(self):
    exit_text = ""
    dirs = {0:"North", 1:"East", 2:"South", 3:"West"}
    if(self.exits == [False,False,False,False]):
      exit_text = "None"
    for dirkey in list(dirs.keys()):
      if(self.exits[dirkey] is not False):
        exit_text += "{}: {}\n".format(dirs[dirkey],worldMap[str(self.exits[dirkey])].name)
    return exit_text
  def set_exits(self, exits):
    self.exits = exits
  def get_event_list(self):
    elist = self.events.keys()
    return elist
  def describe(self):
    #cls()
    print("Area: "+self.area+"\n")
    area_desc = self.description
    if(self.state !=0 and self.states):
      area_desc += "\n"+self.states[self.state]+"\n"
    
    print(area_desc)#, title=self.name)
    exits = self.show_exits()
    print("\nExits:\n{}".format(exits))
    time.sleep(0.33)
  def set_state(self, state):
    self.state = state
  def handle_npc(self, player):
    npc = npcList[self.npc]
    if(npc.state == 0):
      print(npc.desc)
      print("Quest acquired!")
      player.give_quest(npc.quest_type,npc.required[0])
      npc.set_state(1) # quest accepted
    elif(npc.state == 1):
      print(npc.states[1]) # quest in progress
      if(npc.quest_type == "monster" and player.kills[npc.required[0]] >= npc.required[1]):
        print("You killed enough!")
        player.remove_quest(npc.quest_type,npc.required[0])
        npc.set_state(2)
      elif(npc.quest_type == "item" and gameItems[npc.required[0]] in player.items):
        print("You have enough items!")
        player.remove_quest(npc.quest_type,npc.required[0])
        player.remove_items(npc.required[0])
        npc.set_state(2)
    elif(npc.state == 2):
      print(npc.states[2]) # quest complete
    
    
    

class NPC:
    def __init__(self, name="",location="",path="",desc="",quest_type="",required=[],state=0,states={}, **kwargs):
        self.name = name
        self.location = location
        self.path = path
        self.path_tick = 0 #inc ...
        self.desc = desc
        self.quest_type = quest_type # monster/item
        self.required = required #["name", 5]
        self.state = state
        self.states = states
    def set_state(self,state):
        self.state = state
    def tick(self):
        if(self.path is not False):
            self.path_tick += 1
            if(self.path_tick > len(self.path)-1):
                self.path.reverse()
                self.path_tick = 0
            worldMap[self.location].npc = ""
            print("npc moving from {} to {}".format(self.location, self.path[self.path_tick]))
            self.location = self.path[self.path_tick]
            worldMap[self.location].npc = self.name.lower()
  


npcList = {
  "momo" : NPC(
    name="Momo",
    location="start4",
    path = ["start4", "start5", "start6"],
    desc = "Momo needs 3 mice!",
    quest_type = "monster",
    required = ["mouse", 1],
    states = {
      1 : "Have you got those mice yet?",
      2 : "Momo likes those mice!"
    }
  )
}    
    


worldMap = {
  "dummy" : Room(
    room_id="dummy",
    name="Debug room",
    area="Secret",
    description="Testing purposes only",
    exits=["start4","start4","start4","start4"]
  ),
  "start1" : Room(
    room_id="start1",
    name="Hunting Patch",
    area="Outskirts",
    description="Seems to be a popular spot for local cats to hunt.  A tall fence blocks your passage to the south. There's a big stick blocking the trail to the north.",
    exits=[False,"start2",False,False],
    enemies=["bird", "mouse", "squirrel"],
    random_battle=True,
    states={
      1:"Seems to be a popular spot for local cats to hunt.  A tall fence blocks your passage to the south. Your fallen foe, the stick, lies to the north."
    },
    events = {
      "stick" : Event(
        reqs={ 
          "stat" : "ferocity", 
          "value" : 3, 
          "trigger" : "hit" 
        },
        descs={ "sniff": "The stick smells sticky.", "look" : "A strong cat could hit this stick away!", "hit" : "You hit the stick with all your cat strength, but it's not enough." },
        trigger_text="You swipe at the stick and it clatters to the ground, startling you, but revealing a path to the north.", 
        remove_self=True,
        on_trigger=[["room", "set_exits", ["dummy","start2",False,False]], ["room", "set_state", 1]],
        e_type="text"
      )
    }
  ),
  "start2" : Room(
    room_id="start2",
    name="Sidewalk",
    area="Outskirts",
    description="A grassy sidewalk next to the road.  A tall fence blocks your path to the south.  The road seems crossable, if you're careful.",
    exits=[False, "start3", False, "start1"],
    enemies=["bird", "mouse"],
    random_battle=True,
    states = {
      1:"A grassy sidewalk next to the road.  A tall fence blocks your path to the south.  The road is easy to cross now that you know the ropes."
    },
    events={
      "road" : Event(
        reqs={ 
          "stat" : "acrobatics", 
          "value" : 3, 
          "trigger" : "look" 
        },
        descs={ "sniff": "The road doesn't smell like anything.", "look" : "The first step is looking, but you're not fast enough." },
        trigger_text="You naughtily dash across the street! There's a way north here!", 
        remove_self=True,
        on_trigger=[["room", "set_exits", ["dummy",False,"start3","start1"]], ["room", "set_state", 1]],
        e_type="text"
      )
    }
  ),
  "start3" : Room(
    room_id="start3",
    name="Small Woods",
    area="Outskirts",
    description="A small but dense group of trees. Lots of places to scratch and hide! There's a small trail here, maybe worth your interest.",
    exits=[False, False, "start6", "start2"],
    enemies=["squirrel"],
    random_battle=True,
    states = {
      1:"A small but dense group of trees. Lots of places to scratch and hide! You uncovered a trail to the north."
    },
    events={
      "trail" : Event(
        reqs={ 
          "stat" : "curiosity", 
          "value" : 3, 
          "trigger" : "sniff" 
        },
        descs={ "sniff": "You don't recognize the smell", "look" : "Looks like a trail made by other cats." },
        trigger_text="The trail smells like treats!  You follow your nose and find a way through the trail to the north!", 
        remove_self=True,
        on_trigger=[["room", "set_exits", ["dummy",False,"start6","start2"]], ["room", "set_state", 1]],
        e_type="text"
      ),
      "tree" : Event(
        reqs={
          "stat" : "acrobatics",
          "value" : 4,
          "trigger" : "climb"
        },
        descs={ "sniff" : "Something smells funny up one of these trees.", "look": "You see something up top one of the trees.", "hit":"You test your claws against the tree! Nothing happens.", "climb":"You can't seem to climb high enough, yet." },
        trigger_text="You scramble up the tree and find a stash of catnip!  You get the zoomies!",
        remove_self=True,
        on_trigger=[["player","apply_item",gameItems["zoomy"]]]
      )
    }
  ),
  "start4" : Room(
    #starting room
    room_id="start4",
    name="Your Yard",
    area="Outskirts",
    description="This is the yard you've known most of your life. There's nothing new or interesting here. All the mice have been hunted to extinction. It's time to venture out and seek new friends in the neighborhood! A tall fence blocks your way to the north.",
    exits=[False, "start5", False, False],
    random_battle=False,
    npc="momo"
  ),
  "start5" : Room(
    room_id="start5",
    name="Mouse Field",
    area="Outskirts",
    description="A tall fence blocks your way to the north. Most of the mice from your yard have retreated to here.",
    exits=[False, "start6", False, "start4"],
    enemies=["mouse"],
    random_battle=True
  ),
  "start6" : Room(
    room_id="start6",
    name="Parking Lot",
    area="Outskirts",
    description="A small parking lot where the more unsavory street cats like to meet up.  Be careful hunting on their turf!",
    exits=["start3", False, False, "start5"],
    enemies=["bird", "squirrel", "mouse", "streetcat"],
    random_battle=True
  ),
  "treeh" : Room(
    room_id="treeh",
    name="Treehouse",
    area="Secret",
    description="A secret treehouse!",
    exits=[False,False,False,False]
  ),
  "fyard1" : Room(
    room_id="fyard1",
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
        on_trigger=[["room", "set_state", 0]],
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
        on_trigger=[["room", "set_state", 2]],
        e_type="text"
      ),
      "tree" : Event(
        reqs={
          "stat" : "acrobatics",
          "value" : 10,
          "trigger" : "climb"
        },
        descs={ "look" : "You could climb this tree if you were a little more acrobatic.", "sniff" : "Smells like a cat has climbed this recently." },
        trigger_text="You climb the tree with ease",
        remove_self=False,
        on_trigger=["player", "enter", "treeh"]
      )
    }
  ),
  "driveway" : Room(
    room_id="driveway",
    name="Momo's Hangout (Driveway)",
    area="Front Yard",
    description="This is Momo's zone",
    exits=["porch1", False, False, "fyard1"]
  ),
  "porch1" : Room(
    room_id="porch1",
    name="Secretive Porch",
    area="House (Outside)",
    description="A nice hiding spot",
    exits=["house1", False, False, "fyard1"]
  ),
  "house1" : Room(
    room_id="house1",
    name="Food cave",
    area="House (Inside)",
    description="This where the food is",
    exits=[False,False,"porch1",False]
  )
}



