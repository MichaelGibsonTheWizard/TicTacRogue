import libtcodpy as lcod

def handle_keys(key):
    if key.vk == lcod.KEY_UP:
        return {"move": (0, -1)}
    elif key.vk == lcod.KEY_DOWN:
        return {"move": (0, 1)}
    elif key.vk == lcod.KEY_LEFT:
        return {"move": (-1, 0)}
    elif key.vk == lcod.KEY_RIGHT:
        return {"move": (1, 0)}

    if key.vk == lcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}

    elif key.vk == lcod.KEY_ESCAPE:
        return {"exit": True}

    return {}
