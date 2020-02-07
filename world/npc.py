# import world

# worldMap = world.worldmap.worldMap

class NPC:
    def __init__(self, name="",location="",path="",desc="",quest_type="",thanks="",required=[],state=0,states={}, **kwargs):
        self.name = name
        self.location = location
        self.path = path
        self.path_tick = 0 #inc ...
        self.desc = desc
        self.quest_type = quest_type # monster/item
        self.required = required #["name", 5]
        self.thanks = thanks
        self.state = state
        self.states = states
        # states:
        # 0 - hasn't been talked to yet
        # 1 - quest given
        # 2 - quest accepted
        # 3 - quest complete
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