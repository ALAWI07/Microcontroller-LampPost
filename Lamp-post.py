from machine import Pin
import math
import utime

f1 =0
g1 =1
a1 =2
b1 =3
f2 =4
a2 =5
b2 =6
e1 =7
d1 =8
c1 =9
e2 =10
d2 =11
g2 =12
c2 =13

#sq is a list 2D sequnes 
sq = [[a1,b1,c1,d1,e1,f1,g1],
      [a2,b2,c2,d2,e2,f2,g2]]


outputPin = Pin(sq[0][0], Pin.OUT, value=0)

#Task 2.1
# 2D sequence containing the segment signals for each digit state
segment_states = [
    [1, 1, 1, 1, 1, 1, 0],  # Digit 0
    [0, 1, 1, 0, 0, 0, 0],  # Digit 1
    [1, 1, 0, 1, 1, 0, 1],  # Digit 2
    [1, 1, 1, 1, 0, 0, 1],  # Digit 3
    [0, 1, 1, 0, 0, 1, 1],  # Digit 4
    [1, 0, 1, 1, 0, 1, 1],  # Digit 5
    [1, 0, 1, 1, 1, 1, 1],  # Digit 6
    [1, 1, 1, 0, 0, 0, 0],  # Digit 7
    [1, 1, 1, 1, 1, 1, 1],  # Digit 8
    [1, 1, 1, 1, 0, 1, 1]   # Digit 9
]


def setDigitSegments(digit, value):
    global segment_states
    # Get the segment pattern for the desired value
    segment_pattern = segment_states[value]
    
    # Define pins for each segment
    if digit is "ones":
        segment_pins = sq[1]
    elif digit is 'tens':
        segment_pins = sq[0]
    
    
    # Set or clear each segment based on the segment pattern
    for pin, state in zip(segment_pins, segment_pattern):
        if state:
            # Set the pin to HIGH (illuminate the segment)
            Pin(pin, Pin.OUT, value=1)
        else:
            # Set the pin to LOW (turn off the segment)
            Pin(pin, Pin.OUT, value=0)

# Test the function
#setDigitSegments('ones', 5)  # Display digit 5 on the ones digit

def setDisplayDigits(value):
    if value < 10 :
        ones_val = value
        tens_val = 0
        
    elif value >= 10 and value < 100:
        ones_val = value % 10
        tens_val = int(value/10)
    else:
        print("out of range")
        ones_val = 0
        tens_val = 0
    

    setDigitSegments("ones",ones_val)
    setDigitSegments("tens",tens_val)


# Test the function with different values
# setDisplayDigits(12)  # Display the number 12

def timer_function(sleep_interval):
    counter = 0
    while True:
        setDisplayDigits(counter)
        utime.sleep(sleep_interval)
        counter += 1
        if counter == 100:
            counter = 0
        
timer_function(0.3)    

#section 3


# myISR: Toggle LED pin and increment counter on ISR call
def myISR(pin):
    global countISR # ’countISR’ is declared as global despite
    print("triggered")
    countISR = countISR + increment # ’countISR’ is altered. ’increment’ is used as a constant
    
    setDisplayDigits(countISR)

 # Initialise global values, configure GPIO pins and attach interrupts
increment = 1
countISR = 0
setDisplayDigits(countISR)

button = Pin(27, Pin.IN, Pin.PULL_DOWN)
button.irq(handler=myISR, trigger=Pin.IRQ_RISING)

 # Reset counter when it reaches 10
while True:
     if countISR >= 10:
         countISR = 0