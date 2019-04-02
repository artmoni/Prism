import time
import argparse
from digi.xbee.devices import XBeeDevice
# from digi.xbee.io import IOLine, IOMode

BAUD_RATE = 9600
# IOLINE_IN = IOLine.DIO1_AD1


class Commander:

    def __init__(self, comPort):
        self.device = XBeeDevice(comPort, BAUD_RATE)
        self.network = None
        self.peers = []
        self.device.open()

    def discover_peer(self):
        if self.network is None:
            self.network = self.device.get_network()
        self.network.set_discovery_timeout(15)
        self.network.clear()

        self.network.add_device_discovered_callback(lambda peer: self.peers.append(peer))
        self.network.start_discovery_process()

        while self.network.is_discovery_running():
            time.sleep(1)
        print("Discovered: {} peers".format(len(self.peers)))

    def listen_remote_event(self):
        def rcv_callback(msg):
            print("[{}] {}".format(
                msg.remote_device.get_64bit_addr(),
                msg.data.decode()
            ))

        self.device.add_data_received_callback(rcv_callback)

    def __del__(self):
        if self.device.is_open():
            self.device.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prism')
    parser.add_argument('--port', help="com port")

    args = parser.parse_args()
    commander = Commander(args.port)

    commander.discover_peer()
    commander.listen_remote_event()
