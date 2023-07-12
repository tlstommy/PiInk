
import os
from PIL import Image
from inky.auto import auto


# Get the current path
PATH = os.path.dirname(__file__)

#setup eink display and border
inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.BLACK)

img = Image.open(os.path.join(PATH, "img/image.jpg"))
img = img.resize(inky_display.resolution)

# Display the logo image

inky_display.set_image(img)
inky_display.show()