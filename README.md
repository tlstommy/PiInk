#

<h1 align="center">PiInk - A Raspberry Pi Powered E-Ink Picture Frame </h1>

![image](https://github.com/tlstommy/PiInk/assets/36305669/626a897f-e623-4cc2-a8d9-015e7bd3f8fa)

### An open-source, low-power, digital picture frame powered by a Raspberry Pi that gives images a natural aesthetic due to its E-Ink Display.

- **Web Ui**: Built-in Web UI to control PiInk and upload images over the network.
- **Low Power**: The E-Ink display does not require power to continually display images, allowing pictures on the frame to persist
- **Natural Aesthetic**: The lack of a backlight and the nature of E-Ink technology allows images displayed on PiInk to resemble images printed on paper.
- **Open Source**: PiInk has a MIT License, so feel free to modify it however you want!

## Installation

To install, clone the repository, run the install script, and follow the script's installation instructions.

```bash
git clone https://github.com/tlstommy/PiInk.git
cd PiInk
sudo bash install

```
## Parts List

**The PiInk 3D printed mount was designed to work with the Raspberry Pi Zero family but the software should work with any Raspberry Pi model.**

You can buy a Pi Zero from websites like [Adafruit](https://www.adafruit.com/category/105) or [Pimironi](https://shop.pimoroni.com/collections/raspberry-pi). 

### E-Ink Display

**You will need one Pimironi Inky Impression. They come in 3 different sizes: 4". 5.7" & 7.3". You can purchase them at the links below.**

- **[Inky Impression - 4 Inches](https://shop.pimoroni.com/products/inky-impression-4)**
- **[Inky Impression - 5.7 Inches](https://shop.pimoroni.com/products/inky-impression-5-7)**
- **[Inky Impression - 7.3 Inches](https://shop.pimoroni.com/products/inky-impression-7-3)**

The mounting hardware that comes included with the Inky Impression will be used to secure it to the 3D-printed stand.

### 3D Printed Stand

The [STL folder](https://github.com/tlstommy/PiInk/tree/main/STL) contains 3D printable stand files for the frame. These can also be found on [Printables.com]().

There is a different stand for each size of E-Ink display, use the table below to find the appropriate one.

| E-Ink Display | STL file|
| ------------- |:-------------:|
|Inky Impression - 4.0 Inches| [PiInk_stand_4_Inch.stl](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_4_Inch.stl) |
|Inky Impression - 5.7 Inches| [PiInk_stand_5.7_Inch.stl](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_5.7_Inch.stl) |
|Inky Impression - 7.3 Inches| [PiInk_stand_7.3_Inch.stl](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_7.3_Inch.stl) |

#### Recommended Printing Settings
- 0.15mm
- 10%-15% Infill
- Baseplate Supports

## Assembly



