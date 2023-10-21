My CircuitPython code for electronic business card [Maker Badge](https://www.makermarket.cz/maker-badge/).

---

![https://github.com/NetCzech/maker-badge/blob/3e36630f7859b08d106f8034f60413f942338f33/_makerPict/CircuitPython__logo.png](https://github.com/NetCzech/maker-badge/blob/3e36630f7859b08d106f8034f60413f942338f33/_makerPict/CircuitPython__logo.png)

---
> **CircuitPython for Maker Badge:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[https://circuitpython.org/board/maker_badge/](https://circuitpython.org/board/maker_badge/)
---

### **More edits main.py*:*

> 1. :memo: **Setting the color of individual LEDs:**
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- define colors in the program as needed

```python
    if touch_1.value:
        printm("Press button 1")
        # Turn off the LED
        led_matrix[0](<your_color)
        led_matrix[1](<your_color)
        led_matrix[2](<your_color)
        led_matrix[3](<your_color)
        led_matrix.show()
        activate_gui_layer(container, screen1) 
        display.show(container)
        display.refresh()
```

&nbsp;
&nbsp;

> 2. :memo: **The LEDs flashes when the button is pressed**

```python
# Define LED blink
def led_blink(pin, count):
    for _ in range(count):
        led_matrix.fill((led_blue))
        led_matrix.show()
        time.sleep(0.25)
        led_matrix.fill((led_off))
        led_matrix.show()
        time.sleep(0.25)
```
```python
    if touch_1.value:
        printm("Press button 1")
        activate_gui_layer(container, screen1)
        display.show(container)
        display.refresh()
        led_blink(board.D18, 10)
```

---

### **Maker Badge:**

Maker Badge is primarily meant to be a name tag on actions such as Maker Faire, where you want to simply tell someone your name, the name of your company or the company you work for. But it is also a full -fledged development board, on which you can prototyte your projects in CircuitPython, Micropython or Arduino.

![https://github.com/NetCzech/maker-badge/blob/20c657af727cb02ffeea53f4066178e163fabe98/_makerPict/maker_badge.jpg](https://github.com/NetCzech/maker-badge/blob/20c657af727cb02ffeea53f4066178e163fabe98/_makerPict/maker_badge.jpg)

---
> **GitHub:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[https://github.com/makerfaireczech/maker_badge](https://github.com/makerfaireczech/maker_badge)

> **www:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[https://www.makermarket.cz](https://www.makermarket.cz)

> **Buy:**&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[https://www.makermarket.cz/maker-badge/](https://www.makermarket.cz/maker-badge/)
---

