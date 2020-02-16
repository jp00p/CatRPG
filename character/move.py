# an attack move, usable by any Character
# effects only work on Player objects for now
class Move:
  def __init__(self, name="", verbs=[""], dmg=[1,1], hit=0, targets=[1,1], times=1, effect=False, effect_text="", **kwargs):
    self.name = name
    self.verbs = verbs
    self.dmg = dmg
    self.hit = hit
    self.targets = targets
    self.times = times
    self.effect = effect
    self.effect_text = effect_text
