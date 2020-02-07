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
  )
}    
    