import socket
import sys

import MySQLdb
import json
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

from _thread import *
import threading
from lightning_network import LightningNode, LightningNetwork


init_queue = []
alert_queue = []
light_net = LightningNetwork()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('165.22.125.102', 5005)
sock.bind(server_address)

def init_processor():
    while True:
        if init_queue:
            print("going")
            conn = MySQLdb.connect(host='localhost', user='cchack', passwd='twentypasteight', db='cchack')
            c = conn.cursor()
            auth_data = init_queue[0][0]
            c.execute("INSERT INTO device_table VALUES(NULL, '{}', {}, {}, {}, {}, {})".format(init_queue[0][1][0], 0, 0, auth_data['mac'], auth_data['geo'][0], auth_data['geo'][1]))
            c.execute("SELECT * FROM device_table")
            auth_data['lightning_id'] = "{}".format(c.fetchall()[-1][0])
            for con in auth_data['cons']:
                try:
                    c.execute("SELECT * FROM  device_table WHERE ID={}".format(con))
                    house = c.fetchone()

                    dist = haversine(house[5], house[6], auth_data['geo'][0], auth_data['geo'][1])
                    c.execute("INSERT INTO device_connections VALUES(NULL, {}, {}, {})".format(auth_data['lightning_id'], con, dist))

                except Exception as e:
                    print(e)

            sock.sendto(json.dumps(auth_data).encode(), init_queue[0][1])
            conn.commit()
            conn.close()
            del init_queue[0]

def alert_processor():
    while True:
        if alert_queue:
            auth_data = alert_queue[0][0]
            print("{} {} {}".format(auth_data['diff'], auth_data['stored'], auth_data['lightning_id']))
            sock.sendto(json.dumps(auth_data).encode(), alert_queue[0][1])
            del alert_queue[0]

init_thread = threading.Thread(target=init_processor)
alert_thread = threading.Thread(target=alert_processor)
init_thread.start()
alert_thread.start()


while True:
    data, address = sock.recvfrom(4096)
    print("{} recieved".format(data))
    json_data = json.loads(data.decode("utf-8"))
    if json_data['type'] == "init":
        init_queue.append((json_data, address))
    elif json_data['type'] == "alert":
        alert_queue.append((json_data, address))
    print(init_queue)
    print(alert_queue)
