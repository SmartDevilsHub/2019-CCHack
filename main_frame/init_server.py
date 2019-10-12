import socket
import sys

import MySQLdb
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('165.22.125.102', 5005)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    conn = MySQLdb.connect(host='localhost', user='cchack', passwd='twentypasteight', db='cchack')
    c = conn.cursor()
    data, address = sock.recvfrom(4096)
    print("received {} bytes from {}".format(len(data), address))
    print(data)
    auth_data = json.loads(data.decode('utf-8'))
    c.execute("INSERT INTO device_table VALUES(NULL, '{}', {}, {}, {})".format(address[0], 0, 0, auth_data['mac']))
    conn.commit()
    c.execute("SELECT * FROM device_table")
    auth_data['lightning_id'] = "{}".format(c.fetchall()[-1][0])
    sock.sendto(json.dumps(auth_data).encode(), address)
    conn.close()


