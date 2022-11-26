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
