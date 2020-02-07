import time
# from . import worldmap
# worldMap = worldmap.worldMap

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
          if(obj == "room"):
            call = getattr(worldMap[player.location],method) # call = function of Room
          if(obj == "player"):
            call = getattr(player,method) # call = function of player
          call(value) # def need some error handling here
        if(self.remove_self):
          worldMap[player.location].events.pop(noun)
    elif(self.descriptions[verb] != False):
      print(self.descriptions[verb])