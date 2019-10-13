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
import battery
import time
import random

# other imports
import sys
import json
import os
import uuid
import threading

# API to get IP by http://jsonip.com
# API to get GEO by https://ipstack.com
GEO_API_KEY = '433b8ba2a50ac91c3467ff415eadd729'

MAIN_FRAME_IP = '165.22.125.102'
MAIN_FRAME_PORT = 5005 

DIFF_VALS = (-1, -1, -1, -1, -1)
I = 0

class Lightning:
    def __init__(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config:
                self.config = json.loads( config.read() )
            print('Settings fetch from \'config.json\'.')
        else:
            self.config = self.get_config_from_main_frame()

        self.battery = battery.Battery(50)
        self.watch_and_alert(5)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((MAIN_FRAME_IP, MAIN_FRAME_PORT))

        self.listen_thread = threading.Thread(target=self.listen_for_energy_change)
        self.listen_thread.start()

    def get_config_from_main_frame(self):
        # send data
        msg_dict = {
            'type': 'init',
            'mac': uuid.getnode(),
            'cons': self.get_cons(),
            'geo': self.get_geo(),
        }
        msg_json_enc = json.dumps(msg_dict).encode()
        server_address = (MAIN_FRAME_IP, MAIN_FRAME_PORT)
        print( 'Sending {!r}.'.format(msg_json_enc) )
        sent = self.sock.sendto(msg_json_enc, server_address)
            # where sent is the num of bytes sent

        # receive response
        print('Awaiting response.')
        data, server = self.sock.recvfrom(4096)
        config_json = data.decode('UTF-8')
        print('Settings file received.')

        # create config.json file
        with open('config.json', 'w') as config:
            config.write(config_json)

        # sock.close()
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
        """
        # manual geo input
        try:
            geo_input = input('Input latitude and longditude: ')
            return [float(each) for each in geo_input.split()]
        except:
            print('Invalid input.\n')
            return self.get_geo()
        """

        # autmatic geo detection
        ip = json.loads( requests.get('http://jsonip.com').text )['ip']
        url = f'http://api.ipstack.com/{ip}?access_key={GEO_API_KEY}'
        response = requests.get(url)
        response_dict = json.loads(response.text)
        return (response_dict['latitude'], response_dict['longitude'])


    def watch_and_alert(self, interval):
        while True:
            time.sleep(interval) # change wait to 60 (sec.)
            diff = self.diff()
            print(f'Diff: {diff}.')
            if diff != 0:
                alt_diff = self.battery.discharge_by( abs(diff) ) \
                           if diff < 0 else \
                           self.battery.charge_by(diff)
                if alt_diff:
                    self.alert_server(alt_diff)

    def alert_server(self, alt_diff):
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (MAIN_FRAME_IP, MAIN_FRAME_PORT)"""
        msg_dict = {
            'type': 'alert',
            'lightning_id': self.config['lightning_id'],
            'diff': alt_diff,
            'stored': self.battery.amount_stored,
            'capacity': self.battery.capacity,
        }
        msg_json_enc = json.dumps(msg_dict).encode('UTF-8')
        print( 'Sending {!r}.'.format(msg_json_enc) )
        sent = self.sock.sendto(msg_json_enc, server_address)
            # where sent is the num of bytes sent
        """
        # receive response
        print('Awaiting response.')
        data, server = sock.recvfrom(4096)
        print(f'Got response to alert:\n{data}')
        sock.close()
        """
    def prod(self):
        return random.randint(0, 100)

    def cons(self):
        return random.randint(0, 150)

    def diff(self):
        return 20
#        return self.prod() - self.cons()

    def listen_for_energy_change(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (MAIN_FRAME_IP, MAIN_FRAME_PORT)
        while True:
            data, server = self.sock.recvfrom(4096)
            packet = json.loads(data.decode('utf-8'))
            if packet['found']:
                if packet['direction']:
                    self.route_energy(packet['amount'], packet['destination'])
                else:
                    self.accept_energy(packet['amount'], packet['destination'])

    @staticmethod
    def route_energy(to, amount):
        print(f'Routing {amount} energy units to {to}')

    @staticmethod
    def accept_energy(amount, to):
        print(f'Accepting {amount} energy units from {to}')

