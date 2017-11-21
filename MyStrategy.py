from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Player import Player
from model.World import World

from map import WorldMap


class MyStrategy:
    def __init__(self, max_size=1024):
        self.map = WorldMap(max_size=max_size)

    def move(self, me: Player, world: World, game: Game, move: Move):
        self.map.update(world.new_vehicles, world.vehicle_updates)
        if world.tick_index == 0:
            move.action = ActionType.CLEAR_AND_SELECT
            move.right = world.width
            move.bottom = world.height

        if world.tick_index == 1:
            move.action = ActionType.MOVE
            move.x = world.width / 1.0
            move.y = world.height / 2.0
