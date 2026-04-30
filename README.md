# DIY spectrophotometer

The instrument for which this was built uses a Raspberry Pi Zero W to control a stepper motor via a driver on the GPIO pins

Data is acquired through a photodiode outputting an analog voltage, which the RPi reads through an ADC communicating over I2C

A desktop or laptop computer is used to control the RPi and to receive the data

The RPi must be free to scp files to the computer


led.py is a simple program on the RPi that turns on an external LED when the RPi is ready to be signed into by secure shell after reboot

photodiode.py is a simple program on the RPi that monitors the output voltage from the photodiode and presents it in a simple graphical form

spectrophotometer.py must be running on the RPi to use the spectrophotometer


spectrophotometer_control.py is run on the controlling computer to trigger the spectrophotometer to read a spectrum (or obtain a blank reading); after a spectrum has been obtained, it automatically creates an absorbance vs. motor position plot

spectrum_compare.py allows the user to select multiple spectra to open at once and compare them

Please feel free to use this "terrible python code" as the foundation for your own projects; I can't wait to see what you come up with!

Soli Deo Gloria!

Ethan S
