import time
# from . import worldmap
# worldMap = worldmap.worldMap


class Event:
    def __init__(self, reqs={}, desc="", descs={}, trigger_text="", remove_self=False, on_trigger=[], e_type="", **kwargs):
        self.reqs = reqs
        self.desc = desc
        self.descriptions = descs
        self.trigger_text = trigger_text
        self.remove_self = remove_self
        self.on_trigger = on_trigger
        self.e_type = e_type

    def fire(self, noun, verb, player, worldMap):
        print("\nDebug: Required {}: {} - Yours is {}\nTriggered on {}\n".format(
            self.reqs["stat"],
            self.reqs["value"],
            getattr(player, self.reqs["stat"]),
            self.reqs["trigger"]
        ))
        player_location = player.location
        if((getattr(player, self.reqs["stat"]) >= self.reqs["value"]) and (verb == self.reqs["trigger"])):
            print(self.trigger_text+"\n")
            time.sleep(0.4)
            print("\n")
            time.sleep(0.2)
            if(self.on_trigger):
                for i in self.on_trigger:
                    trigger = i
                    obj = trigger[0]
                    method = trigger[1]
                    value = trigger[2]
                    if(len(trigger) > 3):
                        _room_id = trigger[3]
                    else:
                        _room_id = False
                    if(obj == "room"):
                        # call = function of Room
                        if(_room_id):
                            call = getattr(worldMap[_room_id], method)
                        else:
                            call = getattr(worldMap[player.location], method)
                    if(obj == "player"):
                        # call = function of player
                        call = getattr(player, method)
                    time.sleep(2)
                    call(value)  # def need some error handling here
                if(self.remove_self):
                    worldMap[player_location].events.pop(noun)
        elif(verb in self.descriptions.keys() and self.descriptions[verb] != ""):
            print(self.descriptions[verb])
        else:
            print("You can't do that here.")
