import libtcodpy as lcod

def main():
    screen_width = 80
    screen_height = 50

    lcod.console_set_custom_font("arial10x10.png", lcod.FONT_TYPE_GRAYSCALE | lcod.FONT_LAYOUT_TCOD)

    lcod.console_init_root(screen_width, screen_height, 'TicTacRogue', False)

    while not lcod.console_is_window_closed():
        lcod.console_set_default_foreground(0, lcod.white)
        lcod.console_put_char(0, 1, 1, '@', lcod.BKGND_NONE)
        lcod.console_flush()

        key = lcod.console_check_for_keypress()

        if key.vk == lcod.KEY_ESCAPE:
            return True

if __name__ == "__main__":
    main()
