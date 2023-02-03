import create_response as ESP

### aircon/teams esp
## TV esp
# ip address for esp
ip_tv = "http://10.0.0.126/"

# create object
ESP_TV = ESP.Esp("esp_aircon", ip_tv)

# set available paths
ESP_TV.ip_paths["post_aircon"] = ip_tv + "aircon"
ESP_TV.ip_paths["post_teams"] = ip_tv + "teams"
ESP_TV.ip_paths["get_state"] = ip_tv + "state"

# set default data to post
ESP_TV.data = {
    "aircon": {
        "power": "1",
        "mode": "",
        "temp": "",
        "fan": "",
        "powerful": "",
        "quiet": "",
        "econ": "",
        "comfort": ""
    },
    "room_temp": "",
    "teams_status": "unknown"
}


# door esp
ip_door = "http://10.0.0.117/"
esp_door = ESP.Esp("esp_door", ip_door)

ip_roof = "http://10.0.0.118/"
esp_roof = ESP.Esp("esp_roof", ip_roof)

