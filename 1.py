from mininet.topo import Topo

def diamond_size(l):
	def rec(i):
		if i != 0:
			return 2**i + rec(i - 1)
		return 0
	return int(rec(l) - 2**(l-1))

class T(Topo):
	def __init__ (self, hosts, level):
		Topo.__init__(self)
		self.level = level
		self.qhs = hosts
		self.qsw = diamond_size(self.level)
		self.sws()
		self.hs()
		self.link()

	def _h(self, i):
		return "h"+str(i)

	def _sw(self, i):
		return "sw"+str(i)

	def hs(self):
		for h in map(lambda i: self._h(i), range(self.qhs)):
			self.addHost(h)

	def sws(self):
		for s in map(lambda i: self._sw(i), range(self.qsw)):
			self.addSwitch(s)

	def link(self):
		half = self.qhs//2
		for i in xrange(self.qhs):
			if i < half:
				self.addLink(self._sw(0), self._h(i))
			else:
				self.addLink(self._sw(self.qsw-1), self._h(i))

		if self.level > 1:
			n = map(lambda i: self._sw(i), range(1, 2**self.level -1))[::-1]
			b = map(lambda i: self._sw(i), range(self.qsw-(2**self.level)+1, self.qsw-1))
			if self.level > 2:
				f = n[-(2**(self.level-1)-2):]
				l = b[-(2**(self.level-1)-2):]
			else:
				f = []
				l = []

			f.append(self._sw(0))
			f = f[::-1]
			l.append(self._sw(self.qsw - 1))
			l = l[::-1]

			for sw in f:
				self.addLink(sw, n.pop())
				self.addLink(sw, n.pop())

			for sw in l:
				self.addLink(sw, b.pop())
				self.addLink(sw, b.pop())

topos = { 't': T }
