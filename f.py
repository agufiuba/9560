from pox.core import core
import pox.openflow.libopenflow_01 as openflow
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
import pox.lib.packet as pkt

log = core.getLogger ()

h1mac = EthAddr('00:00:00:00:00:02')
h2mac = EthAddr('00:00:00:00:00:03')
h3mac = EthAddr('00:00:00:00:00:04')

class Firewall(EventMixin):

	def __init__(self):
		self.listenTo(core.openflow)

	def _handle_ConnectionUp(self, e):
		b = openflow.ofp_match()
		b2 = openflow.ofp_match()
		b.dl_src = h2mac
		b.dl_dst = h3mac
		b2.dl_src = h3mac
		b2.dl_dst = h2mac
		fm = openflow.ofp_flow_mod()
		fm.match = b
		e.connection.send(fm)
		fm.match = b2
		e.connection.send(fm)

	def _handle_PacketIn (self, e):
		p = e.parsed.find('ipv4')
		if not p: return

		e.halt = self._block80(p)
		if e.halt:
			log.debug('Paquete al 80, BLOQUEADO!')
		else:
			e.halt = self._blockH1UDP5001(p, e)
			if e.halt:
				log.debug('Paquete proveniente del H1 por UDP al 5001, BLOQUEADO!')

	def _block80 (self, p):
		return p.protocol != pkt.ipv4.ICMP_PROTOCOL and p.payload.dstport == 80

	def _blockH1UDP5001 (self, p, e):
		return p.protocol == pkt.ipv4.UDP_PROTOCOL and p.payload.dstport == 5001 and e.parsed.src == h1mac

def launch():
	core.registerNew(Firewall)
