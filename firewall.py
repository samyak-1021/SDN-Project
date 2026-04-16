from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4
from pox.lib.addresses import IPAddr
import datetime

log = core.getLogger()

# Open log file (append mode)
log_file = open("firewall_log.txt", "a")

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        return

    ip_packet = packet.find('ipv4')

    if ip_packet:
        src = ip_packet.srcip
        dst = ip_packet.dstip

        log.info("Packet from %s to %s", src, dst)

        # BLOCK: h1 -> h3
        if src == IPAddr("10.0.0.1") and dst == IPAddr("10.0.0.3"):
            log.warning("Blocking traffic from h1 to h3")

            # Write to file
            log_file.write(f"{datetime.datetime.now()} | BLOCKED: {src} -> {dst}\n")
            log_file.flush()

            msg = of.ofp_flow_mod()
            msg.priority = 100
            msg.match.dl_type = 0x800  # IP
            msg.match.nw_src = src
            msg.match.nw_dst = dst
            # No actions = DROP

            event.connection.send(msg)
            return

        # ALLOWED traffic logging
        log_file.write(f"{datetime.datetime.now()} | ALLOWED: {src} -> {dst}\n")
        log_file.flush()

    # Normal Forwarding
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Firewall controller started")
