import libtcodpy as lcod


def handle_keys(key):
    key_char = chr(key.c)

    if key.vk == lcod.KEY_UP or key_char == 'k':
        return {"move": (0, -1)}
    elif key.vk == lcod.KEY_DOWN or key_char == 'j':
        return {"move": (0, 1)}
    elif key.vk == lcod.KEY_LEFT or key_char == 'h':
        return {"move": (-1, 0)}
    elif key.vk == lcod.KEY_RIGHT or key_char == 'l':
        return {"move": (1, 0)}
    elif key_char == 'y':
        return {"move": (-1, -1)}
    elif key_char == 'u':
        return {"move": (1, -1)}
    elif key_char == 'b':
        return {"move": (-1, 1)}
    elif key_char == 'n':
        return {"move": (1, 1)}
    elif key_char == 'c':
        return {"cast": True}

    if key.vk == lcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}

    elif key.vk == lcod.KEY_ESCAPE:
        return {"exit": True}

    return {}
