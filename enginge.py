import libtcodpy as lcod
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
    map_width = 80
    map_height = 50
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

    fighter_component = Fighter(hp=12, defense=2, power=5)
    player = Entity(0, 0, '@', lcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    lcod.console_set_custom_font("arial10x10.png", lcod.FONT_TYPE_GRAYSCALE | lcod.FONT_LAYOUT_TCOD)

    lcod.console_init_root(screen_width, screen_height, "TicTacRogue", False)

    con = lcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = lcod.Key()
    mouse = lcod.Mouse()

    game_state = GameStates.PLAYER_TURN

    while not lcod.console_is_window_closed():
        lcod.sys_check_for_event(lcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        lcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        player_turn_resluts = []

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_resluts.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            lcod.console_set_fullscreen(not lcod.console_is_fullscreen())

        for player_turn_reslut in player_turn_resluts:
            message = player_turn_reslut.get("message")
            dead_entity = player_turn_reslut.get("dead")

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            print(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()
