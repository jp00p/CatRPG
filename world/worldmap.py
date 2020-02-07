from . import room
from . import event

worldMap = {
  "dummy" : room.Room(
    room_id="dummy",
    name="Debug room",
    area="Secret",
    description="Testing purposes only",
    exits=["start4","start4","start4","start4"]
  ),
  "start1" : room.Room(
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
      "stick" : event.Event(
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
  "start2" : room.Room(
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
      "road" : event.Event(
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
  "start3" : room.Room(
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
      "trail" : event.Event(
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
      "tree" : event.Event(
        reqs={
          "stat" : "acrobatics",
          "value" : 4,
          "trigger" : "climb"
        },
        descs={ "sniff" : "Something smells funny up one of these trees.", "look": "You see something up top one of the trees.", "hit":"You test your claws against the tree! Nothing happens.", "climb":"You can't seem to climb high enough, yet." },
        trigger_text="You scramble up the tree and find a stash of catnip!  You get the zoomies!",
        remove_self=True,
        on_trigger=[["player","apply_item","zoomy"]]
      )
    }
  ),
  "start4" : room.Room(
    #starting room
    room_id="start4",
    name="Your Yard",
    area="Outskirts",
    description="This is the yard you've known most of your life. There's nothing new or interesting here. All the mice have been hunted to extinction.\nIt's time to venture out and seek new friends in the neighborhood! A tall fence blocks your way to the north.",
    exits=[False, "start5", False, False],
    random_battle=False
  ),
  "start5" : room.Room(
    room_id="start5",
    name="Mouse Field",
    area="Outskirts",
    description="A tall fence blocks your way to the north. Most of the mice from your yard have retreated to here.",
    exits=[False, "start6", False, "start4"],
    enemies=["mouse"],
    random_battle=True
  ),
  "start6" : room.Room(
    room_id="start6",
    name="Parking Lot",
    area="Outskirts",
    description="A small parking lot where the more unsavory street cats like to meet up.  Be careful hunting on their turf, you might run into one!",
    exits=["start3", False, False, "start5"],
    enemies=["squirrel", "mouse", "streetcat"],
    random_battle=True
  ),
  "fyard1" : room.Room(
    room_id="fyard1",
    name="Big Tree Zone",
    area="Front Yard of Momo's House",
    description="Right in front of the house, there's a big, tall tree.  Birds and squirrels scurry around the area.",
    items=[],
    exits=["dummy","fyard2","dummy",False],
    enemies=["bird", "squirrel"],
    random_battle=True,
    events={
      "tree" : event.Event(
        reqs={ 
          "stat" : "acrobatics", 
          "value": 10, 
          "trigger":"climb" 
        },
        descs={ "look": "The tree goes up past the roof!", "sniff" : "You can smell the faint scent of a cat that's run up the tree recently.", "climb":"You try to find a good spot to jump but aren't acrobatic enough yet." },
        trigger_text="You scramble up the tree and climb up to the roof!", 
        remove_self=False,
        on_trigger=[["player", "enter", "roof1"]],
        e_type="text"
      )
    }
  ),
  "fyard2" : room.Room(
    id="fyard2",
    name="Sunny Resting Spot",
    area="Front Yard of Momo's House",
    description="A sunny and relaxing spot, with no wild creatures around to disturb you.  There's a big soft bed, just for cats, laying in the middle of a sunbeam.",
    exits=["dummy", False, "dummy", "fyard1"],
    random_battle = False,
    events={
      "bed" : event.Event(
        reqs={
          "stat" : "acrobatics",
          "value" : 0,
          "trigger" : "lay"
        },
        descs={ "look": "Looks like a warm and cozy spot to lay down.", "sniff" : "Smells like a bunch of other cats.  Probably safe to lay on." },
        trigger_text = "You get cozy on the bed and curl up.  It makes you sleepy!",
        remove_self=False,
        on_trigger=[["player", "apply_item", "sleepy"]]
      )
    }
  ),
  "fyard3" : room.Room(
    id="fyard3",
    name="House Cat Hunting Grounds",
    desc="A popular place for the local house cats to come out and hunt. The cats probably won't mind you hunting on their turf, but the critters around here are experienced veterans.",
    exits=["fyard2", False, "start1", "fyard"],
    random_battle = True,
    enemies=["bunny", "snake"]
  ),
  "roof1" : room.Room(
    room_id = "roof1",
    name="Front of roof",
    area="Rooftop",
    description="It's really high up!",
    exits=["dummy", False, False, False],
    random_battle = False,
    events={
      "tree" : event.Event(
        reqs = {
          "stat" : "acrobatics",
          "value" : 1,
          "trigger" : "climb"
        },
        descs={"look":"You can climb back down the tree if you want."},
        trigger_text="You climb down the tree",
        remove_self=False,
        on_trigger=[["player", "enter", "fyard1"]]
      )
    }
  ),
  "driveway" : room.Room(
    room_id="driveway",
    name="Momo's Hangout (Driveway)",
    area="Front Yard",
    description="This is Momo's zone",
    exits=["porch1", False, False, "fyard1"]
  ),
  "porch1" : room.Room(
    room_id="porch1",
    name="Secretive Porch",
    area="House (Outside)",
    description="A nice hiding spot",
    exits=["house1", False, False, "fyard1"]
  ),
  "house1" : room.Room(
    room_id="house1",
    name="Food cave",
    area="House (Inside)",
    description="This where the food is",
    exits=[False,False,"porch1",False]
  )
}



