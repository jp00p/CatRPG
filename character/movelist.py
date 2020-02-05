from .move import Move

moveList = {
  "claw" : Move(
    name="Claw",
    verbs=['{} swipes at {} with their claws!', '{} slashes with their claws!'],
    dmg = [1,6],
    times = [0,1]
  ),
  "doubleclaw" : Move(
    name="Double Claw",
    verbs = ['{} does a super fast double-claw!'],
    dmg = [1,8],
    times = [0,4],
    hit = -2
  ),
  "bite" : Move(
    name="Bite",
    verbs=['{} chomps on {}!', '{} bites {}!'],
    dmg = [0,1],
    hit = -1,
  ),
  "bunny" : Move(
    name="Bunny Kick",
    verbs=['{} kicks and grabs and kicks!'],
    dmg = [0,12]
  ),
  "pounce" : Move(
    name="Pounce",
    verbs=['{} charges up and pounces!'],
    dmg = [0,16],
    hit = 2
  ),
  "nibble" : Move(
    name="Nibble",
    verbs= ['{} gives {} a little nibble!', '{} nibbles on {}!'],
    dmg= [0,2]
  ),
  "squeak" : Move(
    name="Squeak",
    verbs= ['{} squeaks loudly!'],
    dmg= [0,1]
  ),
  "swoop" : Move(
    name="Swoop",
    verbs = ['{} swoops down at {} with their claws!'],
    dmg = [0,3]
  ),
  "peck" : Move(
    name="Peck",
    verbs=['{} pecks at {}!', '{} dives at {} with their beak!'],
    dmg = [1,2],
    times = [0,4]
  ),
  "kick" : Move(
    name="Kick",
    verbs=['{} does a crazy kick!', '{} kicks {}!'],
    dmg=[10,15],
    times = [0,1]
  ),
  "slap" : Move(
    name="Slap",
    verbs=['{} does a powerful multi-slap!'],
    dmg=[2,4],
    times = [0,3]
  ),
  "tailgrab" : Move(
    name="Tail Grab",
    verbs = ['{} grabs {}\'s tail!'],
    dmg=[4,6],
    times=[0,1],
    hit=-2
  ),
  "backrub" : Move(
    name="Backwards Fur Rub",
    verbs = ['{} rubs {}\'s backwards!'],
    dmg=[1,2],
    times=[0,2]
  )
}