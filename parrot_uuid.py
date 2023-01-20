from enum import Enum
"""
https://forum.fhem.de/index.php?topic=68568.15
"""

class Service(str, Enum):
    """Services UUIDs"""

    Live = "39e1FA00-84a8-11e2-afba-0002a5d5c51b"
    Clock = "39e1FD00-84a8-11e2-afba-0002a5d5c51b"
    Watering = "39e1f900-84a8-11e2-afba-0002a5d5c51b"
    PlantDr = "39e1f900-84a8-11e2-afba-0002a5d5c51b"


class Characteristic(str, Enum):
    # Service Live
    notifications_timer = "39e1fa06-84a8-11e2-afba-0002a5d5c51b"
    sunlight = "39e1fa01-84a8-11e2-afba-0002a5d5c51b"
    soil_ec = "39e1fa02-84a8-11e2-afba-0002a5d5c51b"
    soil_temperature = "39e1fa03-84a8-11e2-afba-0002a5d5c51b"
    air_temperature = "39e1fa04-84a8-11e2-afba-0002a5d5c51b"
    soil_moisture = "39e1fa05-84a8-11e2-afba-0002a5d5c51b"
    led = "39e1fa07-84a8-11e2-afba-0002a5d5c51b"
    lastmovedate = "39e1fa08-84a8-11e2-afba-0002a5d5c51b"
    calibrated_soil_moisture = "39e1fa09-84a8-11e2-afba-0002a5d5c51b"
    calibrated_air_temperature = "39e1fa0a-84a8-11e2-afba-0002a5d5c51b"
    calibrated_dli = "39e1fa0b-84a8-11e2-afba-0002a5d5c51b"
    calibrated_ea = "39e1fa0c-84a8-11e2-afba-0002a5d5c51b"
    calibrated_ecb = "39e1fa0d-84a8-11e2-afba-0002a5d5c51b"
    calibrated_ec_porous = "39e1fa0e-84a8-11e2-afba-0002a5d5c51b"
    light_red = "39e1fa0f-84a8-11e2-afba-0002a5d5c51b"
    light_green = "39e1fa10-84a8-11e2-afba-0002a5d5c51b"
    light_blue = "39e1fa11-84a8-11e2-afba-0002a5d5c51b"
    # Service.Clock
    time_start = "39e1fd01-84a8-11e2-afba-0002a5d5c51b"
    time_utc = "39e1fd02-84a8-11e2-afba-0002a5d5c51b"
    # Service.Watering
    wat_config_id = "39e1f901-84a8-11e2-afba-0002a5d5c51b"
    wat_plant_id = "39e1f902-84a8-11e2-afba-0002a5d5c51b"
    wat_vwc_irr = "39e1f903-84a8-11e2-afba-0002a5d5c51b"
    wat_vwc_cmd = "39e1f904-84a8-11e2-afba-0002a5d5c51b"
    wat_n_irr = "39e1f905-84a8-11e2-afba-0002a5d5c51b"
    wat_cmd = "39e1f906-84a8-11e2-afba-0002a5d5c51b"
    wat_lvl = "39e1f907-84a8-11e2-afba-0002a5d5c51b"
    wat_pump_duty_cycle = "39e1f908-84a8-11e2-afba-0002a5d5c51b"
    wat_unknown = "39e1f909-84a8-11e2-afba-0002a5d5c51b"
    wat_vwc_irr_eco = "39e1f90a-84a8-11e2-afba-0002a5d5c51b"
    wat_vwc_cmd_eco = "39e1f90b-84a8-11e2-afba-0002a5d5c51b"
    wat_n_irr_eco = "39e1f90c-84a8-11e2-afba-0002a5d5c51b"
    wat_mode = "39e1f90d-84a8-11e2-afba-0002a5d5c51b"
    wat_time_slot_start = "39e1f90e-84a8-11e2-afba-0002a5d5c51b"
    wat_time_slot_durr = "39e1f90f-84a8-11e2-afba-0002a5d5c51b"
    wat_vacation_start = "39e1f910-84a8-11e2-afba-0002a5d5c51b"
    wat_vacation_end = "39e1f911-84a8-11e2-afba-0002a5d5c51b"
    wat_algo_status = "39e1f912-84a8-11e2-afba-0002a5d5c51b"
    wat_unknown2 = "39e1f913-84a8-11e2-afba-0002a5d5c51b"
    # Service.PlantDr
    pdr_config_id = "39e1fd81-84a8-11e2-afba-0002a5d5c51b"
    pdr_dry_n = "39e1fd82-84a8-11e2-afba-0002a5d5c51b"
    pdr_dry_vwc = "39e1fd83-84a8-11e2-afba-0002a5d5c51b"
    pdr_wet_n = "39e1fd84-84a8-11e2-afba-0002a5d5c51b"
    pdr_wet_vwc = "39e1fd85-84a8-11e2-afba-0002a5d5c51b"
    pdr_status_flags = "39e1fd86-84a8-11e2-afba-0002a5d5c51b"
    pdr_next_wat_date = "39e1fd87-84a8-11e2-afba-0002a5d5c51b"
    pdr_next_empty_tank_date = "39e1fd88-84a8-11e2-afba-0002a5d5c51b"
    pdr_full_tank_autonomy = "39e1fd89-84a8-11e2-afba-0002a5d5c51b"


UUID = {
    Service.Live: [
        Characteristic.notifications_timer,
        Characteristic.sunlight,
        Characteristic.soil_ec,
        Characteristic.soil_temperature,
        Characteristic.air_temperature,
        Characteristic.soil_moisture,
        Characteristic.led,
        Characteristic.lastmovedate,
        Characteristic.calibrated_soil_moisture,
        Characteristic.calibrated_air_temperature,
        Characteristic.calibrated_dli,
        Characteristic.calibrated_ea,
        Characteristic.calibrated_ecb,
        Characteristic.calibrated_ec_porous,
        Characteristic.light_red,
        Characteristic.light_green,
        Characteristic.light_blue,
    ],
    Service.Clock: [
        Characteristic.time_start,
        Characteristic.time_utc,
    ],
    Service.Watering: [
        Characteristic.wat_config_id,
        Characteristic.wat_plant_id,
        Characteristic.wat_vwc_irr,
        Characteristic.wat_vwc_cmd,
        Characteristic.wat_n_irr,
        Characteristic.wat_cmd,
        Characteristic.wat_lvl,
        Characteristic.wat_pump_duty_cycle,
        Characteristic.wat_unknown,
        Characteristic.wat_vwc_irr_eco,
        Characteristic.wat_vwc_cmd_eco,
        Characteristic.wat_n_irr_eco,
        Characteristic.wat_mode,
        Characteristic.wat_time_slot_start,
        Characteristic.wat_time_slot_durr,
        Characteristic.wat_vacation_start,
        Characteristic.wat_vacation_end,
        Characteristic.wat_algo_status,
        Characteristic.wat_unknown2,
    ],
    Service.PlantDr: [
        Characteristic.pdr_config_id,
        Characteristic.pdr_dry_n,
        Characteristic.pdr_dry_vwc,
        Characteristic.pdr_wet_n,
        Characteristic.pdr_wet_vwc,
        Characteristic.pdr_status_flags,
        Characteristic.pdr_next_wat_date,
        Characteristic.pdr_next_empty_tank_date,
        Characteristic.pdr_full_tank_autonomy,
    ],
}
