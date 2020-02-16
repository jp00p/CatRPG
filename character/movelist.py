from . import move

class COLORS:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

moveList = {
    "claw": move.Move(
        name="Claw",
        verbs=['{} swipes at {} with their claws!',
               '{} slashes with their claws!'],
        dmg=[1, 6],
        times=2
    ),
    "doubleclaw": move.Move(
        name="Double Claw",
        verbs=['{} does a super fast double-claw!'],
        dmg=[1, 8],
        times=4,
        hit=-2,
    ),
    "bite": move.Move(
        name="Bite",
        verbs=['{} chomps on {}!', '{} bites {}!'],
        dmg=[1, 12],
        hit=-1,
    ),
    "bunny": move.Move(
        name="Bunny Kick",
        verbs=['{} grabs and kicks like a wild bunny'],
        dmg=[1, 12]
    ),
    "pounce": move.Move(
        name="Pounce",
        verbs=['{} charges up and pounces!', '{} pounces on {}!'],
        dmg=[4, 16],
        hit=2
    ),
    "slime": move.Move(
      name="Slime",
      verbs=["{} shoots slime at {}!", "{} covers {} in slime!", "{} excretes slime!"],
      dmg=[0,15],
      hit=-5
    ),
    "slurp": move.Move(
      name="Slurp",
      verbs=["{} slurps {}!", "{} makes a weird slurping noise!"],
      dmg=[1,4],
      hit=5,
      times=3
    ),
    "shroom": move.Move(
        name="Shroom Spores",
        verbs=['{} flings spores all over!', '{} does mushroomy things at {}!'],
        dmg=[10,15],
        hit=4
    ),
    "nibble": move.Move(
        name="Nibble",
        verbs=['{} gives {} a little nibble!', '{} nibbles on {}!'],
        dmg=[1, 2]
    ),
    "squeak": move.Move(
        name="Squeak",
        verbs=['{} squeaks loudly!', '{} makes a shrill shrieking noise!'],
        dmg=[1, 1],
        effect=["ringing", 50],
        effect_text="There's a ringing in your ears!"
    ),
    "hiss": move.Move(
        name="Hiss",
        verbs=['{} does a scary hiss at {}!', '{} hisses!'],
        dmg=[1, 10],
        hit=1
    ),
    "barf": move.Move(
        name="Hairball",
        verbs=['{} coughs up a hairball!', '{} starts barfing and grosses {} out!'],
        dmg=[1, 12],
        hit=-1,
        times=2,
        effect=["stinkyface", 100],
        effect_text=COLORS.GREEN+"You are grossed out!"+COLORS.END
    ),
    "slither": move.Move(
        name="Slither",
        verbs=["{} does a creepy spiraling slither at {}!", "{} does a scary slither at {}!"],
        dmg=[1, 4],
        times=3
    ),
    "splash": move.Move(
        name="Splash",
        verbs=["{} splashes water at {}!"],
        dmg=[1, 6],
        hit=-1
    ),
    "swoop": move.Move(
        name="Swoop",
        verbs=['{} swoops down at {} with their claws!'],
        dmg=[1, 3]
    ),
    "peck": move.Move(
        name="Peck",
        verbs=['{} pecks at {}!', '{} dives at {} with their beak!'],
        dmg=[1, 2],
        times=4
    ),
    "kick": move.Move(
        name="Kick",
        verbs=['{} does a crazy kick!', '{} kicks {}!'],
        dmg=[1, 8]
    ),
    "slap": move.Move(
        name="Slap",
        verbs=['{} does a powerful multi-slap!'],
        dmg=[2, 4],
        times=4,
        hit=-4
    ),
    "tailgrab": move.Move(
        name="Tail Grab",
        verbs=['{} grabs {}\'s tail!'],
        dmg=[4, 6],
        times=1,
        hit=-2
    ),
    "backrub": move.Move(
        name="Backwards Fur Rub",
        verbs=['{} rubs {}\'s fur backwards!'],
        dmg=[4, 8],
        times=2
    ),
    "vacuum_move": move.Move(
      name="Slight Movement",
      verbs=["The {}} makes a slight movement, startling you!", "The {} is moved slightly."],
      dmg=[8,16],
      hit=1
    ),
    "vacuum_roar": move.Move(
      name="Vacuum Roar",
      verbs=["The Vacuum roars to life!"],
      dmg=[6,10],
      times=3
    ),
    "dance": move.Move(
      name="War Dance",
      verbs=["{} does a weasel war dance at {}!", "{} does a weird dance and makes strange sounds!"],
      dmg=[6,12],
      hit=2
    ),
    "dust": move.Move(
      name="Dust Spray",
      verbs=["{} makes {} sneeze!", "{} makes {} cough!"],
      dmg=[7,8],
      times=4
    ),
    "blanket1": move.Move(
      name="Hand Moving under the Blanket",
      verbs=["{} is not moving, which scares you!", "{} moves with suddeness, scaring you!"],
      dmg=[0,10],
      hit=10
    )    
}
