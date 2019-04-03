import time
import logging
import threading
from digi.xbee.io import IOLine, IOMode, IOValue


class Peer:

    def __init__(self, device):
        self.device = device
        self.tasks = []
        self.run = True
        logging.info("New peer: {}-{}".format(self.device.get_node_id(), self.device.get_64bit_addr()))

    def light_off(self):
        try:
            self.device.set_dio_value(IOLine.DIO1_AD1, IOValue.HIGH)
            self.device.set_dio_value(IOLine.DIO2_AD2, IOValue.LOW)
        except:
            logging.warn("Error")

    def light_on(self):
        try:
            self.device.set_dio_value(IOLine.DIO1_AD1, IOValue.LOW)
            self.device.set_dio_value(IOLine.DIO2_AD2, IOValue.HIGH)
        except:
            logging.warn("Error")

    def listen_from_ad(self, AD):
        def read_digital_task():
            while self.run:
                logging.info("[{}] {}".format(
                    self.device.get_64bit_addr(),
                    self.device.get_dio_value(AD)
                ))
                time.sleep(0.2)

        self.device.set_io_configuration(AD, IOMode.DIGITAL_IN)
        task = threading.Thread(target=read_digital_task)
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
