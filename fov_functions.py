import libtcodpy as lcod


def initialize_fov(game_map):
    fov_map = lcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            lcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    lcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
