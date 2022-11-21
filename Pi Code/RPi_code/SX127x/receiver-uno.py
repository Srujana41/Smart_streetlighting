import sys 

#Change the path to the location where the below imported python files are present
sys.path.insert(0, '../../RPi_code')  

from SX127x.LoRa import *

from SX127x.LoRaArgumentParser import LoRaArgumentParser

from SX127x.board_config import BOARD

import RPi.GPIO as GPIO

'''parser = LoRaArgumentParser("A simple LoRa beacon")
parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")'''


BOARD.setup()

class LoRaRcvCont(LoRa):

    def __init__(self, verbose=False):

        super(LoRaRcvCont, self).__init__(verbose)

        self.set_mode(MODE.SLEEP)

        self.set_dio_mapping([0] * 6)


    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3,GPIO.IN)
        self.reset_ptr_rx()

        self.set_mode(MODE.RXCONT)
        
        print("Receiving data on 433MHz")
        time.sleep(.5)

        #rssi_value = self.get_rssi_value()

        #status = self.get_modem_status()

        sys.stdout.flush()
        pir_data = GPIO.input(3)
        print(pir_data)
        while True:
            if (GPIO.input(3) == 1):
                self.set_mode(MODE.TX)
                print("Transmitting")
            else:
                self.on_rx_done()
                print("Receiving")
            


    def on_rx_done(self):
        #print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        
        data = ''.join([chr(c) for c in payload])
        print(data)
        while data:
            print("Packet received")
            
            if (data[0] in {'1','2','3','4'}):
                loc = data[1:]
                print("Fault in Node "+str(data[0])+"at: "+loc)
                #global args
                self.set_mode(MODE.STDBY)
                self.clear_irq_flags(TxDone=1)
                sys.stdout.flush()
                data_sent = [int(hex(ord(c)), 0) for c in data]
                self.write_payload(data_sent)
                print("Message sent to G1!")
            elif (data == "0003" or data == "01111"):
            print("Object detected by previous nodes. Turning on led!")
            BOARD.led_on();
            time.sleep(5);
            BOARD.led_off();
            elif (data == "002"):
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                if (current_time > '18:00:00' or current_time < '06:00:00'):
                    GPIO.output(13, GPIO.HIGH)
                    time.sleep(5)
                    GPIO.output(13, GPIO.LOW)
                    if (GPIO.input(3) == 1):
                        self.on_tx_done()
            elif (data[0] == 'G' ):
                print("Packet received from GW "+ data[1])
                print("Fault in Node "+data[2]+" at: "+data[3:])
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        data = "01111"
        print(data)
        #self.write_payload([0x0f])
        data_sent = [int(hex(ord(c)), 0) for c in data]
        self.write_payload(data_sent)
        print("\nTxDone")
        #self.set_mode(MODE.SLEEP)
        #self.reset_ptr_rx()
        #self.set_mode(MODE.RXCONT)
        self.set_mode(MODE.TX)
lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)


#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm


lora.set_pa_config(pa_select=1)


try:
    lora.start()

except KeyboardInterrupt:

    sys.stdout.flush()

    print("")

    sys.stderr.write("KeyboardInterrupt\n")

finally:

    sys.stdout.flush()

    print("")

    lora.set_mode(MODE.SLEEP)

    BOARD.teardown()


lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)

assert(lora.get_agc_auto_on() == 1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

