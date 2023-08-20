<h1 align="center">PiInk - A Raspberry Pi Powered E-Ink Picture Frame</h1>

![all 3 piinks](https://github.com/tlstommy/PiInk/assets/36305669/9531da45-1ef7-40e7-9d1f-2fef53ca01f3)


### An open-source, low-power, digital picture frame that gives images a natural, paper-like, aesthetic.

**Features:**
- **Web Ui**: A built-in interface to control PiInk and upload images over the network.
- **Low Power**: The E-Ink display only needs power to change images, allowing pictures to persist on the frame.
- **Natural Aesthetic**: No backlight and the unique E-Ink technology make images look as if they are printed onto paper.
- **Open Source**: PiInk is under the MIT License, so modify it as you see fit!

# Table of Contents
* [Overview](#piink---a-raspberry-pi-powered-e-ink-picture-frame)
* [Installation](#installation)
* [WebUI](#webui--piink-buttons)
* [Parts List](#parts-list)
   * [E-Ink Display](#e-ink-display)
   * [3D Printed Stand](#3d-printed-stand)
* [Frame Assembly](#frame-assembly)
* [Demo](#demo)
* [Issues & Suggestions](#issues--suggestions)


# Installation

To install, clone the repository, run the install script, and follow the on-screen instructions:

```bash
git clone https://github.com/tlstommy/PiInk.git
cd PiInk
sudo bash install.sh

```

Upon reboot, the PiInk program will start and be accessible on the web at the Raspberry Pi's IP address or at `piink.local`. 


# WebUI & PiInk Buttons

**The PiInk can be controlled via the WebUI which can be found at the Raspberry Pi's IP address or at `piink.local`**

![webui](https://github.com/tlstommy/PiInk/assets/36305669/26215ec5-999e-482c-944a-ea160f643bcf)


### Uploading an image
Use the WebUI to upload an image to the PiInk via a file upload or an image link.
**If you ever are unable to access the WebUI, press the `A` button on the back of the PiInk and an info screen will pop up.**

### Settings
In the PiInk Settings, set options for the PiInk such as orientation or automatic image adjustment. Reboot or shut down PiInk from the power button in the top right.

### PiInk Buttons
Located on the backside of the PiInk's display are four buttons: A, B, C, and D. Each of these buttons is designed to execute a specific operation on the PiInk. Refer to the table below for the function associated with each button:
| Button | Function |
| :---: |:---|
| `A` | Display the PiInk info screen |
| `B` | Rotate the current image clockwise|
| `C` | Rotate the current image counterclockwise|
| `D` | Currently unused|



# Parts List

PiInk's 3D printed mount is tailored to fit the Raspberry Pi Zero family, but it's versatile enough to be used with any Raspberry Pi model. Here's what you'll need to build your own PiInk:

- **Raspberry Pi**: Purchase a Pi Zero or other Raspberry Pi model from websites like [Adafruit](https://www.adafruit.com/category/105) or [Pimoroni](https://shop.pimoroni.com/collections/raspberry-pi).
- **E-Ink Display**: Specific details are in the next section.
- **3D-Printed Stand**: Required for mounting the E-Ink Display.

### E-Ink Display


**PiInk uses a Pimoroni Inky Impression E-Ink Display, available in 3 sizes: 4", 5.7", & 7.3" You can purchase one at the links below.**
###### Note: The larger the display, the longer it takes to refresh an image.
- **[4 Inch Display](https://shop.pimoroni.com/products/inky-impression-4)**
- **[5.7 Inch Display](https://shop.pimoroni.com/products/inky-impression-5-7)**
- **[7.3 Inch Display](https://shop.pimoroni.com/products/inky-impression-7-3)**

The included mounting hardware is used to secure the Inky Impression to the 3D-printed stand.

### 3D Printed Stand

Find 3D printable stand files in the [STL folder](https://github.com/tlstommy/PiInk/tree/main/STL) or on [Printables.com](https://www.printables.com/model/552238-piink-a-raspberry-pi-powered-e-ink-picture-frame). Select the appropriate stand for your E-Ink display size from the table below:

| E-Ink Display                  | STL file                                                                                           |
| ------------------------------ |:--------------------------------------------------------------------------------------------------:|
| Inky Impression - 4.0 Inches   | [4 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_4_Inch.stl)             |
| Inky Impression - 5.7 Inches   | [5.7 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_5.7_Inch.stl)         |
| Inky Impression - 7.3 Inches   | [7.3 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_7.3_Inch.stl)         |


#### Recommended Printing Settings
- Layer Height: 0.15mm
- Infill: 10%-15%
- Supports: Baseplate

# PiInk Frame Assembly

Mounting the PiInk onto the PiInk stand is a straightforward process that can be completed in 3 simple steps.

**You will need the following materials that are included with the Inky Impression:**
- (2) Standoffs
- (2) Screws
  
### Step 1: Attach the Pi Zero and install the standoffs to the lower mounting holes.
![Assembly Step 1](https://github.com/tlstommy/PiInk/assets/36305669/aee84a70-efd5-4cc2-aec4-e3419f7ba9ac)

### Step 2: Secure the stand onto standoffs using the screws. They will thread themselves.
![Assembly Step 2](https://github.com/tlstommy/PiInk/assets/36305669/31585b41-ff0b-4884-9739-a2917a938b48)

### Step 3: Route the Raspberry Pi power cable behind the PiInk stand.
![Assembly Step 3](https://github.com/tlstommy/PiInk/assets/36305669/84fbf238-1630-4371-92aa-cf4432f78f38)

# Demo

**Below is a video showing the PiInk updating to a new image.**

[IMG_0512 (1).webm](https://github.com/tlstommy/PiInk/assets/36305669/4dda6b41-d10e-469c-a952-cf3f85b38dbc)




# Issues & Suggestions
If you encounter any issues or have any suggestions, please submit them through the [GitHub Issues](https://github.com/tlstommy/piink/issues) page. Your feedback is greatly appreciated!




