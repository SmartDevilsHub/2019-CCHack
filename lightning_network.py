#import HashMap

import MySQLdb

class LightningNode:
	def __init__(self):
		self.diff = 0
		self.neigh = []
	def push_value(self, id, distance):
		self.neigh.append((id, distance))
	def print(self):
		for t_id, dist in self.neigh:
			print("({} {}) ".format(t_id, dist))
		print("\n")

class LightningNetwork:
	def __init__(self):
		self.network = {}
		conn = MySQLdb.connect(host='localhost', user='cchack', passwd='twentypasteight', db='cchack')
		c = conn.cursor()
		c.execute("SELECT * FROM device_connections")
		ret = c.fetchall()
		for table_id, dev1, dev2, distance in ret:
			if dev1 not in self.network:
				self.network[dev1] = LightningNode()
			self.network[dev1].push_value(dev2, distance)
			if dev2 not in self.network:
				self.network[dev2] = LightningNode()
			self.network[dev2].push_value(dev1, distance)
	def print_everything(self):
		for key in self.network:
			print("{} : ".format(key))
			self.network[key].print()
		print(self.network.keys());


ln = LightningNetwork()
ln.print_everything()
