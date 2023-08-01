import urllib.request
import os,random,time,signal
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime
from PIL import Image
import json
from inky.auto import auto
import RPi.GPIO as GPIO

import generateInfo
# Gpio button pins from top to bottom
BUTTONS = [5, 6, 16, 24]
ORIENTATION = 0
ADJUST_AR = False

#Set up RPi.GPIO
GPIO.setmode(GPIO.BCM)



GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#sudo killall python
# Get the current path
PATH = os.path.dirname(os.path.dirname(__file__))
print(PATH)
UPLOAD_FOLDER = os.path.join(PATH,"img")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
print(ALLOWED_EXTENSIONS)


# Check whether the specified path exists or not
pathExist = os.path.exists(os.path.join(PATH,"img"))

if(pathExist == False):
   os.makedirs(os.path.join(PATH,"img"))



#setup eink display and border
inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.BLACK)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#handles button presses
def handleButton(pin):

    #top button
    if(pin == 5):
        print("top pressed")
        generateInfo.infoGen(inky_display.width,inky_display.height)
        #update the eink display
        updateEink("infoImage.png",0,"")


#app.config['SERVER_NAME'] = "pi-ink.local:80"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    ADJUST_AR = False

    arSwitchCheck,horizontalOrientationRadioCheck,verticalOrientationRadioCheck = loadSettings()

    #todo: read settings in from file each time its loaded
    if horizontalOrientationRadioCheck == "checked":
        ORIENTATION = 0
    else:
        ORIENTATION = 1
    
    if arSwitchCheck == "checked":
        ADJUST_AR = True
    

    if request.method == 'POST':
        print(request.form)
        

        #upload via link
        if request.form["submit"] == "Upload Image":
            file = request.files['file']
            print(file)
            if file and allowed_file(file.filename):
                deleteImage()
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = os.path.join(app.config['UPLOAD_FOLDER'],filename)

                #update the eink display
                updateEink(filename,ORIENTATION,ADJUST_AR)
            else:
                deleteImage()
                imageLink = request.form.getlist("text")[0]
                print(imageLink)
                try:
                    filename = imageLink.replace(":","").replace("/","")
                    print(filename)
                    #grab the url and download it to the folder
                    urllib.request.urlretrieve(imageLink, os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    updateEink(filename,ORIENTATION,ADJUST_AR)
                except:
                    #flash error message
                    flash("Error: Unsupported Media or Invalid Link!")
                    return render_template('main.html')
                    
        #other button funcs
        #reboot
        if request.form["submit"] == 'Reboot':
            print("reboot")
            os.system("sudo reboot")
        
        #shutdown
        if request.form["submit"] == 'Shutdown':
            print("shutdown")
            os.system("sudo shutdown")

        #rotate
        if request.form["submit"] == 'rotateImage':
            print("rotating image")
            rotateImage()

        #save frame settings
        if request.form["submit"] == 'Save Settings':
            if(request.form["frame_orientation"] == "Horizontal Orientation"):
                horizontalOrientationRadioCheck = "checked"
                verticalOrientationRadioCheck = ""
            else:
                horizontalOrientationRadioCheck = ""
                verticalOrientationRadioCheck = "checked"
            try:
                if request.form["adjust_ar"] == "true":
                    arSwitchCheck = "checked"
            except:
                arSwitchCheck = ""
                pass
            saveSettings(horizontalOrientationRadioCheck,verticalOrientationRadioCheck,arSwitchCheck)
            return render_template('main.html',horizontalOrientationRadioCheck = horizontalOrientationRadioCheck,verticalOrientationRadioCheck=verticalOrientationRadioCheck,arSwitchCheck=arSwitchCheck)       
    return render_template('main.html',horizontalOrientationRadioCheck = horizontalOrientationRadioCheck,verticalOrientationRadioCheck=verticalOrientationRadioCheck,arSwitchCheck=arSwitchCheck)

def loadSettings():
    horizontalOrient = ""
    verticalOrient = ""
    try:
        jsonFile = open(os.path.join(PATH,"config/settings.json"))
    except:
        saveSettings("","checked",'aria-checked="false"')
        jsonFile = open(os.path.join(PATH,"config/settings.json"))
    settingsData = json.load(jsonFile)
    jsonFile.close()
    if settingsData.get("orientation") == "Horizontal":
        horizontalOrient = "checked"
        verticalOrient = ""
    else:
        verticalOrient = "checked"
        horizontalOrient = ""
    return settingsData.get("adjust_aspect_ratio"),horizontalOrient,verticalOrient
def saveSettings(orientationHorizontal,orientationVertical,adjustAR):
    if orientationHorizontal == "checked":
        orientationSetting = "Horizontal"
    else:
        orientationSetting = "Vertical"
    jsonStr = {
        "orientation":orientationSetting,
        "adjust_aspect_ratio":adjustAR,
    }
    with open(os.path.join(PATH,"config/settings.json"), "w") as f:
        json.dump(jsonStr, f)

def updateEink(filename,orientation,adjustAR):
    
    img = Image.open(os.path.join(PATH, "img/",filename))

    #do image transforms 
    img = changeOrientation(img,orientation)
    img = adjustAspectRatio(img,adjustAR)    

    # Display the image
    inky_display.set_image(img)
    inky_display.show()

    #now that it has been shown delete the file
    #os.remove(os.path.join(PATH, "img/",filename))

def changeOrientation(img,orientation):
    # 0 = horizontal
    # 1 = portrait
    if orientation == 0:
        img = img.rotate(0)
    elif orientation == 1:
        img = img.rotate(90)
    return img

def adjustAspectRatio(img,adjustARBool):
    if adjustARBool:
        w = inky_display.width
        h = inky_display.height
        ratioWidth = w / img.width
        ratioHeight = h / img.height
        if ratioWidth < ratioHeight:
            # It must be fixed by width
            resizedWidth = w
            resizedHeight = round(ratioWidth * img.height)
        else:
            # Fixed by height
            resizedWidth = round(ratioHeight * img.width)
            resizedHeight = h
        imgResized = img.resize((resizedWidth, resizedHeight), Image.LANCZOS)
        background = Image.new('RGBA', (w, h), (0, 0, 0, 255))

        #offset image for background and paste the image
        offset = (round((w - resizedWidth) / 2), round((h - resizedHeight) / 2))
        background.paste(imgResized, offset)
        img = background
    else:
        img = img.resize(inky_display.resolution)
    return img
def deleteImage():
    os.system("sudo rm ../img/*")

def rotateImage():
    

    img = Image.open(os.path.join(PATH, "img/",os.listdir(app.config['UPLOAD_FOLDER'])[0]))
    
    #rotate image 90 degrees and update
    img = img.rotate(90, Image.NEAREST,expand=1)
    img = img.save(os.path.join(PATH, "img/",os.listdir(app.config['UPLOAD_FOLDER'])[0]))
    updateEink(os.listdir(app.config['UPLOAD_FOLDER'])[0],ORIENTATION,ADJUST_AR)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


#run button checks on gpio    
for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handleButton, bouncetime=250)
if __name__ == '__main__':
    app.secret_key = str(random.randint(100000,999999))
    app.run(host="0.0.0.0",port=80)
