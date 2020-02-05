class Item():
  def __init__(self, name="",fer=0,acr=0,cur=0,max_hp=0,item_type="", **kwargs):
    self.name = name
    self.fer = fer
    self.acr = acr
    self.cur = cur
    self.max_hp = max_hp
    self.item_type = item_type

gameItems = {
  "grumpy" :      Item("Grumpy", 5,0,0,0, item_type="attitude"),
  "zoomy" :       Item("Zoomy", 0,5,0,0, item_type="attitude"),
  "inquisitive" : Item("Inquisitive", 0,0,5,0, item_type="attitude"),
  "sleepy" :      Item("Sleepy", -1,-2,-1,0, item_type="attitude"),
  "top hat" :      Item("Top Hat", 3,3,3,15, item_type="hat"),
  "bunny ears"  :      Item("Bunny Ears", 0,0,10,0, item_type="hat"),
  "cat ears" : Item("Cat Ears", 1,1,5,10, item_type="hat")
}