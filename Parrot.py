#!/usr/bin/python
import sys
import json
from parrot_pot import ParrotPot

READ_ALL = [
    "CURRENT_TIME",
    "SUNLIGHT",
    "SOIL_EC",
    "SOIL_TEMPERATURE",
    "AIR_TEMPERATURE",
    "SOIL_MOISTURE",
    "CALIBRATED_SOIL_MOISTURE",
    "CALIBRATED_AIR_TEMPERATURE",
    "CALIBRATED_DLI",
    "WAT_LVL",
    # "CALIBRATED_EA",
    # "CALIBRATED_ECB",
    # "CALIBRATED_EC_POROUS",
]


cache_file_path = "/var/www/html/plugins/script/core/ressources/flower_power_cache.json"
try:
    cached_values = json.load(open(cache_file_path, "r+"))
except Exception as e:
    print("Warning during load", e)
    cached_values = {}


def get_live_vals(pot: ParrotPot, args):
    cache_dict = {}
    pot.live = True
    for arg in args:
        val = None
        if arg == "AIR_TEMPERATURE":
            val = pot.air_temperature
        elif arg == "SOIL_TEMPERATURE":
            val = pot.soil_temperature
        elif arg == "SOIL_EC":
            val = pot.soil_electrical_conductivity
        elif arg == "SOIL_MOISTURE":
            val = pot.soil_moisture
        elif arg == "SUNLIGHT":
            val = pot.sunlight
        elif arg == "CALIBRATED_DLI":
            val = pot.calibrated_dli
        elif arg == "CALIBRATED_SOIL_MOISTURE":
            val = pot.calibrated_soil_moisture
        elif arg == "CALIBRATED_AIR_TEMPERATURE":
            val = pot.calibrated_air_temperature
        elif arg == "CALIBRATED_EA":
            val = pot.calibrated_ea
        elif arg == "CALIBRATED_ECB":
            val = pot.calibrated_ecb
        elif arg == "CALIBRATED_EC_POROUS":
            val = pot.calibrated_ec_porous
        elif arg == "WAT_LVL":
            val = pot.water_level
        if val is not None:
            cache_dict[arg] = val
    pot.live = False
    return cache_dict


force_read = False
show = False
val = None
pot = ParrotPot()
pot.connect()
for arg in sys.argv[1:]:
    args = READ_ALL if arg == "ALL" else [arg]
    for arg in args:
        val = None
        if arg == "LED":
            pot.led()
        elif arg == "WATER":
            pot.water(10)
        elif arg == "CACHE":
            all_vals = get_live_vals(pot, READ_ALL)
            json.dump(all_vals, open(cache_file_path, "w+"))
            val = cache_file_path
        elif arg == "FORCE":
            force_read = True
        elif arg == "SHOW":
            show = True
        elif arg == "CURRENT_TIME":
            val = pot.current_time
        else:
            if force_read or arg not in cached_values:
                vals = get_live_vals(pot, [arg])
                val = vals[arg]
            else:
                val = cached_values[arg]
        if show:
            print(arg, val)

print(val)
pot.disconnect()
