import time
import logging
import websockets
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from .peer import Peer

BAUD_RATE = 9600
IOLINE_IN = IOLine.DIO0_AD0


class Commander:

    def __init__(self, comPort):
        self.device = XBeeDevice(comPort, BAUD_RATE)
        self.network = None
        self.peers = []
        self.run = True
        self.device.open()
        logging.info("Commander address: {}".format(self.device.get_64bit_addr()))

    def discover_peer(self):
        """
            Search other connected device to the same Zigbee network
        """
        logging.info("Starting discovering peer")
        if self.network is None:
            self.network = self.device.get_network()
        self.network.set_discovery_timeout(15)
        self.network.clear()

        self.network.add_device_discovered_callback(lambda peer: self.peers.append(Peer(peer)))
        self.network.start_discovery_process()

        while self.network.is_discovery_running():
            time.sleep(1)
        logging.info("Discovered: {} peers".format(len(self.peers)))

    def __listen_remote_data(self):
        def recv_callback(msg):
            logging.info("[{}] {}".format(
                msg.remote_device.get_64bit_addr(),
                msg.data.decode()))

        self.device.add_data_received_callback(recv_callback)

    def listen_remote_event(self):
        """
            Listen remote event
        """
        for peer in self.peers:
            peer.listen_from_ad(IOLINE_IN)
        #self.__listen_remote_data()

    def light_play(self):
        while True:
            for peer in self.peers:
                peer.light_on()
            time.sleep(2)
            for peer in self.peers:
                peer.light_off()
            time.sleep(2)

    def __del__(self):
        for peer in self.peers:
            peer.stop_all_task()
        if self.device.is_open():
            self.device.close()