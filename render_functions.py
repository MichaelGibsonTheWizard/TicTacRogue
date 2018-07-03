import libtcodpy as lcod

def render_all(con, entities, game_map, screen_width, screen_height, colors):
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                lcod.console_set_char_background(con, x, y, colors.get("dark_wall"))
            else:
                lcod.console_set_char_background(con, x, y, colors.get("dark_ground"))

    for entity in entities:
        draw_entity(con, entity)

    lcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    lcod.console_set_default_foreground(con, entity.color)
    lcod.console_put_char(con, entity.x, entity.y, entity.char, lcod.BKGND_NONE)

def clear_entity(con, entity):
    lcod.console_put_char(con, entity.x, entity.y, ' ', lcod.BKGND_NONE)
