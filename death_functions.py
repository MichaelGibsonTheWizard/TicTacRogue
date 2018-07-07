import libtcodpy as lcod
from render_functions import RenderOrder
from gamestates import GameStates


def kill_player(player):
    player.char = '%'
    player.color = lcod.dark_red

    return "You died!", GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = "{0} is dead!".format(monster.name.capitalize())

    monster.char = '%'
    monster.color = lcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = "Remains of " + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
