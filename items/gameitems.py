from random import randint
from . import item

gameItems = {
  "grumpy" :      item.Item("Grumpy", 5,0,0,0, item_type="attitude"),
  "zoomy" :       item.Item("Zoomy", 0,5,0,0, item_type="attitude"),
  "inquisitive" : item.Item("Inquisitive", 0,0,5,0, item_type="attitude"),
  "sleepy" :      item.Item("Sleepy", -1,-2,-1,0, item_type="attitude"),
  "top hat" :      item.Item("Top Hat", 3,3,3,15, item_type="hat"),
  "bunny ears"  : item.Item("Bunny Ears", 0,0,10,0, item_type="hat", move="bunny"),
  "cat ears" : item.Item("Cat Ears", 5,5,5,15, item_type="hat"),
  "snake hat" : item.Item("Snake Hat", 5,0,0,15, item_type="hat", move="hiss"),
  "gogurt" : item.Item("Gogurt", 0,0,0,0, item_type="quest"),

  "potion" : item.Item(
    name="Potion",
    item_type="usable",
    item_effect=[["player", "give_hp", randint(5,10)]],
    use_text="You heal a little hp!"
  ),
  "gold star": item.Item(
    name="Gold Star",
    item_type="usable",
    item_effect=[["player", "level_up"]],
    use_text="You become stronger!"
  )
}