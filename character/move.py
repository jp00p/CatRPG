# an attack move
class Move:
  def __init__(self, name="", verbs=[], dmg=[], hit=0, targets=[1,1], times=[0,1], **kwargs):
    self.name = name
    self.verbs = verbs
    self.dmg = dmg
    self.hit = hit
    self.targets = targets
    self.times = times
