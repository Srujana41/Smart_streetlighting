import RPi.GPIO as GPIO
import time

pir= 3
led = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

GPIO.output(led,False)
print ("Initialzing PIR Sensor......")
time.sleep(1)
print ("PIR Ready...")


try:
   pir_data = GPIO.input(pir)
   print(pir_data)
   while True:
      if (pir_data == 1):
          GPIO.output(led,GPIO.HIGH)
          print ("Motion Detected")
          while GPIO.input(pir):
              time.sleep(0.2)
      else:
          GPIO.output(led,GPIO.LOW)


except KeyboardInterrupt:
    GPIO.cleanup()

