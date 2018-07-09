class Effect:
    def __init__(self, target, turns_used=0, used_last_turn=False):
        self.target = target
        self.turns_used = turns_used
        self.used_last_turn = used_last_turn

    def process_effect(self):
        self.turns_used += 1
        self.used_last_turn = True

    def clean_effect(self):
        self.turns_used = 0
        self.used_last_turn = False


class PowerArmor(Effect):
    def __init__(self, target, turns_used=0, used_last_turn=False):
        Effect.__init__(self, target, turns_used, used_last_turn)
        self.starting_power = target.fighter.power
        self.starting_defense = target.fighter.defense

    def process_effect(self):
        if self.target.fighter:
            target = self.target.fighter
            defense_gained = int((target.power ** self.turns_used) / 4)
            print(str(defense_gained) + '\n')
            if target.power >= defense_gained:
                target.defense += defense_gained
                target.power -= defense_gained
            else:
                target.power = 0

        super().process_effect()

    def clean_effect(self):
        super().clean_effect()
        self.target.fighter.power = self.starting_power
        self.target.fighter.defense = self.starting_defense
