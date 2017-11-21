import numpy as np

VEHICLE_TYPES = {"ARRV": 0,
                 "FIGHTER": 1,
                 "HELICOPTER": 2,
                 "IFV": 3,
                 "TANK": 4}

N_VEHICLE_TYPES = len(VEHICLE_TYPES)

MAP_SIZE = 1024.


class WorldMap(object):
    """
    Store some information about world in one place: vehicles positions (density) in hierarchical view.
    """
    def __init__(self, max_size=1024):
        """

        :param max_size: maximum size of discrete map, each next map will be twice smaller
        """
        self.vehicles = {}  # dictionary to store all vehicles
        self.maps = []

        self.scale = MAP_SIZE / max_size
        self.max_size = max_size
        self.dividers = [1]
        sz = max_size
        self.n_channels = N_VEHICLE_TYPES * 2  # for each player & for each type of vehicle

        self.dividers = []

        while sz > 1:
            self.maps.append(np.zeros((sz, sz, self.n_channels)))
            self.dividers.append(max_size // sz)
            sz = sz // 2

    def update(self, new_vehicles, vehicle_updates):
        """
        Update maps & states of vehicles
        :param new_vehicles: list of new vehicles
        :param vehicle_updates: list of updated vehicles
        :return:
        """
        for v in new_vehicles:
            self.vehicles[v.id] = v
            for d, m in zip(self.dividers, self.maps):
                m[int(v.x / self.scale) // d, int(v.y / self.scale) // d] += 1

        for v_update in vehicle_updates:
            self._update_maps(v_update)
            # update vehicle
            self.vehicles[v_update.id].update(v_update)

    def _update_maps(self, update):
        v = self.vehicles[update.id]
        for d, m in zip(self.dividers, self.maps):
            m[int(v.x / self.scale) // d, int(v.y / self.scale) // d] -= 1
            m[int(update.x / self.scale) // d, int(update.y / self.scale) // d] += 1
