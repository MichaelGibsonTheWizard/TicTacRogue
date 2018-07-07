import libtcodpy as lcod
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
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

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    lcod.console_set_default_foreground(con, lcod.white)
    lcod.console_print_ex(con, 1, screen_height - 2, lcod.BKGND_NONE, lcod.LEFT,
                          "HP: {0:02}/{1:02}".format(player.fighter.hp, player.fighter.max_hp))

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
