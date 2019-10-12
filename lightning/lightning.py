"""
sto     50
ren   +100
cons  -150
diff  - 50
"""

#!/usr/bin/python3

# web imports
import socket
import requests

# symulation imports
import random

# other imports
import sys
import json
import os
import uuid

GEO_API_KEY = '433b8ba2a50ac91c3467ff415eadd729'

class Lightning:
    def __init__(self):
        # lightning web setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.main_frame_init_port = 5005
        self.main_frame_regular_port = 5505
        self.main_frame_ip = '165.22.125.102'

        if os.path.exists('config.json'):
            with open('config.json', 'r') as config:
                self.config = json.loads( config.read() )
            print('Settings fetch from \'config.json\'.')
        else:
            self.config = self.get_config_from_main_frame()

        # lightning const
        self.power_storage_available = 50
        self.power_stored = 0

    def get_config_from_main_frame(self):
        # send data
        msg_dict = {
            'mac': str( uuid.getnode() ), # getnode() gets MAC address
            'cons': self.get_cons(),
            'geo': self.get_geo(),
        }
        msg_json_enc = json.dumps(msg_dict).encode()
        server_address = (self.main_frame_ip, self.main_frame_init_port)
        print( 'Sending {!r}.'.format(msg_json_enc) )
        sent = self.sock.sendto(msg_json_enc, server_address)
            # where sent is the num of bytes sent

        # receive response
        print('Awaiting ID.')
        data, server = self.sock.recvfrom(4096)
        config_json = data.decode('UTF-8')
        print('Settings file received.')

        # create config.json file
        with open('config.json', 'w') as config:
            config.write(config_json)

        return json.loads(config_json)

    def get_cons(self):
        cons = input('Input lightning_ids of connected houses: ')
        try:
            ids = [int(each) for each in cons.split()]
            return ids
        except:
            print('Invalid input.\n')
            return self.get_cons()

    def get_geo(self):
        url = f'http://api.ipstack.com/152.78.0.22?access_key={GEO_API_KEY}'
        response = requests.get(url)
        response_dict = json.loads(response.text)
        return (response_dict['latitude'], response_dict['longitude'])



    def ren_hourly(self):
        return random.randint(0, 100)

    def cons_hourly(self):
        return random.randint(0, 200)

    def diff_hourly(self):
        return self.ren_hourly() - self.cons_hourly()

    def route_energy(to, amount):
        print(f'Routing {amount} energy units to {to}')

