import time
import argparse
import logging
import threading
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode

BAUD_RATE = 9600
IOLINE_IN = IOLine.DIO1_AD1

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Commander:

    def __init__(self, comPort):
        self.device = XBeeDevice(comPort, BAUD_RATE)
        self.network = None
        self.peers = []
        self.run = True
        self.tasks = []
        self.device.open()
        logging.info("Commander address: {}".format(self.device.get_64bit_addr()))

    def discover_peer(self):
        def discover_callback(peer):
            logging.info("New peer: {}".format(peer.get_64bit_addr()))
            self.peers.append(peer)

        logging.info("Starting discovering peer")
        if self.network is None:
            self.network = self.device.get_network()
        self.network.set_discovery_timeout(15)
        self.network.clear()

        self.network.add_device_discovered_callback(discover_callback)
        self.network.start_discovery_process()

        while self.network.is_discovery_running():
            time.sleep(1)
        logging.info("Discovered: {} peers".format(len(self.peers)))

    def stop_all_task(self):
        self.run = False
        for task in self.tasks:
            if task.isAlive():
                task.join()

    def listen_remote_event(self):
        def read_adc_task(peer):
            while True:
                logging.info("[{}] {}".format(
                    peer.get_64bit_addr(),
                    peer.get_adc_value(IOLINE_IN)
                ))
                time.sleep(0.2)
        for peer in self.peers:
            peer.set_io_configuration(IOLINE_IN, IOMode.ADC)
            self.tasks.append(threading.Thread(target=read_adc_task, args=[peer]))
        
        for task in self.tasks:
            task.start()


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

    input()

    commander.stop_all_task()