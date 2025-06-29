# Kill all Python processes
sudo pkill -f python

# Reset all GPIO pins
sudo python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for pin in [17, 27, 22, 23]:
    try:
        GPIO.setup(pin, GPIO.IN)
        GPIO.cleanup(pin)
    except:
        pass
GPIO.cleanup()
"

# Wait a moment
sleep 2

# Now test
python3 test_buttons.py# Kill all Python processes
sudo pkill -f python

# Reset all GPIO pins
sudo python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for pin in [17, 27, 22, 23]:
    try:
        GPIO.setup(pin, GPIO.IN)
        GPIO.cleanup(pin)
    except:
        pass
GPIO.cleanup()
"

# Wait a moment
sleep 2

# Now test
python3 test_buttons.py