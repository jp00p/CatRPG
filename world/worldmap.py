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


# some common events
potion = event.Event(
    reqs={
        "stat": "acrobatics",  # doesnt matter which stat
        "value": 0,  # free thing
        "trigger": "take"
    },
    descs={"look": "Looks like a potion?", 
           "sniff": "Smells healthy!",
           "hit": "That's not how you take things!"},
    trigger_text="You take the potion.",
    remove_self=True,
    on_trigger=[["player", "give_items", ["potion"]]]
)


worldMap = {
    "dummy": room.Room(
        room_id="dummy",
        name="Debug room",
        area="Secret",
        description="Testing purposes only",
        exits=["start4", "start4", "start4", "start4"]
    ),

    "start1": room.Room(
        room_id="start1",
        name="Hunting Patch",
        area="Outskirts",
        description="Seems to be a popular spot for local cats to hunt.  A tall fence blocks your passage to the south. There's a big stick blocking the trail to the north.",
        exits=[False, "start2", False, False],
        enemies=["bird", "mouse", "squirrel"],
        random_battle=True,
        states={
            1: "Seems to be a popular spot for local cats to hunt.  A tall fence blocks your passage to the south. Your fallen foe, the stick, lies to the north."
        },
        events={
            "stick": event.Event(
                reqs={
                    "stat": "ferocity",
                    "value": 3,
                    "trigger": "hit"
                },
                descs={"sniff": "The stick smells sticky.",
                       "look": "A strong cat could hit this stick away!",
                       "take": "You can't take it!",
                       "hit": "You hit the stick with all your cat strength, but you're just not strong enough yet."},
                trigger_text="You swipe at the stick and it clatters to the ground, startling you! It also reveals a path to the north.",
                remove_self=True,
                on_trigger=[["room", "set_exits", ["fyard4", "start2", False, False]], 
                            ["room", "set_state", 1]],
                e_type="text"
            )
        }
    ),
    "start2": room.Room(
        room_id="start2",
        name="Sidewalk",
        area="Outskirts",
        description="A grassy sidewalk next to the road.  A tall fence blocks your path to the south.  The road seems crossable, if you're careful.",
        exits=[False, "start3", False, "start1"],
        enemies=["bird", "mouse"],
        random_battle=True,
        states={
            1: "A grassy sidewalk next to the road.  A tall fence blocks your path to the south.  The road is easy to cross now that you know the ropes."
        },
        events={
            "road": event.Event(
                reqs={
                    "stat": "acrobatics",
                    "value": 3,
                    "trigger": "look"
                },
                descs={"sniff": "The road doesn't smell like anything.",
                       "hit":"Hit the road Jack!",
                       "look": "The first step is looking both ways, but you're not fast enough to dash across yet."},
                trigger_text="You naughtily dash across the street! Luckily there's no cars allowed on this street.",
                remove_self=True,
                on_trigger=[["room", "set_exits", ["driveway", False, "start3", "start1"]], [
                    "room", "set_state", 1], ["player", "enter", "driveway"]],
                e_type="text"
            )
        }
    ),
    "start3": room.Room(
        room_id="start3",
        name="Small Woods",
        area="Outskirts",
        description="A small but dense group of trees. Lots of places to scratch and hide! There's a small trail here, maybe worth your interest.",
        exits=[False, False, "start6", "start2"],
        enemies=["squirrel"],
        random_battle=True,
        states={
            1: "A small but dense group of trees. Lots of places to scratch and hide! You uncovered a trail to the north."
        },
        events={
            "trail": event.Event(
                reqs={
                    "stat": "curiosity",
                    "value": 3,
                    "trigger": "sniff"
                },
                descs={"sniff": "You don't recognize the smell",
                       "look": "Looks like a trail made by other cats."},
                trigger_text="The trail smells like treats!  You follow your nose and find a way through the trail to the north!",
                remove_self=True,
                on_trigger=[["room", "set_exits", ["nyard1", False,
                                                   "start6", "start2"]], ["room", "set_state", 1]],
                e_type="text"
            ),
            "tree": event.Event(
                reqs={
                    "stat": "acrobatics",
                    "value": 4,
                    "trigger": "climb"
                },
                descs={"sniff": "Something smells funny up one of these trees.",
                       "look": "You see something up top one of the trees.",
                       "hit": "You test your claws against the tree! Nothing happens.",
                       "climb": "You can't seem to climb high enough, yet."},
                trigger_text="You scramble up the tree and find a stash of catnip!  You get the zoomies!",
                remove_self=True,
                on_trigger=[["player", "apply_item", "zoomy"]]
            )
        }
    ),
    "start4": room.Room(
        # starting room
        room_id="start4",
        name="Your Yard",
        area="Outskirts",
        npc="momo",
        description="This is the yard you've known most of your life, right outside your home. There's nothing new or interesting here. All the mice have been hunted to extinction.\nIt's time to venture out and seek new friends in the neighborhood!",
        exits=[False, "start5", False, False],
        random_battle=False,
        events={
            "home": event.Event(
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
        random_battle=True
    ),
    "start6": room.Room(
        room_id="start6",
        name="Parking Lot",
        area="Outskirts",
        description="A small parking lot near a neighborhood shop. This is where the more rough and tumble street cats like to meet up.  Be careful hunting on their turf, you might run into one!  There's a dumpster behind the shop ",
        exits=["start3", False, False, "start5"],
        enemies=["squirrel", "mouse", "streetcat"],
        random_battle=True,
        states= {
            1: "A small parking lot near a neighborhood shop. This is where the more rough and tumble street cats like to meet up.  Be careful hunting on their turf, you might run into one!"
        },
        events={
            "dumpster": event.Event(
                reqs={
                    "stat" : "acrobatics",
                    "value" : 5,
                    "trigger" : "look"
                },
                descs={"look": "It's too hard for you to balance on the edge to look inside!",
                       "sniff": "Smells like garbage! And fish..."},
                trigger_text="You balance on the edge and look inside... you find a tuna fish!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["tuna"]],
                            ["room", "set_state", 1]]
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
                reqs={
                    "stat": "acrobatics",
                    "value": 10,
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
        description="A sunny and relaxing spot, with no wild creatures around to disturb you.  There's a big soft bed, just for cats, laying in the middle of a sunbeam.",
        exits=["porch", "driveway", "fyard4", "fyard1"],
        random_battle=False,
        events={
            "bed": event.Event(
                reqs={
                    "stat": "acrobatics",
                    "value": 0,  # trap!
                    "trigger": "lay"
                },
                descs={"look": "Looks like a warm and cozy spot to lay down.",
                       "sniff": "Smells like a bunch of other cats.  Probably safe to lay upon."},
                trigger_text="You get cozy on the bed and curl up.  It makes you sleepy!  Too sleepy.",
                remove_self=False,
                on_trigger=[["player", "apply_item", "sleepy"]]
            )
        }
    ),
    "fyard3": room.Room(
        room_id="fyard3",
        name="Mushroom Circle",
        description="A circle of colorful mushrooms in the corner of the yard. There's some red, blue, and green mushrooms mixed in.",
        area="Front Yard",
        exits=["fyard1", "fyard4", False, False],
        events={
            "mushroom":event.Event(
                reqs={
                    "stat":"acrobatics",
                    "value":999,
                    "trigger":"look"
                },
                descs={"sniff":"Which mushroom are you trying to sniff?", "look":"Which mushroom are you looking at?"},
                trigger_text="",
                remove_self=False
            ),
            "mushrooms":event.Event(
                reqs={
                    "stat":"acrobatics",
                    "value":999,
                    "trigger":"look"
                },
                descs={"sniff":"Which mushroom are you trying to sniff?", "look":"Which mushroom are you looking at?"},
                trigger_text="",
                remove_self=False
            ),
            "red mushroom":event.Event(
                reqs={
                    "stat":"curiosity",
                    "value":11,
                    "trigger":"sniff"
                },
                descs={"sniff":"Smells mysterious...", "look":"It's covered in a fine shiny red powder.", "hit":"The mushroom is too delicate for that!"},
                trigger_text="Sniffing the mushroom makes you feel stronger! You sniff it until the mushroom falls apart.",
                remove_self=True,
                on_trigger=[["player", "add_stat", ["fer", 3]]]
            ),
            "green mushroom":event.Event(
                reqs={
                    "stat":"ferocity",
                    "value":6,
                    "trigger":"hit"
                },
                descs={"sniff":"Smells healthy!", "hit":"You hit the mushroom and hear something rattling inside. Hit it harder!", "look":"This mushroom looks like its full of something..."},
                trigger_text="You hit the mushroom as hard as you can and a bunch of potions spill out!",
                remove_self=True,
                on_trigger=[["player", "give_items", ["potion","potion","potion"]]]
            ),
            "blue mushroom":event.Event(
                reqs={
                    "stat":"acrobatics",
                    "value":8,
                    "trigger":"climb"
                },
                descs={
                    "sniff":"This tall mushroom smells very mushroomy",
                    "look":"This mushroom is super tall! You can't see on top of it",
                    "climb":"You don't have the skills to climb this mushroom... yet"
                },
                trigger_text="You climb up the slimy blue mushroom and find a Mushroom Hat on top!",
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
    "roof1": room.Room(
        room_id="roof1",
        name="Front of roof",
        area="Rooftop",
        description="It's really high up!",
        exits=["dummy", False, False, False],
        random_battle=False,
        events={
            "tree": event.Event(
                reqs={
                    "stat": "acrobatics",
                    "value": 1,
                    "trigger": "climb"
                },
                descs={"look": "You can climb back down the tree if you want."},
                trigger_text="You climb down the tree",
                remove_self=False,
                on_trigger=[["player", "enter", "fyard1"]]
            )
        }
    ),
    "driveway": room.Room(
        room_id="driveway",
        name="Driveway",
        area="Front Yard",
        description="The driveway acts as a central hub for most of the cats that live around here. It's safe, quiet, and leads to a lot of different areas.",
        # set south exit when start2 is done
        exits=["dummy", False, "start2", "fyard1"]
    ),
    "porch": room.Room(
        room_id="porch",
        name="Porch",
        area="House (Outside)",
        description="Where most adventures begin for the local cats. A good place for scouting, surveying, and hiding.",
        exits=["house3", False, "fyard1", False],
        npc="mochi"
    ),
    "house1": room.Room(
        room_id="house1",
        name="Utility Room",
        area="House (Inside)",
        description="This room has some heavy duty litter boxes in it.",
        exits=[False, "house2", "house3", False]  # opens north to backyard6
    ),
    "house2": room.Room(
        room_id="house2",
        name="Bedroom",
        area="House (Inside)",
        description="Big bed",
        exits=[False, False, "house4", "house1"]
    ),
    "house3": room.Room(
        room_id="house3",
        name="Living Room",
        area="House (Inside)",
        description="Cat tower kingdom",
        exits=["house1", "house4", "porch", False]
    ),
    "house4": room.Room(
        room_id="house4",
        name="Kitchen",
        area="House (Inside)",
        description="This is where the cat food is! There are stairs leading down into darkness...",
        exits=["house2", False, False, "house3"]
    ),
    "nyard1": room.Room(
        room_id="nyard1",
        name="Untamed Jungle",
        area="Neighbor's Yard",
        description="This place is almost a literal jungle! There are huge trees with vines hanging down, and bats squeaking overhead.",
        events={
            "vine": event.Event(
                reqs={
                    "stat": "acrobatics",
                    "value": 8,
                    "trigger": "hit"
                },
                descs={"look": "You can see something hanging from a vine.",
                       "sniff": "The vines smell like bats!",
                       "hit": "You try to hit the vine but you can't jump high enough yet."},
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
        description="Lush, green and full of snails and frogs. There's a large pond here which you probably don't want to get into.",
        exits=[False, False, False, "nyard1"],
        enemies=["fish", "snake", "bird"],
        random_battle=True,
        events={
            "pond": event.Event(
                reqs={
                    "stat": "curiosity",
                    "value": 10,
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
    )
}
