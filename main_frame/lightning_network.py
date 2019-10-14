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
	def add(self, dev1, dev2, distance):
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

	def algo(self, node):
		lookup = self.network[node].diff
		if lookup == 0:
			return None
		visited = []
		toVisit = []
		toVisit.append(node)
		while toVisit:
			var = toVisit.pop(0)
			print(visited)
			if var in visited:
				continue
			visited.append(var)
			comp = self.network[var].diff
			print("{} -> {} : {} -> {}".format(node, var, lookup, comp))
			if (lookup < 0 and comp > 0 and comp + lookup >= 0) or (lookup > 0 and comp < 0 and comp + lookup <= 0) and node != var:
				return var
			print(self.network[var].neigh)
			for n in self.network[var].neigh:
				modn = n[0]
				toVisit.append(modn)
				


