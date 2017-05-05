#!/usr/bin/python3
import homeassistant.remote as remote
from sys import argv as argv
from sys import exit as exit
import yaml
from datetime import datetime as dt
from datetime import timedelta, timezone
from re import match

with open("/home/zgilburd/git/hass/app_config/secrets.yaml", "r") as stream:
    secrets = yaml.load(stream)

api = remote.API('127.0.0.1', secrets['http_password'])
yrno = remote.get_state(api, 'sensor.yr_symbol')
me = remote.get_state(api, 'sensor.command_sensor')
s = remote.get_state(api, 'sun.sun')
za = remote.get_state(api, 'device_tracker.zandra_v20')
zc = remote.get_state(api, 'device_tracker.zgilburd_zs8')
symb = yrno.as_dict()
sun = s.as_dict()
zandra = za.as_dict()
zack = zc.as_dict()
command = me.as_dict()


set_time = dt.strptime(
                       sun['attributes']['next_setting']
                       .replace("+00:00", "+0000"), '%Y-%m-%dT%H:%M:%S%z')

rise_time = dt.strptime(
                       sun['attributes']['next_rising']
                       .replace("+00:00", "+0000"), '%Y-%m-%dT%H:%M:%S%z')

diff_set = timedelta(hours=23)
diff_rise = timedelta(hours=0.5)
now = dt.now(timezone.utc)

if len(argv) > 1:
    symb['state'] = argv[1]

w_state = 'w'+symb['state']

weather_states = dict(
    w1={'rgb': [224, 157, 34], 'brightness': 135},
    w2={'rgb': [164, 142, 52], 'brightness': 105},
    w3={'rgb': [164, 142, 52], 'brightness': 60},
    w4={'rgb': [86, 88, 90], 'brightness': 60},
    w40={'rgb': [174, 187, 255], 'brightness': 130},
    w5={'rgb': [155, 164, 254], 'brightness': 100},
    w41={'rgb': [83, 17, 255], 'brightness': 76},
    w24={'rgb': [174, 187, 255], 'brightness': 130},
    w6={'rgb': [155, 164, 254], 'brightness': 100},
    w25={'rgb': [83, 17, 255], 'brightness': 76},
    w42={'rgb': [161, 235, 254], 'brightness': 80},
    w7={'rgb': [135, 193, 255], 'brightness': 121},
    w43={'rgb': [66, 192, 255], 'brightness': 107},
    w26={'rgb': [161, 235, 254], 'brightness': 80},
    w20={'rgb': [135, 193, 255], 'brightness': 121},
    w27={'rgb': [66, 192, 255], 'brightness': 107},
    w44={'rgb': [161, 235, 254], 'brightness': 190},
    w8={'rgb': [135, 193, 255], 'brightness': 190},
    w45={'rgb': [66, 192, 255], 'brightness': 190},
    w28={'rgb': [161, 235, 254], 'brightness': 190},
    w21={'rgb': [135, 193, 255], 'brightness': 190},
    w29={'rgb': [66, 192, 255], 'brightness': 190},
    w46={'rgb': [36, 61, 255], 'brightness': 57},
    w9={'rgb': [36, 61, 255], 'brightness': 110},
    w10={'rgb': [36, 61, 255], 'brightness': 190},
    w30={'rgb': [36, 61, 255], 'brightness': 57},
    w22={'rgb': [36, 61, 255], 'brightness': 110},
    w11={'rgb': [36, 61, 255], 'brightness': 190},
    w47={'rgb': [161, 235, 254], 'brightness': 80},
    w12={'rgb': [135, 193, 255], 'brightness': 121},
    w48={'rgb': [66, 192, 255], 'brightness': 107},
    w31={'rgb': [161, 235, 254], 'brightness': 80},
    w23={'rgb': [135, 193, 255], 'brightness': 121},
    w32={'rgb': [66, 192, 255], 'brightness': 107},
    w49={'rgb': [161, 235, 254], 'brightness': 190},
    w13={'rgb': [135, 193, 255], 'brightness': 190},
    w50={'rgb': [66, 192, 255], 'brightness': 190},
    w33={'rgb': [161, 235, 254], 'brightness': 190},
    w14={'rgb': [135, 193, 255], 'brightness': 190},
    w34={'rgb': [66, 192, 255], 'brightness': 190},
    w15={'rgb': [86, 88, 90], 'brightness': 25}
)


def turn_on_light(sets):
    try:
        if sets['norun']:
            print(sets['norun'])
            exit(0)
    except KeyError:
        pass
    remote.call_service(api, 'light', 'turn_on',
                        {'entity_id': 'light.hugo',
                            'rgb_color': sets['rgb'],
                            'brightness': sets['brightness']})
    print("w"+symb['state'])
    exit(0)


def turn_off_light(cmd, rmt):
    if match("^w\d{1,2}$", cmd['state']):
        rmt.call_service(api, 'light', 'turn_off', {'entity_id': 'light.hugo'})


if sun['state'] == "below_horizon":
    if set_time - now < diff_set and rise_time - now > diff_rise:
        weather_states[w_state]['norun'] = "no run: sun's down"
        turn_off_light(command, remote)

if zack['state'] == "home" or zandra['state'] == "home":
    pass
else:
    weather_states[w_state]['norun'] = "no run: no one is home"
    turn_off_light(command, remote)

turn_on_light(weather_states[w_state])
