from . import npc

npcList = {
  "momo" : npc.NPC(
    name="Momo",
    location="start4",
    path = False,
    desc = "A large, plushy, tuxedo cat named Momo stands here. He looks friendly enough to talk to!",
    thanks = "Momo thanks you for the Gogurt and is now your friend.",
    quest_type = "item",
    required = ["gogurt", 1],
    states = {
      0 : "Momo asks you to find him a gogurt.  He's not sure where the humans keep them, but he wishes he knew.",
      1 : "Momo asks: Have you got that gogurt yet?",
      2 : "Momo likes that gogurt!"
    }
  ),
  "mochi" : npc.NPC(
    name="Mochi",
    location="porch",
    path=["porch", "fyard2", "fyard2", "fyard1", "fyard1", "fyard3", "fyard3", "fyard4"],
    desc="A cutie chunky tuxedo baby who likes to hang out around the front yard and the porch. He looks hungry, as usual!",
    thanks="Mochi says thank you! Then he begins searching for more food.",
    quest_type="item",
    required = ["mochifood", 5],
    states = {
      0: "Mochi is starving! He needs 5 bags of food, now! He thinks he saw some in the backyard.",
      1: "Mochi looks so hungry! He needs those bags of food.",
      2: "Mochi thanks you for the delicious food!"
    }
  ),
  "mori" : npc.NPC(
    name="Mori",
    location="basement2"
  ),
  "mika" : npc.NPC(
    name="Mika",
    location="roof",
    path=False
  ),
  "morty" : npc.NPC(
    name="Mortimer",
    location="byard1",
    desc="A weird marbled tabby baby",
    thanks="",
    quest_type="",
    required= [],
    states={
      
    },
    path=["byard1","byard5","byard6","byard2","byard3","byard7","byard8","byard4"]
  ),
  "dorian" : npc.NPC(
    name="Dorian",
    location="house1",
    path=["house1","house2","house3","house4"]
  ),
  "moreau" : npc.NPC(
    name="Moreau",
    location="alley1",
    path=False
  )
}    
    