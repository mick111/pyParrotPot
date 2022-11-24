#!/usr/bin/python
import sys
import json
import warnings

from parrot_pot import ParrotPot

CACHED_ALL = [
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
]
ALL = CACHED_ALL + [
    "CALIBRATED_EA",
    "CALIBRATED_ECB",
    "CALIBRATED_EC_POROUS",
]

cache_file_path = "/var/www/html/plugins/script/core/ressources/flower_power_cache.json"
try:
    cached_values = json.load(open(cache_file_path, "r+"))
    warnings.warn(f"Cached values: {cached_values}")
except Exception as e:
    warnings.warn(f"Warning during load: {e}")
    cached_values = {}


def get_live_vals(pot: ParrotPot, args):
    values = {}
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
        elif arg == "CURRENT_TIME":
            val = pot.current_time
        if val is not None:
            values[arg] = val
    pot.live = False
    return values


cached = False
show = False
val = None
pot = ParrotPot()
pot.connect()
all_read_vals = {}
for arg in sys.argv[1:]:
    if arg == "ALL":
        new_vals = json.load(open(cache_file_path)) if cached else get_live_vals(pot, ALL)

        all_read_vals.update(new_vals)
        if show:
            print(arg, val)
    elif arg == "CACHE":
        # Save in cache all previous read values
        json.dump(all_read_vals, open(cache_file_path, "w+"))
    elif arg == "LED":
        pot.led()
    elif arg == "WATER":
        pot.water(10)
    elif arg == "SHOW":
        # When this keyword is encountered, all read data is shown
        show = True
    elif arg == "CACHED":
        # When this keyword is encountered, all data are read from cache
        cached = True
    else:
        if cached:
            # Read all cached values
            read_vals.update(json.load(open(cache_file_path)))
        else:
            # Read all values in one LIVE session
            read_vals.update(get_live_vals(pot, ALL))

    args = ALL if arg ==  else [arg]
    for arg in args:
        val = None


print(val)
pot.disconnect()
