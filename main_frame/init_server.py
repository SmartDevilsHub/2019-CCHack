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
from queue import Queue
import threading
from lightning_network import LightningNode, LightningNetwork


init_queue = Queue()
alert_queue = Queue()
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
            queue_item = init_queue.pop()
            auth_data = queue_item[0]
            c.execute(
                "INSERT INTO device_table VALUES(NULL, '{}', {}, {}, {}, {}, {})".format(
                    queue_item[1][0], # ip
                    auth_data['mac'], # mac
                    auth_data['geo'][0], # long
                    auth_data['geo'][1], # lat
                    queue_item[1][1] # port
                )
            )
            c.execute("SELECT * FROM device_table")
            auth_data['lightning_id'] = "{}".format(c.fetchall()[-1][0])
            for con in auth_data['cons']:
                try:
                    c.execute("SELECT * FROM  device_table WHERE ID={}".format(con))
                    house = c.fetchone()

                    dist = haversine(house[5], house[6], auth_data['geo'][0], auth_data['geo'][1])
                    c.execute("INSERT INTO device_connections VALUES(NULL, {}, {}, {})".format(auth_data['lightning_id'], con, dist))
                    light_net.add(auth_data['lightning_id'], con, dist)

                except Exception as e:
                    print(e)

            sock.sendto(json.dumps(auth_data).encode(), queue_item[1]) # sending new config file with lightning_id
            conn.commit()
            conn.close()

def alert_processor():
    while True:
        if alert_queue:
            queue_item = alert_queue.pop()
            auth_data = queue_item[0]

            light_net.network[auth_data['lightning_id']].diff = auth_data['diff']
            second_node = light_net.algo(auth_data['lightning_id'])
            if auth_data > 0:
                direc = True
            else:
                direc = False
            pack_to_send = {"destination": second_node, "found": bool(second_node), "direction": direc, "amount": auth_data['diff']}
            sock.sendto(json.dumps(pack_to_send).encode(), queue_item[1])
            if second_node:
                 print("second node found")
                 conn = MySQLdb.connect(host='localhost', user='cchack', passwd='twentypasteight', db='cchack')
                 c = conn.cursor()
                 c.execute("SELECT IP, PORT FROM device_table WHERE ID={}".format(second_node))
                 address = c.fetchone()
                 pack_to_send = {"destination": auth_data['lightning_id'], "found": True, "direction": (not direc), "amount": auth_data['diff']}
                 sock.sendto(json.dumps(pack_to_send).encode(), address)
                 print("sent {}".format(pack_to_send))

init_thread = threading.Thread(target=init_processor)
alert_thread = threading.Thread(target=alert_processor)
init_thread.start()
alert_thread.start()


while True:
    data, address = sock.recvfrom(4096)
    print("{} recieved".format(data))
    json_data = json.loads(data.decode("utf-8"))
    if json_data['type'] == "init":
        init_queue.push( (json_data, address) )
    elif json_data['type'] == "alert":
        alert_queue.push( (json_data, address) )
    print(init_queue)
    print(alert_queue)
