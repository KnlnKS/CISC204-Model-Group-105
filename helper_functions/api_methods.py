import urllib.request as ur_req
import json
import requests as req

def calc(atkr, defr, move, field=None):
    post_attacker(atkr)
    post_defender(defr)
    post_move(move)
    post_result()

    return get_result()


def get_move_info(move):
    url = 'http://localhost:2001/check-move'
    x = req.post(url, data=move)
    with ur_req.urlopen(url) as url_load:
        return json.loads(url_load.read().decode())


# Post Methods
def post_attacker(pokemon):
    url = 'http://localhost:2001/pokemon-attacker'
    x = req.post(url, data=pokemon)
    return x


def post_defender(pokemon):
    url = 'http://localhost:2001/pokemon-defender'
    x = req.post(url, data=pokemon)
    return x


def post_move(name):
    url = 'http://localhost:2001/attacking-move'
    x = req.post(url, data=name)
    return x


def post_result():
    url = 'http://localhost:2001/calc'
    x = req.post(url)
    return x


# Get Methods
def get_result():
    url = 'http://localhost:2001/calc'
    with ur_req.urlopen(url) as url_load:
        return json.loads(url_load.read().decode())


def get_attacker():
    url = 'http://localhost:2001/pokemon-attacker'
    with ur_req.urlopen(url) as url_load:
        return json.loads(url_load.read().decode())


def get_defender():
    url = 'http://localhost:2001/pokemon-defender'
    with ur_req.urlopen(url) as url_load:
        return json.loads(url_load.read().decode())


def get_move():
    url = 'http://localhost:2001/attacking-move'
    with ur_req.urlopen(url) as url_load:
        return json.loads(url_load.read().decode())
