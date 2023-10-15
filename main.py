# Import libraries
import time
import terminalio
import board
import gc
import analogio
import digitalio
import neopixel
import touchio
import displayio
import adafruit_ssd1680
import microcontroller

from digitalio import DigitalInOut, Direction
from adafruit_display_text import label

# Define board pinout
board_spi = board.SPI()  # Uses SCK and MOSI
board_epd_cs = board.D41
board_epd_dc = board.D40
board_epd_reset = board.D39
board_epd_busy = board.D42
enable_display = DigitalInOut(board.D16)
enable_display.direction = Direction.OUTPUT

# Define touch buttons
touch_threshold = 20000
touch_1 = touchio.TouchIn(board.D5)
touch_1.threshold = touch_threshold
touch_2 = touchio.TouchIn(board.D4)
touch_2.threshold = touch_threshold
touch_3 = touchio.TouchIn(board.D3)
touch_3.threshold = touch_threshold
touch_4 = touchio.TouchIn(board.D2)
touch_4.threshold = touch_threshold
touch_5 = touchio.TouchIn(board.D1)
touch_5.threshold = touch_threshold

# Define LED pinout
led_pin = board.D18
led_matrix = neopixel.NeoPixel(led_pin, 4, brightness = 0.1, auto_write = False)

# Define LED colors value
led_off = (0, 0, 0)
led_red = (255, 0, 0)
led_green = (0, 255, 0)
led_blue = (0, 0, 255)

# Function for CPU temperature measurement
def get_temperature():
    temperature = (microcontroller.cpu.temperature)
    time.sleep(0.15)
    return temperature

# Function for display free RAM
def get_ram():
     ram = gc.mem_free()
     ram_mb = ram
     return ram_mb

# Function to display RAM in console/terminal 
def printm(text):
    print(f"RAM {gc.mem_free()} B:\t{text}")

# Define battery pinout
vbat_voltage = analogio.AnalogIn(board.D6)
enable_battery_reading = digitalio.DigitalInOut(board.D14)
enable_battery_reading.direction = digitalio.Direction.OUTPUT
battery_reading_interval = 180 #300 # 5*60 seconds

# Function for reading the battery status
def get_voltage():
    coefficient_divisor = 2
    enable_battery_reading.value = False
    battery_pin_value = vbat_voltage.value
    enable_battery_reading.value = True
    battery_value = battery_pin_value * (3.3 / 65536)
    return battery_value * coefficient_divisor, battery_value, battery_pin_value

# First read of the value from the A/D converter "to empty"
get_voltage()

# Convert battery voltage to percentage
def get_percentage(voltage):
    min_voltage = 3.7
    max_voltage = 4.2
    percentage = max(0, min(100, (voltage - min_voltage) / (max_voltage - min_voltage) * 100))
    return percentage

# Define ePaper display resolution
display_width = 250
display_height = 122

# Define ePaper display colors value
display_black = 0x000000
display_white = 0xFFFFFF
display_color_palette = displayio.Palette(1)
display_color_palette[0] = display_white
display_background = displayio.Bitmap(display_width, display_height, 1)

# Prepare ePaper display
enable_display.value = False
displayio.release_displays()
display_bus = displayio.FourWire(
    board_spi,
    command = board_epd_dc,
    chip_select = board_epd_cs,
    reset = board_epd_reset,
    baudrate = 1000000
)
time.sleep(1)

# Configure the ePaper driver and create an ePaper display object
display = adafruit_ssd1680.SSD1680(
    display_bus,
    width = display_width,
    height = display_height,
    rotation = 270,
    busy_pin = board_epd_busy,
    seconds_per_frame=0.1,
)

# Function to set the visibility of the layer/object on the display
def set_layer_visibly(visible, parent, layer):
    try:
        if visible:
            parent.append(layer)
        else:
            parent.remove(layer)
    except ValueError:
        pass

# Function for activate layer/object
def activate_gui_layer(parent, layer):
    for _layer in parent:
        set_layer_visibly(False, parent, _layer)
    set_layer_visibly(True, parent, layer)

# Function for create text on display
def create_text_object(text, size, color, x, y):
    object = displayio.Group(scale=size, x=x, y=y)
    text_obj = label.Label(terminalio.FONT, text=text, color=color)
    object.append(text_obj)
    return object

# Create main display container
container = displayio.Group()

#-------------------------------
# Create first screen (screen1)
#-------------------------------
screen1 = displayio.Group()
screen1.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))
# # Load the image on the first screen
screen1_image = displayio.OnDiskBitmap("/img/martia1.bmp")
image_sprite = displayio.TileGrid(screen1_image, pixel_shader=screen1_image.pixel_shader)
screen1.append(image_sprite)

#-------------------------------
# Create second screen (screen2)
#-------------------------------
screen2 = displayio.Group()
screen2.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))
# Load the image on the first screen
screen2_image = displayio.OnDiskBitmap("/img/martia2.bmp")
image_sprite = displayio.TileGrid(screen2_image, pixel_shader=screen2_image.pixel_shader)
screen2.append(image_sprite)

#-------------------------------
# Create third screen (screen3)
#-------------------------------
screen3 = displayio.Group()
screen3.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))
screen3.append(create_text_object("TOTO JE", 3, display_black, 5, 20))
screen3.append(create_text_object("TRETI", 3, display_black, 5, 60))
screen3.append(create_text_object("OBRAZOVKA", 3, display_black, 5, 100))

#-------------------------------
# Create fourth screen (screen4)
#-------------------------------
screen4 = displayio.Group()
screen4.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))
# Load the first image on the first screen
screen4_image = displayio.OnDiskBitmap("/img/simonscat.bmp")
image_sprite = displayio.TileGrid(screen4_image, pixel_shader=screen4_image.pixel_shader)
screen4.append(image_sprite)

#-------------------------------
# Create fifth screen (screen5)
#-------------------------------
screen5 = displayio.Group()
screen5.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))
# Load the image on the fifth screen
screen5_image = displayio.OnDiskBitmap("/img/hwinfo.bmp")
image_sprite = displayio.TileGrid(screen5_image, pixel_shader=screen4_image.pixel_shader, x=0, y=0)
screen5.append(image_sprite)
# Add text on the fifth screen
# - section of CPU temperature measurement
screen5.append(create_text_object("CPU type:", 1, display_black, 5, 40))
screen5.append(create_text_object("ESP32-S2-WROOM", 1, display_black, 135, 40))
# - section of CPU temperature measurement
screen5.append(create_text_object("CPU temperature:", 1, display_black, 5, 55))
screen5.append(create_text_object("press button 5", 1, display_black, 135, 55))
# # - display of free RAM
screen5.append(create_text_object("Free RAM:", 1, display_black, 5, 70))
screen5.append(create_text_object("press button 5", 1, display_black, 135, 70))
# - section of battery voltage measurement
screen5.append(create_text_object("Battery voltage:", 1, display_black, 5, 85))
screen5.append(create_text_object("press button 5", 1, display_black, 135, 85))
# - section of battery percentagle
screen5.append(create_text_object("Battery percentage:", 1, display_black, 5, 100))
screen5.append(create_text_object("press button 5", 1, display_black, 135, 100))

# Set first screen as default
activate_gui_layer(container, screen5)
display.show(container)
display.refresh()

# -------------------------------------------------------------------
#                            MAIN LOOP
# -------------------------------------------------------------------

while True:
    if touch_1.value:
        printm("Press button 1")
        # Turn off the LED
        led_matrix.fill(led_off)
        led_matrix.show()
        activate_gui_layer(container, screen1) 
        display.show(container)
        display.refresh()
    if touch_2.value:
        printm("Press button 2")
        # Set LED to red
        led_matrix.fill(led_red)
        led_matrix.show()
        activate_gui_layer(container, screen2)
        display.show(container)
        display.refresh()
    if touch_3.value:
        printm("Press button 3")
        # Set LED to green
        led_matrix.fill(led_green)
        led_matrix.show()
        activate_gui_layer(container, screen3)
        display.show(container)
        display.refresh()
    if touch_4.value:
        printm("Press button 4")
        # Set LED to blue
        led_matrix.fill(led_blue)
        led_matrix.show()
        activate_gui_layer(container, screen4)
        display.show(container)
        display.refresh()
    if touch_5.value:
        printm("Press button 5")
        # Turn off the LED
        led_matrix.fill(led_off)
        led_matrix.show()
        # Measure CPU temperature
        cpu_temperature = get_temperature()
        screen5[5][0].text = str(f"{cpu_temperature:.2f} °C")
        # Display of free RAM
        free_ram = get_ram()
        screen5[7][0].text = str(f"{free_ram} B")
        # Measure battery voltage
        battery_voltage, _, _ = get_voltage()
        voltage_text = str(f"{battery_voltage:.2f} V")
        screen5[9][0].text = voltage_text
        # Display battery percentage
        battery_percentage = get_percentage(battery_voltage)
        screen5[11][0].text = str(f"{battery_percentage:.2f} %")
        activate_gui_layer(container, screen5)
        display.show(container)
        display.refresh()
