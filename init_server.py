import socket
import sys

import MySQLdb
import json
from math import radians, cos, sin, asin, sqrt

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('165.22.125.102', 5005)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

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

while True:
    conn = MySQLdb.connect(host='localhost', user='cchack', passwd='twentypasteight', db='cchack')
    c = conn.cursor()
    data, address = sock.recvfrom(4096)
    print("received {} bytes from {}".format(len(data), address))
    print(data)
    auth_data = json.loads(data.decode('utf-8'))
    c.execute("INSERT INTO device_table VALUES(NULL, '{}', {}, {}, {}, {}, {})".format(address[0], 0, 0, auth_data['mac'], auth_data['geo'][0], auth_data['geo'][1]))
    c.execute("SELECT * FROM device_table")
    auth_data['lightning_id'] = "{}".format(c.fetchall()[-1][0])
    for con in auth_data['cons']:
"""
        c.execute("SELECT * FROM  device_table WHERE ID={}".format(con))
        house = c.fetchone()

        dist = haversine(house[5], house[6], auth_data['geo'][0], auth_data['geo'][1])
"""
        c.execute("INSERT INTO device_connections VALUES(NULL, {}, {}, {})".format(auth_data['lightning_id'], con, dist))


    sock.sendto(json.dumps(auth_data).encode(), address)
    conn.commit()
    conn.close()
