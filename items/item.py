class Item():
  def __init__(self, name="",fer=0,acr=0,cur=0,max_hp=0,item_type="",move=False, **kwargs):
    self.name = name
    self.fer = fer
    self.acr = acr
    self.cur = cur
    self.max_hp = max_hp
    self.item_type = item_type
    self.move = move