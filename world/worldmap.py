from . import room
from . import event


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


class AREA_DIFFICULTY:
    START = 3
    FYARD = 5
    NYARD = 7
    HOUSE = 9
    BYARD = 11
    ALLEY = 15


# Faucet
# Dog
# Hair Tie
# Cat tower
# possum
# blanket monster (hand under a blanket)
# boxes
# bushes
# spiders

worldMap = {
    "dummy": room.Room(
        room_id="dummy",
        name="Debug room",
        area="Secret",
        description="Testing purposes only",
        exits=["start4", "start4", "start4", "start4"],
        enemies=["mouse"],
        battle_enter=True
    ),

    "start1": room.Room(
        room_id="start1",
        name="Wooded Path",
        area="Outskirts",
        description="A small trail in the woods. ",
        exits=[False, "start2", False, False],
        enemies=["bird", "mouse", "squirrel"],
        random_battle=True,
        events={
            "stick": event.Event(
                desc="There's a big stick blocking the trail to the north.",
                reqs={
                    "stat": "ferocity",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "hit"
                },
                descs={"sniff": "The stick smells sticky.",
                       "look": "A strong cat could hit this stick away!",
                       "take": "You can't take it!",
                       "hit": "You hit the stick with all your cat strength, but you're just not strong enough yet."},
                trigger_text="You swipe at the stick and it clatters to the ground, startling you! It also reveals a path to the north.",
                remove_self=True,
                on_trigger=[["room", "set_exits", ["fyard4", "start2", False, False]],
                            ["room", "set_exits", ["fyard2", "driveway", "start1", "fyard3"], "fyard4"]],
                e_type="text"
            )
        }
    ),
    "start2": room.Room(
        room_id="start2",
        name="Sidewalk",
        area="Outskirts",
        description="A grassy sidewalk next to the road.",
        exits=[False, "start3", False, "start1"],
        enemies=["bird", "mouse"],
        random_battle=True,
        events={
            "road": event.Event(
                desc="There's a road to the north that you could cross if you look carefully.",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "look"
                },
                descs={"sniff": "The road doesn't smell like anything.",
                       "hit": "Hit the road Jack!",
                       "look": "The first step is looking both ways, but you're not fast enough to dash across yet."},
                trigger_text="You naughtily dash across the street! Luckily there's no cars allowed on this street.",
                remove_self=True,
                on_trigger=[["room", "set_exits", ["driveway", False, "start3", "start1"]], [
                    "player", "enter", "driveway"]],
                e_type="text"
            ),
            "grass": event.Event(
                desc="You see a slightly suspicious patch of grass.",
                reqs={
                    "stat": "curiosity",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "sniff"
                },
                descs={
                    "sniff": "Smells like something... you can't quite make it out yet",
                    "look": "Looks like a discolored patch of grass",
                    "hit": "You paw the grass and disturb the grasshoppers, but nothing happens",
                },
                trigger_text="You sniff the patch of grass and realize another cat peed here! You make a stinky face",
                remove_self=True,
                on_trigger=[["player", "apply_item", "stinkyface"]]
            )
        }
    ),
    "start3": room.Room(
        room_id="start3",
        name="Small Woods",
        area="Outskirts",
        description="A small but dense group of trees. Lots of places to scratch and hide!",
        exits=[False, False, "start6", "start2"],
        enemies=["squirrel"],
        random_battle=True,
        events={
            "trail": event.Event(
                desc="There's a small trail here, maybe worth your interest.",
                reqs={
                    "stat": "curiosity",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "sniff"
                },
                descs={"sniff": "You don't recognize the smell",
                       "look": "Looks like a trail made by other cats."},
                trigger_text="The trail smells like treats!  You follow your nose and find a way through the trail to the north!",
                remove_self=True,
                on_trigger=[
                    ["room", "set_exits", ["nyard1", False, "start6", "start2"]],
                    ["room", "set_state", 1],
                    ["room", "set_exits", [False, "nyard2", "start3", "driveway"], "nyard1"]],
                e_type="text"
            ),
            "tree": event.Event(
                desc="A tree here has a scent that catches your nose.",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "climb"
                },
                descs={"sniff": "Something smells funny up in the tree's branches.",
                       "look": "You see something up top the tree.",
                       "hit": "You test your claws against the tree! Nothing happens.",
                       "climb": "You can't seem to climb high enough, yet."},
                trigger_text="You scramble up the tree and find a stash of ...batnip!?",
                remove_self=True,
                on_trigger=[["player", "give_items", ["batnip"]]]
            )
        }
    ),
    "start4": room.Room(
        # starting room
        room_id="start4",
        name="Your Yard",
        area="Outskirts",
        description="This is the yard you've known most of your life. There's nothing new or interesting here. All the mice have been hunted to extinction.\nIt's time to venture out and seek new friends in the neighborhood!",
        exits=["dummy", "start5", False, False],
        random_battle=False,
        events={
            "home": event.Event(
                desc="You can see your home in the distance.",
                reqs={
                    "stat": "curiosity",
                    "value": 0,
                    "trigger": "sniff"
                },
                descs={"look": "Home sweet home. Where the food flows freely.",
                       "paw": "You swipe the air at your house like a weirdo.",
                       "climb": "You climb to the top of your house and survey the neighborhood."},
                trigger_text="You smell the scents of home, making you feel nostalgic.",
                remove_self=False,
                on_trigger=[["player", "apply_item", "nostalgic"]]
            )
        }
    ),
    "start5": room.Room(
        room_id="start5",
        name="Mouse Field",
        area="Outskirts",
        description="A small grassy field near your house. Most of the mice from your yard have retreated to here to form a new community with what they have left.",
        exits=[False, "start6", False, "start4"],
        enemies=["mouse"],
        random_battle=True,
        events={
            "bag": event.Event(
                desc="There's a bag laying in the middle of the field.",
                reqs={
                    "stat": "ferocity",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "hit"
                },
                descs={
                    "look": "You see a plastic bag flapping in the wind.  It seems to be full of something",
                    "sniff": "The bag smells like something familiar!",
                    "hit": "You feebly paw at the bag but you aren't strong enough to flip it over",
                    "take": "You can't take the bag!"
                },
                trigger_text="You viciously paw the bag open, revealing some goodies!",
                remove_self=True,
                on_trigger=[
                    ["player", "give_items", ["catnip", "potion", "potion"]]
                ]
            ),
            "hole": event.Event(
                desc="You can see a small hole in the grass.",
                reqs={
                    "stat": "curiosity",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "look"
                },
                descs={
                    "look": "You give the hole a cursory glance but you don't feel curious enough to inspect futher.",
                    "sniff": "The hole smells a little scaly",
                    "hit": "You paw the grass around the hole to no effect",
                    "climb": "The hole is too small to climb into."
                },
                trigger_text="As you look deeper into the hole, a snake pops out!",
                remove_self=False,
                on_trigger=[
                    ["player", "battle", "snake"]
                ]
            )
        }
    ),
    "start6": room.Room(
        room_id="start6",
        name="Parking Lot",
        area="Outskirts",
        description="A small parking lot near a neighborhood shop. This is where the more rough and tumble street cats like to meet up.  Be careful hunting on their turf, you might run into one!  You can see an open dumpster behind the shop. ",
        exits=["start3", False, False, "start5"],
        enemies=["squirrel", "mouse", "streetcat"],
        random_battle=True,
        events={
            "dumpster": event.Event(
                desc="There's a dumpster with it's lid open here.",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.START,
                    "trigger": "look"
                },
                descs={"look": "It's too hard for you to balance on the edge to look inside! You're not acrobatic enough!",
                       "sniff": "Smells like garbage! And fish...",
                       "hit": "You paw makes a hollow clang against the dumpster",
                       "take": "You put the dumpster in your pocket.  Just kidding!"},
                trigger_text="You balance on the edge and look inside... you find a tuna fish!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["tuna"]]]
            )
        }
    ),
    "fyard1": room.Room(
        room_id="fyard1",
        name="Big Tree Zone",
        area="Front Yard",
        description="Right in front of the house, there's a big, tall tree. Its branches reach above the roof of the house.  Birds and squirrels scurry around the area and make angry alert sounds at your presence.",
        items=[],
        exits=[False, "fyard2", "fyard3", False],
        enemies=["bird", "squirrel"],
        random_battle=True,
        events={
            "tree": event.Event(
                desc="You think you hear meowing coming from the roof. ",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.FYARD,
                    "trigger": "climb"
                },
                descs={"look": "The tree goes up past the roof!",
                       "sniff": "You can smell the faint scent of a cat that's run up the tree recently.",
                       "climb": "You try to find a good spot to climb up but aren't quite acrobatic enough... yet."},
                trigger_text="You scramble up the tree and climb up to the roof!",
                remove_self=False,
                on_trigger=[["player", "enter", "roof1"]],
                e_type="text"
            )
        }
    ),
    "fyard2": room.Room(
        room_id="fyard2",
        name="Sunny Resting Spot",
        area="Front Yard",
        description="A sunny and relaxing spot, with no wild creatures around to disturb you.",
        exits=["porch", "driveway", "fyard4", "fyard1"],
        random_battle=False,
        events={
            "bed": event.Event(
                desc="There's a big soft bed, just for cats, laying in the middle of a sunbeam.",
                reqs={
                    "stat": "acrobatics",
                    "value": -20,  # trap!
                    "trigger": "lay"
                },
                descs={"look": "Looks like a warm and cozy spot to lay down.",
                       "sniff": "Smells like a bunch of other cats. Probably safe to lay upon."},
                trigger_text="You get cozy on the bed and curl up.  It makes you sleepy!  Too sleepy.",
                remove_self=False,
                on_trigger=[
                    ["player", "apply_item", "sleepy"],
                    ["player", "give_hp", 15]
                    ]
            )
        }
    ),
    "fyard3": room.Room(
        room_id="fyard3",
        name="Mushroom Circle",
        description="A circle of colorful mushrooms in the corner of the yard.",
        area="Front Yard",
        exits=["fyard1", "fyard4", False, False],
        random_battle=True,
        enemies=["shroom"],
        events={
            "red mushroom": event.Event(
                desc="There's a weird red mushroom inside the circle.",
                reqs={
                    "stat": "curiosity",
                    "value": AREA_DIFFICULTY.FYARD,
                    "trigger": "sniff"
                },
                descs={"sniff": "Smells mysterious...", "look": "It's covered in a fine shiny red powder.",
                       "hit": "The mushroom is too delicate for that!"},
                trigger_text="Sniffing the mushroom makes you feel stronger! You sniff it until the mushroom falls apart.",
                remove_self=True,
                on_trigger=[["player", "add_stat", ["fer", 3]]]
            ),
            "green mushroom": event.Event(
                desc="There's a bulky green mushroom standing beside the circle.",
                reqs={
                    "stat": "ferocity",
                    "value": AREA_DIFFICULTY.FYARD,
                    "trigger": "hit"
                },
                descs={"sniff": "Smells healthy!", "hit": "You hit the mushroom and hear something rattling inside. Hit it harder!",
                       "look": "This mushroom looks like its full of something..."},
                trigger_text="You hit the mushroom as hard as you can and a bunch of potions spill out!",
                remove_self=True,
                on_trigger=[["player", "give_items",
                             ["potion", "potion", "potion", "potion", "potion"]]]
            ),
            "blue mushroom": event.Event(
                desc="There's a super tall blue mushroom near the circle",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.FYARD,
                    "trigger": "climb"
                },
                descs={
                    "sniff": "This tall mushroom smells very mushroomy and tall",
                    "look": "This mushroom is super tall! You can't see on top of it",
                    "climb": "You don't have the skills to climb this mushroom... yet"
                },
                trigger_text="You climb up the slimy blue mushroom and find a Mushroom Hat on top! The mushroom crumbles underneath you as you retrieve the hat.",
                remove_self=True,
                on_trigger=[["player", "give_items", ["mushroom hat"]]]
            )
        }
    ),
    "fyard4": room.Room(
        room_id="fyard4",
        name="House Cat Hunting Grounds",
        area="Front Yard",
        description="A popular place for the local house cats to come out and hunt. The cats probably won't mind you hunting on their turf, but the prey here are pretty tough.",
        exits=["fyard2", False, "start1", "fyard3"],
        random_battle=True,
        enemies=["bunny", "snake", "child", "angry_squirrel", "angry_bird"]
    ),
    "roof2": room.Room(
        room_id="roof2",
        name="Front of Roof",
        area="Rooftop",
        description="It's really high up!",
        exits=["roof1", False, False, False],
        random_battle=False,
        events={
            "tree": event.Event(
                desc="There's tree branches you can climb down on.",
                reqs={
                    "stat": "acrobatics",
                    "value": -100,  # dont trap them on the roof
                    "trigger": "climb"
                },
                descs={"look": "You can climb back down the tree if you want."},
                trigger_text="You climb down the tree",
                remove_self=False,
                on_trigger=[["player", "enter", "fyard1"]]
            )
        }
    ),
    "roof1": room.Room(
        room_id="roof1",
        area="Rooftop",
        name="Back of Roof",
        description="Way up here, you can see over the entire back half of the neighborhood. ",
        exits=[False, False, "roof2", False],
        random_battle=False,
        npc="mika",
        events={
            "tree": event.Event(
                desc="There's tree branches you can climb down on.",
                reqs={
                    "stat": "acrobatics",
                    "value": -100,  # dont trap them on the roof
                    "trigger": "climb"
                },
                descs={"look": "You can climb down the tree if you want."},
                trigger_text="You climb down the tree",
                remove_self=False,
                on_trigger=[["player", "enter", "byard5"]]
            )
        }
    ),
    "driveway": room.Room(
        room_id="driveway",
        name="Driveway",
        area="Front Yard",
        description="The driveway acts as a central hub for most of the cats that live around here. It's safe, quiet, and leads to a lot of different areas.",
        exits=["byard1", "nyard1", "start2", "fyard1"],
        npc="momo"
    ),
    "porch": room.Room(
        room_id="porch",
        name="Porch",
        area="Front Yard",
        description="Where most adventures begin for the local Mo Family. A good place for scouting, surveying, and lounging.",
        exits=["house3", False, "fyard1", False],
        npc="mochi",
        events={
            "note": event.Event(
                desc="There's a note written in cat language here.",
                reqs={
                    "stat":"curiosity",
                    "value":AREA_DIFFICULTY.FYARD,
                    "trigger":"look"
                },
                descs={
                    "look":"Unfortunately, you aren't curious enough to have learned cat language.",
                    "hit":"You paw at the note playfully!",
                    "sniff":"The note smells like it was written with squid ink",
                    "take":"The note is firmly pinned to the wall."
                },
                trigger_text="The note reads: \"Mochi likes to hang out on the porch, and he wanders around the front yard slowly. He should be easy to find!\"",
                remove_self=False
            )
        }
    ),
    "house1": room.Room(
        room_id="house1",
        name="Utility Room",
        area="House (Inside)",
        description="This room has a bunch of weird human stuff. Some of it looks like it would be fun to destroy! The loominig presence of the vacuum can be felt in this room.",
        exits=[False, "house2", "house3", False],  # opens north to backyard6
        random_battle=True,
        enemies=["ferret", "vacuum", "dustbunny"],
        events={
            "door": event.Event(
                desc="There's a door leading outside that's just barely opened.",
                reqs={
                    "stat": "ferocity",
                    "value": AREA_DIFFICULTY.HOUSE,
                    "trigger": "hit"
                },
                descs={
                    "look": "The door is very slightly opened.  If you had the strength, you could push it open!",
                    "sniff": "The crack in the door smells like outside!",
                    "hit": "You paw at the door ineffectively. You aren't strong enough!",
                    "take": "You can't take a door."
                },
                trigger_text="You push the door open enough to squeeze through! You can get out to the backyard now!",
                remove_self=True,
                on_trigger=[
                    ["room", "set_exits", ["byard6", "house2", "house3", False]],
                    # set byard6 room's exits too
                    ["room", "set_exits", ["byard2", "byard7",
                                           "house1", "byard5"], "byard6"]
                ]
            ),
            "shelf": event.Event(
                desc="On top of a big shelf, you smell something interesting.",
                reqs={
                    "stat":"acrobatics",
                    "value":AREA_DIFFICULTY.HOUSE,
                    "trigger":"climb"
                },
                descs={
                    "look":"You can't see at the top of the big shelf",
                    "sniff":"Whatever's up there is making you feel extremely curious!",
                    "climb":"You try and fail to climb up the shelf! You aren't acrobatic enough.",
                },
                trigger_text="You launch yourself onto the shelf, only to knock it over with a loud crash! Everything falls off the shelf and breaks, and you feel proud and brave.",
                remove_self=True,
                on_trigger=[
                    ["player", "give_move", "launch"],
                    ["player", "apply_item", "brave"]
                ]
            )
        }
    ),
    "house2": room.Room(
        room_id="house2",
        name="Bedroom",
        area="House (Inside)",
        description="This is a cozy room, perfect for when you need a nap.",
        events={
            "bed": event.Event(
                desc="There's a big tall comfy bed in here.",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.HOUSE,
                    "trigger": "climb"
                },
                descs={
                    "look": "The bed is too tall to see on top of!",
                    "sniff": "You smell something on top of the bed.",
                    "take": "The bed is too big to take!",
                    "climb": "You clumsily fall off the side of the bed! You're not very acrobatic."
                },
                trigger_text="You climb up on the bed and find a portable cat scratcher!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["scratcher"]]]
            )
        },
        exits=[False, False, "house4", "house1"],
        random_battle=True,
        enemies=["ferret", "blanket"]
    ),
    "house3": room.Room(
        room_id="house3",
        name="Living Room",
        area="House (Inside)",
        description="This room is a forest of cat towers!",
        events={
            "cave": event.Event(
                desc="One of the towers has a cave, something inside is glinting in the light.",
                reqs={
                    "stat" : "curiosity",
                    "value" : AREA_DIFFICULTY.HOUSE,
                    "trigger" : "look"
                },
                descs={
                    "look":"Your fear of the dark is overpowering your curiosity to look!",
                    "sniff":"The cave smells a little fishy.",
                    "hit":"Why are you so violent?!",
                    "climb":"You can't climb in before you look inside!"
                },
                trigger_text = "You cautiously look inside the cave... There's a weird fish hat in there!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["fish hat"]]]
            ),
            "tower": event.Event(
                desc="There's something on top of a tower you can smell, and it smells good!",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.HOUSE,
                    "trigger": "climb"
                },
                descs={
                    "look": "You will need to climb up there to see it.",
                    "sniff": "Whatever's up there smells delicious.",
                    "hit": "You bat at the tower and it doesn't budge.",
                    "climb": "You aren't acrobatic enough yet to climb that high!"
                },
                trigger_text="You get to the top of the tallest tower and find a packet of Gogurt! You aren't sure how to open it so you save it for later.",
                remove_self=True,
                on_trigger=[["player", "give_items", ["gogurt"]]]
            )
        },
        exits=["house1", "house4", "porch", False],
        random_battle=True,
        enemies=["ferret", "vacuum", "dustbunny"]
    ),
    "house4": room.Room(
        room_id="house4",
        name="Kitchen",
        area="House (Inside)",
        description="This is where the cat food is! There are stairs leading down into darkness...",
        events={
          "stairs" : event.Event(
              desc="There are stairs leading down into a dark spooky basement here.",
              reqs={
                  "stat" : "ferocity",
                  "value" : AREA_DIFFICULTY.HOUSE + 1,
                  "trigger" : "climb"
              },
              descs={
                  "look" : "The bottom of the stairs is pitch black and scary.",
                  "climb" : "You are too scared to climb down the stairs! You're not very ferocious...",
                  "sniff" : "You can smell dampness and cats down there.",
                  "hit" : "You swipe at the darkness and scare yourself!"
              },
              trigger_text="You bravely climb down the stairs and go into the basement!",
              remove_self=False,
              on_trigger = [["player", "enter", "basement1"]]
          ),
          "faucet" : event.Event(
              
          )
        },
        random_battle=True,
        enemies=["vacuum", "dustbunny", "housemouse"],
        exits=["house2", False, False, "house3"]
    ),
    "nyard1": room.Room(
        room_id="nyard1",
        name="Untamed Jungle",
        area="Neighbor's Yard",
        description="This place is almost a literal jungle! There are huge trees with vines hanging down, and bats squeaking overhead.",
        events={
            "vine": event.Event(
                desc="You see a vine with something on top of it.",
                reqs={
                    "stat": "acrobatics",
                    "value": AREA_DIFFICULTY.NYARD,
                    "trigger": "hit"
                },
                descs={"look": "You can see something hanging from a vine.",
                       "sniff": "The vines smell like bats!",
                       "hit": "You try to hit the vine but you can't jump high enough yet.",
                       "climb": "The vine won't support your weight"},
                trigger_text="You do a super jump and knock a hat out of the tree!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["bat hat"]]]
            )
        },
        exits=[False, "nyard2", "start3", "driveway"],
        enemies=["bat", "snake", "squirrel"],
        random_battle=True
    ),
    "nyard2": room.Room(
        room_id="nyard2",
        name="Verdant Wetlands",
        area="Neighbor's Yard",
        description="Lush, green and full of snails and frogs.",
        exits=[False, False, False, "nyard1"],
        enemies=["fish", "snake", "bird"],
        random_battle=True,
        events={
            "pond": event.Event(
                desc="There's a large pond here. ",
                reqs={
                    "stat": "curiosity",
                    "value": AREA_DIFFICULTY.NYARD,
                    "trigger": "look"
                },
                descs={
                    "look": "You think you see something on the other side but you can't "+COLORS.UNDERLINE+"quite"+COLORS.END+" make it out",
                    "hit": "You splash the pond water!",
                    "sniff": "Smells like water!"
                },
                trigger_text="You spot something in the grass across the pond! You slip and fall into the pond and scramble out on the other side, where you only find a leaf in the wind. Now you're grumpy!",
                remove_self=False,
                on_trigger=[["player", "enter", "dummy"],
                            ["player", "apply_item", "grumpy"]]

            )
        }
    ),

    "byard1": room.Room(
        room_id="byard1",
        name="Backyard 1",
        area="Backyard",
        description="Backyard 1",
        exits=[False, "byard2", "byard5", False],
        battle_enter=True,
        enemies=["dog", "angry_squirrel"]
    ),
    "byard2": room.Room(
        room_id="byard2",
        name="Backyard 2",
        area="Backyard",
        description="Backyard 2",
        exits=[False, "byard3", "byard6", "byard1"]
    ),
    "byard3": room.Room(
        room_id="byard3",
        name="Backyard 3",
        area="Backyard",
        description="Backyard 3",
        exits=[False, "byard4", "byard7", "byard2"]
    ),
    "byard4": room.Room(
        room_id="byard4",
        name="Backyard 4",
        area="Backyard",
        description="Backyard 4",
        exits=[False, False, "byard8", "byard3"]
    ),
    "byard5": room.Room(
        room_id="byard5",
        name="Backyard 5",
        area="Backyard",
        description="Backyard 5",
        exits=["byard1", "byard6", False, False]
    ),
    "byard6": room.Room(
        room_id="byard6",
        name="Backyard 6",
        area="Backyard",
        description="Backyard 6",
        exits=["byard2", "byard7", False, "byard5"]
    ),
    "byard7": room.Room(
        room_id="byard7",
        name="Backyard 7",
        area="Backyard",
        description="Backyard 7",
        exits=["byard3", "byard8", False, "byard6"]
    ),
    "byard8": room.Room(
        room_id="byard8",
        name="Backyard 8",
        area="Backyard",
        description="Backyard 8",
        exits=["byard4", False, "driveway", "byard7"]
    ),

    "basement1": room.Room(),
    "basement2": room.Room(), # mori in here

    "alley1": room.Room(), # moreau paths here
    "alley2": room.Room(),
    "alley3": room.Room(),
    "alley4": room.Room(),
    "alley5": room.Room(),
    "alley6": room.Room(),
    "alley7": room.Room(),
    "alley8": room.Room(),
    "alley9": room.Room(),
    "alley10": room.Room(),
    "alley11": room.Room(),
    "alley12": room.Room()

}
