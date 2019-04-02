import time
import argparse
import logging
import threading
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue

BAUD_RATE = 9600
IOLINE_IN = IOLine.DIO0_AD0

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.getLogger("digi").setLevel(logging.WARNING)  # disable logging for digi module

class Peer:

    def __init__(self, device):
        self.device = device
        self.tasks = []
        self.run = True
        logging.info("New peer: {}-{}".format(self.device.get_node_id(), self.device.get_64bit_addr()))
    
    def light_off(self):
        try:
            self.device.set_dio_value(IOLine.DIO1_AD1, IOValue.HIGH)
        except:
            logging.warn("Error")
    
    def light_on(self):
        try:
            self.device.set_dio_value(IOLine.DIO1_AD1, IOValue.LOW)
        except:
            logging.warn("Error")
    
    def listen_from_ad(self, AD):
        def read_adc_task():
            while self.run:
                logging.info("[{}] {}".format(
                    self.device.get_64bit_addr(),
                    self.device.get_dio_value(AD)
                ))
                time.sleep(0.2)

        self.device.set_io_configuration(AD, IOMode.DIGITAL_IN)
        task = threading.Thread(target=read_adc_task)
        self.tasks.append(task)
        task.start()

    def stop_all_task(self):
        """
            stop all thread
        """
        self.run = False
        for task in self.tasks:
            if task.isAlive():
                task.join()



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
                msg.data.decode()
            ))
        self.device.add_data_received_callback(recv_callback)

    def listen_remote_event(self):
        """
            Listen remote event
        """
        for peer in self.peers:
            peer.listen_from_ad(IOLINE_IN)
        self.__listen_remote_data()
    
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Prism')
    parser.add_argument('--port', help="com port")

    args = parser.parse_args()
    commander = Commander(args.port)

    commander.discover_peer()
    #commander.listen_remote_event()
    commander.light_play()

    input()

    #commander.stop_all_task()
