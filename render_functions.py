import libtcodpy as lcod


def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = lcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible or game_map.tiles[x][y].explored:
                    game_map.tiles[x][y].explored = True
                    if wall:
                        lcod.console_set_char_background(con, x, y, colors.get("dark_wall"), lcod.BKGND_SET)
                    else:
                        lcod.console_set_char_background(con, x, y, colors.get("dark_ground"), lcod.BKGND_SET)

    for entity in entities:
        draw_entity(con, entity, fov_map)

    lcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if lcod.map_is_in_fov(fov_map, entity.x, entity.y):
        lcod.console_set_default_foreground(con, entity.color)
        lcod.console_put_char(con, entity.x, entity.y, entity.char, lcod.BKGND_NONE)


def clear_entity(con, entity):
    lcod.console_put_char(con, entity.x, entity.y, ' ', lcod.BKGND_NONE)
