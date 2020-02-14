import time


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


class Room:
    def __init__(self, room_id='', name='', area='', description='', room_type='',
                 enemies=[], items=[], exits=[],
                 random_battle=False, state=0, states={}, events=False, npc="", **kwargs):
        self.room_type = room_type
        self.id = room_id
        self.name = name
        self.area = area
        self.description = description  # evergreen description
        self.states = states  # list of states
        self.state = state  # which state is the room in
        self.items = items  # list of obtainable items (using get verb)
        self.events = events
        self.enemies = enemies  # maybe...
        self.exits = exits  # which exits does this room have
        self.random_battle = random_battle
        self.npc = npc

    def show_exits(self, worldMap):  # pass worldmap here probably...
        exit_text = ""
        dirs = {0: "North", 1: "East", 2: "South", 3: "West"}
        if(self.exits == [False, False, False, False]):
            exit_text = "None"
        for dirkey in list(dirs.keys()):
            if(self.exits[dirkey] is not False):
                exit_text += "{}: {}\n".format(dirs[dirkey],
                                               worldMap[str(self.exits[dirkey])].name)
        return exit_text

    def set_exits(self, exits):
        self.exits = exits

    def get_event_list(self):
        elist = []
        if(self.events != False):
            elist = self.events.keys()
        return elist

    def describe(self, worldMap, npcList, player):
        # cls()
        area_desc = self.description
        if(self.events):
            for event in self.events:
                area_desc += " {}".format(self.events[event].desc)
        if(self.state != 0 and self.states):
            area_desc = self.states[self.state]
        if(self.npc != ""):
            area_desc += "\n\n"+COLORS.BOLD + \
                npcList[self.npc].desc+COLORS.END+"\n"
        # if(player.curiosity >= 6):
        #     for i in self.get_event_list():
        #         # i == tree, eg
        #         keyword = "{}{}{}".format(COLORS.BOLD, i, COLORS.END)
        #         area_desc = area_desc.replace(i, keyword)
        # print(area_desc)  # , title=self.name)
        #exits = self.show_exits(worldMap)
        # print("\nExits:\n{}".format(exits))
        # time.sleep(0.33)
        return {"desc": area_desc, "title": self.name, "exits": self.exits, "npc": self.npc, "area": self.area, "room_id": self.id}

    def set_state(self, state):
        self.state = state

    def handle_npc(self, player, npcList, gameItems):
        npc = npcList[self.npc]
        if(npc.state == 0):
            print(npc.states[0])
            print("Quest acquired!")
            player.give_quest(npc.quest_type, npc.required[0])
            npc.set_state(1)  # quest accepted
        elif(npc.state == 1):
            if(npc.quest_type == "monster" and player.kills[npc.required[0]] >= npc.required[1]):
                print("DEBUG: You killed enough!")
                player.remove_quest(npc.quest_type, npc.required[0])
                npc.set_state(2)
            elif(npc.quest_type == "item" and gameItems[npc.required[0]] in player.items):
                print("DEBUG: You have enough items for this quest!")
                player.remove_quest(npc.quest_type, npc.required[0])
                player.remove_items([gameItems[npc.required[0]]])
                print(npc.thanks)
                npc.set_state(2)
            else:
                print(npc.states[1])  # quest in progress
        elif(npc.state == 2):
            print(npc.states[2])  # quest complete
