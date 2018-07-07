import libtcodpy as lcod
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    lcod.console_set_default_background(panel, back_color)
    lcod.console_rect(panel, x, y, total_width, 1, False, lcod.BKGND_SCREEN)

    lcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        lcod.console_rect(panel, x, y, bar_width, 1, False, lcod.BKGND_SCREEN)

    lcod.console_set_default_foreground(panel, lcod.white)
    lcod.console_print_ex(panel, int(x + total_width / 2), y, lcod.BKGND_NONE, lcod.CENTER,
                          "{0}: {1}/{2}".format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, colors):
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

    lcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    lcod.console_set_default_background(panel, lcod.black)
    lcod.console_clear(panel)

    y = 1
    for message in message_log.messages:
        lcod.console_set_default_foreground(panel, message.color)
        lcod.console_print_ex(panel, message_log.x, y, lcod.BKGND_NONE, lcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, "HP", player.fighter.hp, player.fighter.max_hp,
               lcod.light_red, lcod.darker_red)

    lcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if lcod.map_is_in_fov(fov_map, entity.x, entity.y):
        lcod.console_set_default_foreground(con, entity.color)
        lcod.console_put_char(con, entity.x, entity.y, entity.char, lcod.BKGND_NONE)


def clear_entity(con, entity):
    lcod.console_put_char(con, entity.x, entity.y, ' ', lcod.BKGND_NONE)
