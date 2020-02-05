class Breed():
  def __init__(self, name="", stats=[], desc="", **kwargs):
    self.name = name
    self.stats = stats # fer,acr,cur
    self.desc = desc

breedList = [
  Breed("Debug Cat", [50,50,50], "GOD MODE"),
  Breed("Domestic Shorthair", [2,2,1], "Average and curious"),
  Breed("Persian", [3,1,0], "Slow but fluffy"),
  Breed("Sphynx", [1,3,0], "Quick and hairless"),
  Breed("Tuxedo", [2,0,2], "Well-dressed and inquisitve"),
  Breed("Maine Coon", [4,0,0], "Super big and beautiful"),
  Breed("Abyssinian", [0,4,0], "Lean and super acrobatic"),
  Breed("Scottish Fold", [0,0,4], "Super curious explorer")
]    