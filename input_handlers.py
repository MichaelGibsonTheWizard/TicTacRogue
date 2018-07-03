import libtcodpy as lcod

def handle_keys(key):
    if key.vk == lcod.KEY_UP:
        print("Up Key")
        return {"move": (0, -1)}
    elif key.vk == lcod.KEY_DOWN:
        print("Down Key")
        return {"move": (0, 1)}
    elif key.vk == lcod.KEY_LEFT:
        print("Left key")
        return {"move": (-1, 0)}
    elif key.vk == lcod.KEY_RIGHT:
        print("Right Key")
        return {"move": (1, 0)}

    if key.vk == lcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}

    elif key.vk == lcod.KEY_ESCAPE:
        return {"exit": True}

    return {}
