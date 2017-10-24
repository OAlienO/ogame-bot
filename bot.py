import time
import random
import datetime

from ogame import OGame
from ogame.constants import Buildings, Research, Facilities, Ships, Missions, Speed

class BOT:
    def __init__(self, universe, username, password, server, delay = 60, gap = 60):
        self.ogame = OGame(universe, username, password, server)
        self.planet_ids = self.ogame.get_planet_ids()
        self.delay = delay
        self.gap = gap
        self.resources = {}
        self.resources_buildings = {}
        self.research = {}

    @staticmethod
    def pretty_dict(name, d):
        print "  " + "\033[91m" + name + "\033[0m"
        for key, value in d.iteritems():
            print "  {}: {}".format(key, value)

    def pretty_info(self):
        for planet_id in planet_ids:
            print '\033[92m' + str(datetime.datetime.now()) + '\033[0m'
            self.pretty_dict("resource", self.resources[planet_id])
            self.pretty_dict("resource level", self.resources_buildings[planet_id])
            self.pretty_dict("research", self.research)

    def get_info(self, planet_id):
        for planet_id in self.planet_ids:
            self.resources[planet_id] = self.ogame.get_resources(planet_id)
            self.resources_buildings[planet_id] = self.ogame.get_resources_buildings(planet_id)
            self.research = self.ogame.get_research()

    def auto_escape(self):
        if not self.ogame.is_under_attack(): return
        print '\033[31m' + "under attack!! auto escape on!!" + '\033[0m'
        ships = []
        where = {'galaxy': 1, 'system': 161, 'position': 16}
        resources = {'metal': 10000000, 'crystal': 10000000, 'deuterium': 10000000}
        for value in Ships.values(): ships.append((value, 10000))
        fleet_id = self.ogame.send_fleet(self.planet_ids[0], ships, Speed['100%'], where, Missions['Expedition'], resources)
        if fleet_id: print '\033[31m' + "successfully depart away from battle field!!" + '\033[0m'

    def auto_merge_resources(self, where):
	ships = []
        resources = {'metal': 10000000, 'crystal': 10000000, 'deuterium': 10000000}
        for value in Ships.values(): ships.append((value, 10000))
        # assume mother planet at the first planet
	for planet_id in self.planet_ids[1:]:
	    fleet_id = self.ogame.send_fleet(planet_id, ships, Speed['100%'], where, Missions['Transport'], resources)
            if fleet_id: print '\033[36m' + "send fleet from " + str(planet_id) + '\033[0m'

    def auto_upgrade(self, positive_energy = True):
        if positive_energy and resource["energy"] < 0:
            ogame.build(planet_id, Buildings["SolarPlant"])
            ogame.build(planet_id, Buildings["FusionReactor"])
            if resource["energy"] < -60: ogame.build(planet_id, (Ships["SolarSatellite"],1))
        else:
            for value in Buildings.values():
                ogame.build(planet_id, value)
            for value in Facilities.values():
                ogame.build(planet_id, value)
            for value in Research.values():
                ogame.build(planet_id, value)

    def run(self):
        while True:
            self.get_info()
            self.pretty_info()
            self.auto_escape()
            self.auto_merge_resources()
            time.sleep(random.randint(self.delay, self.delay + self.gap))
