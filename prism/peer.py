import time
import logging
import threading
from digi.xbee.io import IOLine, IOMode, IOValue

LED_RED = IOLine.DIO3_AD3
LED_GREEN = IOLine.DIO2_AD2
LED_BLUE = IOLine.DIO1_AD1

class Peer:

    def __init__(self, device):
        self.device = device
        self.tasks = []
        self.run = True
    
    def __repr__(self):
        return "{}-{}".format(self.device.get_node_id(), self.get_addr())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_addr() == other.get_addr()

    def light_red(self):
        try:
            self.device.set_dio_value(LED_RED, IOValue.LOW)
            self.device.set_dio_value(LED_GREEN, IOValue.HIGH)
            self.device.set_dio_value(LED_BLUE, IOValue.HIGH)
        except:
            logging.warn("Error")

    def light_green(self):
        try:
            self.device.set_dio_value(LED_RED, IOValue.HIGH)
            self.device.set_dio_value(LED_GREEN, IOValue.LOW)
            self.device.set_dio_value(LED_BLUE, IOValue.HIGH)
        except:
            logging.warn("Error")

    def light_blue(self):
        try:
            self.device.set_dio_value(LED_RED, IOValue.HIGH)
            self.device.set_dio_value(LED_GREEN, IOValue.HIGH)
            self.device.set_dio_value(LED_BLUE, IOValue.LOW)
        except:
            logging.warn("Error")
        
    def get_addr(self):
        return self.device.get_64bit_addr()

    def listen_btn(self):
        def read_digital_task(ad):
            while self.run:
                try:
                    logging.info("[{}] {} {}".format(
                        self.device.get_64bit_addr(),
                        ad,
                        self.device.get_dio_value(ad)
                    ))
                    time.sleep(0.2)
                except:
                    pass
        
        def create_task(ad):
            print(ad)
            #self.device.set_io_configuration(ad, IOMode.DIGITAL_IN)
            task = threading.Thread(target=read_digital_task, args=[ad])
            self.tasks.append(task)
            task.start()
        
        create_task(BTN_ONE)
        create_task(BTN_TWO)
        create_task(BTN_THREE)

    def stop_all_task(self):
        """
            stop all thread
        """
        self.run = False
        for task in self.tasks:
            if task.isAlive():
                task.join()
