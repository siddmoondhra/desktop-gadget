import time
import os

# Test using the sysfs GPIO interface (more reliable)
def setup_gpio_pin(pin):
    # Export the pin
    try:
        with open('/sys/class/gpio/export', 'w') as f:
            f.write(str(pin))
    except:
        pass  # Pin might already be exported
    
    time.sleep(0.1)
    
    # Set as input
    with open(f'/sys/class/gpio/gpio{pin}/direction', 'w') as f:
        f.write('in')

def read_gpio_pin(pin):
    try:
        with open(f'/sys/class/gpio/gpio{pin}/value', 'r') as f:
            return int(f.read().strip())
    except:
        return -1

# Test your pins
pins = {
    'up': 17,      # Grey wire
    'down': 27,    # Black wire  
    'select': 22,  # Brown wire
    'back': 23     # Purple wire
}

print("Setting up GPIO pins...")
for name, pin in pins.items():
    setup_gpio_pin(pin)
    print(f"Setup {name} on GPIO {pin}")

print("\nReading pins (should be 1 normally, 0 when pressed):")
print("Press Ctrl+C to exit")

try:
    while True:
        for name, pin in pins.items():
            value = read_gpio_pin(pin)
            if value == 0:  # Button pressed
                print(f"{name} button pressed (GPIO {pin})")
                time.sleep(0.3)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\nCleaning up...")
    for name, pin in pins.items():
        try:
            with open('/sys/class/gpio/unexport', 'w') as f:
                f.write(str(pin))
        except:
            pass