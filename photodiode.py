from ADCDifferentialPi import ADCDifferentialPi
import time

adc = ADCDifferentialPi(0x68, 0x68, 18)

while True:
	voltage = adc.read_voltage(1)
	bar = int ((abs(adc.read_voltage(1)) - 0) * 8192)
	print(f"{voltage:.6f} V","█" * bar)
	#time.sleep(.5)
