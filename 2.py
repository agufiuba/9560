from mininet.topo import Topo

class T(Topo):
	def __init__ (self, qsw):
		Topo.__init__(self)
		self.qhs = 4
		self.qsw = qsw
		self.sws()
		self.hs()
		self.link()

	def _h(self, i):
		return "h"+str(i)

	def _sw(self, i):
		return "sw"+str(i)

	def hs(self):
		for h in map(lambda i: self._h(i), xrange(self.qhs)):
			self.addHost(h)

	def sws(self):
		for s in map(lambda i: self._sw(i), xrange(self.qsw)):
			self.addSwitch(s)

	def link(self):
		half = self.qhs//2
		for i in xrange(self.qhs):
			if i < half:
				self.addLink(self._sw(0), self._h(i))
			else:
				self.addLink(self._sw(self.qsw-1), self._h(i))

		for i in range(self.qsw-1):
			self.addLink(self._sw(i), self._sw(i+1))

topos = { 't': T }
