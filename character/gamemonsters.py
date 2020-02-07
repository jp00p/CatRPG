gameMonsters = {
  "bird" : {
    "name" : "Bird",
    "moves" :["peck","swoop"],
    "hp" : 6,
    "xp_given" : 1,
    "drop" : False
  },
  "squirrel" : {
    "name" : "Squirrel",
    "moves" :["bite","claw"],
    "hp" : 8,
    "xp_given" : 1,
    "drop" : False
  },
  "angry_squirrel" : {
    "name" : "Angry Squirrel",
    "moves" :["bite","claw","pounce"],
    "hp" : 12,
    "xp_given" : 2,
    "drop" : False
  },
  "mouse" : {
    "name" : "Mouse",
    "moves" :["nibble","squeak"],
    "hp" : 5,
    "xp_given" : 1,
    "drop" : False
  },
  "rabbit" : {
    "name" : "Bunny",
    "moves" :["bunny"],
    "hp" : 9,
    "xp_given" : 2,
    "drop" : ["bunny ears", 45]
  },
  "snake" : {
    "name" : "Snake",
    "moves" :["slither","hiss"],
    "hp" : 15,
    "xp_given" : 3,
    "drop" : ["snake hat", 30]
  },
  "streetcat" : {
    "name" : "Streetcat",
    "moves" :["bite","claw","kick"],
    "hp" : 15,
    "xp_given" : 3,
    "drop" : ["cat ears", 10]
  },
  "child" : {
    "name" : "Human Child",
    "moves" :["backrub","tailgrab"],
    "hp" : 20,
    "xp_given" : 5,
    "drop" : False
  }
  
}
mlist = gameMonsters.keys()