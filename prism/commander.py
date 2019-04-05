import time
import logging
import asyncio
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue
from threading import Lock
from .peer import Peer

BAUD_RATE = 9600
IOLINE_IN = IOLine.DIO0_AD0

BTN_ONE = IOLine.DIO0_AD0
BTN_TWO = IOLine.DIO5_AD5
BTN_THREE = IOLine.DIO4_AD4


CODE = [BTN_ONE, BTN_TWO, BTN_THREE]


class Commander:

    def __init__(self, comPort):
        self.device = XBeeDevice(comPort, BAUD_RATE)
        self.network = None
        self.peers = []
        self.lock = Lock()
        self.run = True
        self.device.open()
        self.code = CODE
        self.on_success = None
        self.on_error = None
        logging.info("Commander address: {}".format(self.device.get_64bit_addr()))
    
    def set_on_error(self, callback):
        self.on_error = callback
    
    def set_on_success(self, callback):
        self.on_success = callback

    @asyncio.coroutine
    def discover_peer(self):
        """
            Search other connected device to the same Zigbee network
        """
        def push_peer(conn):
            peer = Peer(conn)
            if peer not in self.peers:
                logging.info("New peer: {}".format(peer))
                self.lock.acquire()
                self.peers.append(peer)
                self.lock.release()

        if self.network is None:
            self.network = self.device.get_network()
        self.network.set_discovery_timeout(25.5)
        self.network.clear()

        self.network.add_device_discovered_callback(push_peer)
        while self.run:
            logging.info("running network scan...")
            try:
                self.network.start_discovery_process()

                while self.network.is_discovery_running():
                    yield from asyncio.sleep(1)
            except:
                pass
            yield from asyncio.sleep(60)

    def light_red(self):
        self.lock.acquire()
        for peer in self.peers:
            peer.light_red()
        self.lock.release()

    def light_blue(self):
        self.lock.acquire()
        for peer in self.peers:
            peer.light_blue()
        self.lock.release()

    def light_green(self):
        self.lock.acquire()
        for peer in self.peers:
            peer.light_green()
        self.lock.release()

    def listen_remote(self):
        def data_recv_callback(msg):
            logging.info("[{}] {}".format(
                msg.remote_device.get_64bit_addr(),
                msg.data.decode()))
        
        def samples_recv_callback(sample, remote, time):

            remote = Peer(remote)

            def check(btn):
                if len(self.code) > 0 and self.code[0] == btn:
                    self.code.pop()
                else:
                    self.code = CODE
                    remote.light_red()
                    self.on_error()

            logging.info("[{}] {}".format(remote.get_addr(), sample))

            if sample.get_digital_value(BTN_ONE) == IOValue.HIGH:
                check(BTN_ONE)
            elif sample.get_digital_value(BTN_TWO) == IOValue.HIGH:
                check(BTN_TWO)
            elif sample.get_digital_value(BTN_THREE) == IOValue.HIGH:
                check(BTN_THREE)
            if len(self.code) == 0:
                self.code = CODE
                remote.light_green()
                self.on_success()
                

        self.device.add_data_received_callback(data_recv_callback)
        self.device.add_io_sample_received_callback(samples_recv_callback)

    def __del__(self):
        for peer in self.peers:
            peer.stop_all_task()
        if self.device.is_open():
            self.device.close()