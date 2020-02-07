from . import move

moveList = {
  "claw" : move.Move(
    name="Claw",
    verbs=['{} swipes at {} with their claws!', '{} slashes with their claws!'],
    dmg = [1,6]
  ),
  "doubleclaw" : move.Move(
    name="Double Claw",
    verbs = ['{} does a super fast double-claw!'],
    dmg = [1,8],
    times = 2,
    hit = -2
  ),
  "bite" : move.Move(
    name="Bite",
    verbs=['{} chomps on {}!', '{} bites {}!'],
    dmg = [1,1],
    hit = -1,
  ),
  "bunny" : move.Move(
    name="Bunny Kick",
    verbs=['{} kicks and grabs and kicks!'],
    dmg = [1,12]
  ),
  "pounce" : move.Move(
    name="Pounce",
    verbs=['{} charges up and pounces!'],
    dmg = [1,16],
    hit = 2
  ),
  "nibble" : move.Move(
    name="Nibble",
    verbs= ['{} gives {} a little nibble!', '{} nibbles on {}!'],
    dmg= [1,2]
  ),
  "squeak" : move.Move(
    name="Squeak",
    verbs= ['{} squeaks loudly!'],
    dmg= [1,1]
  ),
  "hiss" : move.Move(
    name="Hiss",
    verbs=['{} does a scary hiss at {}!', '{} hisses!'],
    dmg = [1,10],
    hit = 1
  ),
  "slither" : move.Move(
    name="Slither",
    verbs=["{} does a creepy spiraling slither at {}!"],
    dmg=[1,4],
    times=3
  ),
  "swoop" : move.Move(
    name="Swoop",
    verbs = ['{} swoops down at {} with their claws!'],
    dmg = [1,3]
  ),
  "peck" : move.Move(
    name="Peck",
    verbs=['{} pecks at {}!', '{} dives at {} with their beak!'],
    dmg = [1,2],
    times = 4
  ),
  "kick" : move.Move(
    name="Kick",
    verbs=['{} does a crazy kick!', '{} kicks {}!'],
    dmg=[1,15]
  ),
  "slap" : move.Move(
    name="Slap",
    verbs=['{} does a powerful multi-slap!'],
    dmg=[2,4],
    times=3
  ),
  "tailgrab" : move.Move(
    name="Tail Grab",
    verbs = ['{} grabs {}\'s tail!'],
    dmg=[4,6],
    times=1,
    hit=-2
  ),
  "backrub" : move.Move(
    name="Backwards Fur Rub",
    verbs = ['{} rubs {}\'s backwards!'],
    dmg=[4,8],
    times=2
  )
}