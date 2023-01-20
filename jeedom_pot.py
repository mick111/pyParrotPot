from typing import Optional, Any
import requests


class JeedomPot:
    CMD_ID = {
        "wat_lvl": 1259,
        "water_request": 1263,
        "sunlight": 1268,
        "soil_ec": 1267,
        "soil_temperature": 1270,
        "air_temperature": 1269,
        "soil_moisture": 1275,
        "calibrated_soil_moisture": 1271,
        "calibrated_air_temperature": 1272,
        "calibrated_dli": 1273,
    }

    def __init__(self, host, port, apikey):
        self.apikey = apikey
        self.host = host
        self.port = port

    def __getattr__(self, name):
        if (id := JeedomPot.CMD_ID.get(name)) is not None:
            return self.command(id)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if (id := JeedomPot.CMD_ID.get(name)) is not None:
            return self.command(id, value)
        return super.__setattr__(self, name, value)

    def command(self, command, value=None) -> Optional[Any]:
        if type(command) == int:
            cmd_id = command
        elif (cmd_id := JeedomPot.CMD_ID.get(command)) is None:
            return None
        url = f"http://{self.host}:{self.port}/core/api/jeeApi.php?plugin=virtual&apikey={self.apikey}&id={cmd_id}"
        if value is None:
            url += "&type=cmd"
        else:
            url += f"&type=event&value={value}"
        r = requests.get(url)
        return r.text.strip()


if __name__ == "__main__":
    import json

    jeedom_json = json.loads(
        open("/Users/mick111/secrets/jeedom_creds.json").read()
    )
    jeedom_host, jeedom_port, jeedom_apikey = (
        jeedom_json["host"],
        jeedom_json["port"],
        jeedom_json["parrotpotapikey"],
    )
    jeedom = JeedomPot(host=jeedom_host, port=jeedom_port, apikey=jeedom_apikey)
    print(jeedom.water_level)
    jeedom.water_level = 15
    print(jeedom.water_request)
    jeedom.water_request = 0
    print(jeedom.sunlight)
    jeedom.sunlight = 28
    print(jeedom.soil_ec)
    jeedom.soil_ec = 19
    print(jeedom.soil_temperature)
    jeedom.soil_temperature = 10
    print(jeedom.soil_moisture)
    jeedom.soil_moisture = 11
    print(jeedom.calibrated_soil_moisture)
    jeedom.calibrated_soil_moisture = 12
    print(jeedom.calibrated_air_temperature)
    jeedom.calibrated_air_temperature = 17
    print(jeedom.calibrated_dli)
    jeedom.calibrated_dli = 18
