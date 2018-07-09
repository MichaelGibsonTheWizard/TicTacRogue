import libtcodpy as lcod
from game_messages import Message, MessageLog
from effect import Effect, PowerArmor
from death_functions import kill_monster, kill_player
from components.ai import BasicMonster
from components.fighter import Fighter
from gamestates import GameStates
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap


def main():
    screen_width = 80
    screen_height = 50
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    map_width = 80
    map_height = 43
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        "dark_wall": lcod.Color(0, 0, 100),
        "dark_ground": lcod.Color(50, 50, 150),
        "light_wall": lcod.Color(130, 110, 50),
        "light_ground": lcod.Color(200, 180, 50),
    }

    fighter_component = Fighter(hp=12, defense=3, power=5)
    player = Entity(0, 0, '@', lcod.white, "Player", [], blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    lcod.console_set_custom_font("arial10x10.png", lcod.FONT_TYPE_GRAYSCALE | lcod.FONT_LAYOUT_TCOD)

    lcod.console_init_root(screen_width, screen_height, "TicTacRogue", False)

    con = lcod.console_new(screen_width, screen_height)
    panel = lcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = lcod.Key()
    mouse = lcod.Mouse()

    game_state = GameStates.PLAYER_TURN
    power_armor = PowerArmor(player)

    while not lcod.console_is_window_closed():
        lcod.sys_check_for_event(lcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
                   bar_width, panel_height, panel_y, colors)

        lcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        cast = action.get("cast")
        fullscreen = action.get("fullscreen")

        player_turn_results = []

        if cast and game_state == GameStates.PLAYER_TURN:
            if power_armor not in player.effects:
                print("Adding effects to list")
                player.effects.append(power_armor)

            player.evaluate_effects()
            game_state = GameStates.ENEMY_TURN

        elif move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                player.evaluate_effects()
                player.clean_effects()
                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            lcod.console_set_fullscreen(not lcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()
