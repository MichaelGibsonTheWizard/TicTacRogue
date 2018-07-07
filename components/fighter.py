class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({"dead": self.owner})

        return results

    def attack(self, target):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            percent_gone_through = int(float(damage/self.power) * 100)
            results.append({"message": "{0} attacks {1}! It's {2} effective!".format(self.owner.name.capitalize(),
                            target.name, str(percent_gone_through))})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({"message": "Not... Enough... Power...!"})

        return results
