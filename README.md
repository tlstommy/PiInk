
<h1 align="center">PiInk - A Raspberry Pi Powered E-Ink Picture Frame</h1>

![image](https://github.com/tlstommy/PiInk/assets/36305669/626a897f-e623-4cc2-a8d9-015e7bd3f8fa)


### An open-source, low-power, digital picture frame that gives images a natural, paper-like, aesthetic.

**Features:**
- **Web Ui**: A built-in interface to control PiInk and upload images over the network.
- **Low Power**: The E-Ink display only needs power to change images, allowing pictures to persist on the frame.
- **Natural Aesthetic**: No backlight and the unique E-Ink technology make images look as if they are printed onto paper.
- **Open Source**: PiInk is under the MIT License, so modify it as you see fit!

# Table of Contents
* [Overview](#piink---a-raspberry-pi-powered-e-ink-picture-frame)
* [Installation](#installation)
* [WebUI](#webui)
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
sudo bash install

```

Upon reboot, the PiInk program should start and be accessible on the web at the Raspberry Pi's IP address or at `piink.local`. 


# WebUI & Frame Buttons

**The PiInk can be controlled via the WebUI which can be found at the Raspberry Pi's IP address or at `piink.local`**

![image](https://github.com/tlstommy/PiInk/assets/36305669/e2e2549b-6bc0-4879-9c0d-e9283fa75e27)

### Uploading an image
Use the WebUI to upload an image to the PiInk via a file upload or an image link.
**If you ever are unable to access the WebUI, press the `A` button on the back of the PiInk and an info screen will pop up.**

### Settings
In Frame Settings, set options for the PiInk like orientation or automatic image adjustment. Reboot or shut down PiInk from the power button in the top right.

### Buttons
Located on the backside of the PiInk Frame are four buttons: A, B, C, and D. Each of these buttons is designed to execute a specific operation on the frame. Refer to the table below for the function associated with each button:
| Button | Function |
| :---: |:---|
| `A` | Display the PiInk info screen |
| `B` | Rotate the current image clockwise|
| `C` | Rotate the current image counterclockwise|
| `D` | Currently unused|



# Parts List

PiInk's 3D printed mount is tailored to fit the Raspberry Pi Zero family, but it's versatile enough to be used with any Raspberry Pi model. Here's what you'll need to build your own PiInk frame:

- **Raspberry Pi**: Purchase a Pi Zero or other Raspberry Pi model from websites like [Adafruit](https://www.adafruit.com/category/105) or [Pimironi](https://shop.pimoroni.com/collections/raspberry-pi).
- **E-Ink Display**: Specific details are in the next section.
- **3D-Printed Stand**: Required for mounting the E-Ink Display.

### E-Ink Display


**PiInk uses a Pimironi Inky Impression E-Ink Display, available in 3 sizes: 4", 5.7", & 7.3" You can purchase one at the links below.**
###### Note: The larger the display, the longer it takes to refresh an image.
- **[4 Inch Display](https://shop.pimoroni.com/products/inky-impression-4)**
- **[5.7 Inch Display](https://shop.pimoroni.com/products/inky-impression-5-7)**
- **[7.3 Inch Display](https://shop.pimoroni.com/products/inky-impression-7-3)**

The included mounting hardware is used to secure the Inky Impression to the 3D-printed stand.

### 3D Printed Stand

Find 3D printable stand files in the [STL folder](https://github.com/tlstommy/PiInk/tree/main/STL) or on [Printables.com](). Select the appropriate stand for your E-Ink display size from the table below:

| E-Ink Display                  | STL file                                                                                           |
| ------------------------------ |:--------------------------------------------------------------------------------------------------:|
| Inky Impression - 4.0 Inches   | [4 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_4_Inch.stl)             |
| Inky Impression - 5.7 Inches   | [5.7 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_5.7_Inch.stl)         |
| Inky Impression - 7.3 Inches   | [7.3 Inch Stand](https://github.com/tlstommy/PiInk/blob/main/STL/PiInk_stand_7.3_Inch.stl)         |


#### Recommended Printing Settings
- Layer Height: 0.15mm
- Infill: 10%-15%
- Supports: Baseplate

# Frame Assembly

Mounting the PiInk onto the PiInk stand is a straightforward process that can be completed in 3 simple steps.

**You will need the following materials that are included with the Inky Impression:**
- (2) Standoffs
- (2) Screws
  
### Step 1: Attach the Pi Zero and install the standoffs to the lower mounting holes.
![assembly step 1](https://github.com/tlstommy/PiInk/assets/36305669/8ba1b216-5b6a-4fad-ba75-36ca108940f8)

### Step 2: Secure the stand onto standoffs using the screws. They will thread themselves.
![assembly step 2](https://github.com/tlstommy/PiInk/assets/36305669/5afd5266-8ca0-43b3-a68c-68bada6ae897)

### Step 3: Route the Raspberry Pi power cable behind the PiInk stand.
![assembly step 3](https://github.com/tlstommy/PiInk/assets/36305669/d2324130-9911-4ee5-ac8c-276beeb2a951)

# Demo

**Here is a video showing the PiInk frame updating to a new image.**

[IMG_0512 (1).webm](https://github.com/tlstommy/PiInk/assets/36305669/8ea15c3a-578c-4197-86a0-3f3a37161f8d)




# Issues & Suggestions
If you encounter any issues or have any suggestions, please submit them through the [Github Issues](https://github.com/tlstommy/piink/issues) page. Your feedback is greatly appreciated!




