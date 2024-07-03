import urllib.request
import os,random,time,signal
from flask import Flask, flash, request, redirect, url_for,render_template,jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime
from PIL import Image
import json
from inky.auto import auto
import RPi.GPIO as GPIO
from PIL import ImageDraw,Image 
import generateInfo
# Gpio button pins from top to bottom

#5 == info
#6 == rotate clockwise
#16 == rotate counterclockwise

BUTTONS = [5, 6, 16, 24]
ORIENTATION = 0
ADJUST_AR = False

#Set up RPi.GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Get the current path
PATH = os.path.dirname(os.path.dirname(__file__))
print(PATH)
UPLOAD_FOLDER = os.path.join(PATH,"img")
ALBUM_FOLDER = os.path.join(PATH,"album")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
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
app.config['ALBUM_FOLDER'] = ALBUM_FOLDER

#handles button presses
def handleButton(pin):
    #top button
    if(pin == 5):
        print("top pressed")
        generateInfo.infoGen(inky_display.width,inky_display.height)
        #update the eink display
        updateEink("infoImage.png",0,"")
    elif(pin == 6):
        print("rotate clockwise pressed")
        rotateImage(-90)
    elif(pin == 16):
        print("rotate counter clockwise pressed")
        rotateImage(90)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("req ",request.files)    
    ADJUST_AR = False

    arSwitchCheck,modeSwitchCheck,horizontalOrientationRadioCheck,verticalOrientationRadioCheck,albumSwitchInterval = loadSettings()

    print("Frame Mode: ",modeSwitchCheck)

    if horizontalOrientationRadioCheck == "checked":
        ORIENTATION = 0
    else:
        ORIENTATION = 1
    
    if arSwitchCheck == "checked":
        ADJUST_AR = True
    
    if request.method == 'POST':

        #get the form type
        formType = request.form.get('form_type')

        print("debug: " + str(formType))

        if formType == "album_file_form":
            print("album") 
            print(request.form)
        
        #todo make a better curl call
        #upload via link, add support in for api calls like cURL 'curl -X POST -F "file=@image.png" piink.local'
        if request.form and request.form.get("submit") == "Upload Image":
            file = request.files['file']
            print(file)
            print("req form: ", request.form)
            if file and allowed_file(file.filename):
                deleteImage()
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = os.path.join(app.config['UPLOAD_FOLDER'],filename)

                #update the eink display
                updateEink(filename,ORIENTATION,ADJUST_AR)
                if(len(request.form) == 0):
                    return "File uploaded successfully", 200
            elif formType == 'single_file_form':
                deleteImage()
                imageLink = request.form.getlist("text")[0]
                print(imageLink)
                try:
                    filename = imageLink.replace(":","").replace("/","")
                    filename = filename.split("?")[0]
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

        #rotate clockwise
        if request.form["submit"] == 'rotateImage':
            print("rotating image")
            rotateImage(-90)

        #ghosting clears
        if request.form["submit"] == 'clearGhost':
            print("ghosting clear call!")
            clearScreen()

        #save frame settings
        if request.form["submit"] == 'Save Settings':
            print(request.form)
            print(request.form["album_interval"])
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
            
            try:
                if request.form["mode_switch"] == "true":
                    modeSwitchCheck = "checked"
            except:
                modeSwitchCheck = ""
                pass
            try:
                if request.form["album_interval"] != "":
                    albumSwitchInterval = int(request.form["album_interval"])
                    print("psi set")
                else:
                    print("psi default set")
                    albumSwitchInterval = 30
                    
            except:
                pass

            
            saveSettings(horizontalOrientationRadioCheck,verticalOrientationRadioCheck,arSwitchCheck,modeSwitchCheck,albumSwitchInterval)
            return render_template('main.html',horizontalOrientationRadioCheck = horizontalOrientationRadioCheck,verticalOrientationRadioCheck=verticalOrientationRadioCheck,arSwitchCheck=arSwitchCheck,modeSwitchCheck=modeSwitchCheck,photoSwitchInterval=albumSwitchInterval)       
    return render_template('main.html',horizontalOrientationRadioCheck = horizontalOrientationRadioCheck,verticalOrientationRadioCheck=verticalOrientationRadioCheck,arSwitchCheck=arSwitchCheck,modeSwitchCheck=modeSwitchCheck,photoSwitchInterval=albumSwitchInterval)



#mode setting route
@app.route('/set_mode', methods=['POST'])
def set_mode():
    newMode = request.form.get('mode')
    if newMode:
        #Save the new mode
        adjustAR, _, horizontalOrientationRadioCheck, verticalOrientationRadioCheck,photoSwitchInterval = loadSettings()
        saveSettings(horizontalOrientationRadioCheck, verticalOrientationRadioCheck, adjustAR, newMode, photoSwitchInterval)
        return jsonify({"success": True})
    return jsonify({"error": "Invalid mode"}), 400

#mode getting route
@app.route('/get_mode', methods=['GET'])
def get_mode():
    _, modeSwitchCheck, _, _, _ = loadSettings()
    return jsonify({"mode": modeSwitchCheck})



#album stuff-

#file list
@app.route('/files', methods=['GET'])
def listFiles():
    files = os.listdir(app.config['ALBUM_FOLDER'])
    return jsonify(files)

@app.route('/file-preview/<filename>')
def previewFile(filename):
    return send_from_directory(app.config['ALBUM_FOLDER'], filename)

@app.route('/file/delete', methods=['POST'])
def deleteFilesFromAlbum():
    print("Request to delete file received.")
    filename = request.form['filename']
    print("Filename to delete:", filename)

    file_path = os.path.join(ALBUM_FOLDER, filename)
    print(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True})
    else:
        print("File not found:", file_path)
        return jsonify({"error": "File not found"}), 404

#upload image to album
@app.route('/upload', methods=['POST'])
def uploadToAlbum():
    print("Upload to album")
    print("req ",request.files)    
    files = request.files.getlist('file')
    for file in files:
        print(file)
        if file and allowed_file(file.filename):
            print("valid file")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['ALBUM_FOLDER'], filename))
            filename = os.path.join(app.config['ALBUM_FOLDER'],filename)
        else:
            print("invalid file")
    return jsonify({"success": True})
    
   



def loadSettings():
    horizontalOrient = ""
    verticalOrient = ""
    try:
        jsonFile = open(os.path.join(PATH,"config/settings.json"))
    except:
        saveSettings("","checked",'aria-checked="false"',"")
        jsonFile = open(os.path.join(PATH,"config/settings.json"))
    settingsData = json.load(jsonFile)
    jsonFile.close()
    if settingsData.get("orientation") == "Horizontal":
        horizontalOrient = "checked"
        verticalOrient = ""
    else:
        verticalOrient = "checked"
        horizontalOrient = ""
    return settingsData.get("adjust_aspect_ratio"),settingsData.get("frame_mode"),horizontalOrient,verticalOrient,settingsData.get("photo_interval")
def saveSettings(orientationHorizontal,orientationVertical,adjustAR,frameMode,photo_interval):
    if orientationHorizontal == "checked":
        orientationSetting = "Horizontal"
    else:
        orientationSetting = "Vertical"
    jsonStr = {
        "frame_mode":frameMode,
        "orientation":orientationSetting,
        "adjust_aspect_ratio":adjustAR,
        "photo_interval":photo_interval,
    }
    with open(os.path.join(PATH,"config/settings.json"), "w") as f:
        json.dump(jsonStr, f)

def updateEink(filename,orientation,adjustAR):
    with Image.open(os.path.join(PATH, "img/",filename)) as img:

        #do image transforms 
        img = changeOrientation(img,orientation)
        img = adjustAspectRatio(img,adjustAR)    

        # Display the image
        inky_display.set_image(img)
        inky_display.show()

#clear the screen to prevent ghosting
def clearScreen():
    print("running ghost clear")
    img = Image.new(mode="RGB", size=(inky_display.width, inky_display.height),color=(255,255,255))
    clearImage = ImageDraw.Draw(img)
    inky_display.set_image(img)
    inky_display.show()
    updateEink(os.listdir(app.config['UPLOAD_FOLDER'])[0],ORIENTATION,ADJUST_AR)



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
    img_directory = os.path.join(PATH, "img")
    for filename in os.listdir(img_directory):
        fp = os.path.join(img_directory, filename)
        if os.path.isfile(fp):
            os.remove(fp)
            
def rotateImage(deg):
    
    with Image.open(os.path.join(PATH, "img/",os.listdir(app.config['UPLOAD_FOLDER'])[0])) as img:
        #rotate image by degrees and update
        img = img.rotate(deg, Image.NEAREST,expand=1)
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
