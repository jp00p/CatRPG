class Item():
  def __init__(self, name="",fer=0,acr=0,cur=0,max_hp=0,item_type="",move=False, use_text="", item_effect=False, **kwargs):
    self.name = name
    self.fer = fer
    self.acr = acr
    self.cur = cur
    self.max_hp = max_hp
    self.item_type = item_type
    self.move = move
    self.use_text = use_text
    self.item_effect = item_effect
  def use(self, player, worldMap):
      if(self.item_effect):
        for i in self.item_effect:
          trigger = i
          obj = trigger[0]
          method = trigger[1]
          
          if(obj == "room"):
            call = getattr(worldMap[player.location],method)
          if(obj == "player"):
            call = getattr(player,method)

          if(len(trigger) == 3):
            call(trigger[2])
          else:
            call()
          
