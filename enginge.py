import libtcodpy as lcod
from input_handlers import handle_keys

def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    lcod.console_set_custom_font("arial10x10.png", lcod.FONT_TYPE_GRAYSCALE | lcod.FONT_LAYOUT_TCOD)

    lcod.console_init_root(screen_width, screen_height, 'TicTacRogue', False)

    con = lcod.console_new(screen_width, screen_height)

    key = lcod.Key()
    mouse = lcod.Mouse()

    while not lcod.console_is_window_closed():
        lcod.sys_check_for_event(lcod.EVENT_KEY_PRESS, key, mouse)

        lcod.console_set_default_foreground(con, lcod.white)
        lcod.console_put_char(con, player_x, player_y, '@', lcod.BKGND_NONE)
        lcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        lcod.console_flush()

        lcod.console_put_char(con, player_x, player_y, ' ', lcod.BKGND_NONE)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            lcod.console_set_fullscreen(not lcod.console_is_fullscreen())

if __name__ == "__main__":
    main()
