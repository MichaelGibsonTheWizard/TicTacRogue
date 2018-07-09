import libtcodpy as lcod


class Spellbook:
    def __init__(self, spells=None):
        self.spells = spells

    def choose_spell(self):
        self.list_spells()
        key = lcod.Key()
        mouse = lcod.Mouse()
        lcod.sys_check_for_event(lcod.EVENT_KEY_PRESS, key, mouse)
        key_char = chr(key)
        if key_char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            key = int(key_char)
            chosen_spell = self.spells[1-key]
        else:
            chosen_spell = self.spells[0]
        return chosen_spell

    def list_spells(self):
        spell_number = 1
        for spell in self.spells:
            print(str(spell_number) + spell.name + "\n")
            spell_number += 1
