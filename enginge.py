import libtcodpy as lcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 50

    colors = {
        "dark_wall": lcod.Color(0, 0, 100),
        "dark_ground": lcod.Color(50, 50, 150)
    }

    player = Entity(int(screen_width/2), int(screen_height/2), '@', lcod.white)
    npc = Entity(int(screen_width/2 -5), int(screen_height/2), '@', lcod.yellow)
    entities = [npc, player]

    lcod.console_set_custom_font("arial10x10.png", lcod.FONT_TYPE_GRAYSCALE | lcod.FONT_LAYOUT_TCOD)

    lcod.console_init_root(screen_width, screen_height, 'TicTacRogue', False)

    con = lcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)

    key = lcod.Key()
    mouse = lcod.Mouse()

    while not lcod.console_is_window_closed():
        lcod.sys_check_for_event(lcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, game_map, screen_width, screen_height, colors)

        lcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            lcod.console_set_fullscreen(not lcod.console_is_fullscreen())

if __name__ == "__main__":
    main()
