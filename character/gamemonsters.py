from .movelist import moveList

gameMonsters = {
  "bird" : {
    "name" : "Bird",
    "moves" : [moveList["peck"],moveList["swoop"]],
    "hp" : 20,
    "xp_given" : 1
  },
  "squirrel" : {
    "name" : "Squirrel",
    "moves" : [moveList["bite"],moveList["claw"]],
    "hp" : 12,
    "xp_given" : 2
  },
  "mouse" : {
    "name" : "Mouse",
    "moves" : [moveList["nibble"],moveList["squeak"]],
    "hp" : 5,
    "xp_given" : 1
  },
  "streetcat" : {
    "name" : "Streetcat",
    "moves" : [moveList["bite"],moveList["claw"],moveList["kick"]],
    "hp" : 15,
    "xp_given" : 3
  },
  "child" : {
    "name" : "Human Child",
    "moves" : [moveList["backrub"],moveList["tailgrab"]],
    "hp" : 20,
    "xp_given" : 5
  }
  
}
mlist = gameMonsters.keys()