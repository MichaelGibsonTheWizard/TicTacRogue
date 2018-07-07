import libtcodpy as lcod
from game_messages import Message
from render_functions import RenderOrder
from gamestates import GameStates


def kill_player(player):
    player.char = '%'
    player.color = lcod.dark_red

    return Message("You died!", lcod.dark_red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message("{0} is dead!".format(monster.name.capitalize()), lcod.dark_red)

    monster.char = '%'
    monster.color = lcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = "Remains of " + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
