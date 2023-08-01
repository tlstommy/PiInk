#generate info for piink frame
import qrcode,socket,os
from PIL import ImageDraw,ImageFont,Image 

class infoGen:
    def __init__(self, frameWidth,frameHeight):
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight
        self.urlQR = None
        self.hostname = None
        self.frameIP = self.getSystemInfo()
        self.generateQR(f"http://{str(self.frameIP)}/")
    def getSystemInfo(self):
        self.hostname = socket.gethostname()
        return self.get_ip_address()
        #return socket.gethostbyname(socket.gethostname() + ".local")
    def get_ip_address(self):
        ip_address = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    def generateQR(self,qrData):
        print(qrData)

        qrSize = 10

        if(len(self.frameIP) > 9):
            qrSize = 8

        qr = qrcode.QRCode(version= 1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=qrSize,border=1)
        qr.add_data(qrData)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        self.urlQR = img
        self.buildImage()
    def deleteImage(self):
        os.system("sudo rm ../img/*")

    #build info image for the frame    
    def buildImage(self):
        fontFile = "FreeSans.ttf"
        print(fontFile)
        infoImage = Image.new(mode="RGB", size=(self.frameWidth, self.frameHeight),color=(255,255,255))
        titleFont = ImageFont.truetype(fontFile, int(self.urlQR.pixel_size/3))
        subTitleFont = ImageFont.truetype(fontFile, int(self.urlQR.pixel_size/6))
        ipFont = ImageFont.truetype(fontFile, int(self.urlQR.pixel_size/7))
        font = ImageFont.truetype(fontFile, int(self.urlQR.pixel_size/9))
        infoImage.paste(self.urlQR,(0,0))

        imageDraw = ImageDraw.Draw(infoImage)
        imageDraw.text((self.urlQR.pixel_size + int(titleFont.size),0),"PiInk",fill=(0,0,0),font=titleFont)
        imageDraw.line([(self.urlQR.pixel_size+int(titleFont.size)-int(titleFont.size/2),titleFont.size+3),(self.urlQR.pixel_size*2 + int(titleFont.size)+int(titleFont.size/2),titleFont.size+3)],fill=(0,0,0),width=5)
        
        imageDraw.text((self.urlQR.pixel_size+int(titleFont.size)-int(titleFont.size/2),titleFont.size+10),f"[IP]   {self.frameIP}",fill=(0,0,0),font=ipFont)

        lineYPadding = (subTitleFont.size*3)+int(subTitleFont.size/3)
        imageDraw.text((self.urlQR.pixel_size+int(titleFont.size)-int(titleFont.size/2),lineYPadding),f"[WEB]  {self.hostname}.local",fill=(0,0,0),font=ipFont)
        imageDraw.line([
        (self.urlQR.pixel_size+int(titleFont.size)-int(titleFont.size/2),(subTitleFont.size*3)+int(subTitleFont.size/2)+(subTitleFont.size*1)),
        (self.urlQR.pixel_size*2 + int(titleFont.size)+int(titleFont.size/2),(subTitleFont.size*3)+int(subTitleFont.size/2)+(subTitleFont.size*1))],fill=(0,0,0),width=5)
        


        self.urlQR.pixel_size += 5; 

        #horizontal borders
        imageDraw.line([(5,self.urlQR.pixel_size),(self.frameWidth-5,self.urlQR.pixel_size)],fill=(0,0,0),width=5)
        imageDraw.line([(5,self.frameHeight-5),(self.frameWidth-5,self.frameHeight-5)],fill=(0,0,0),width=5)
        
        #vertical borders
        imageDraw.line([(5,self.urlQR.pixel_size),(5,self.frameHeight-5)],fill=(0,0,0),width=5)
        imageDraw.line([(self.frameWidth-5,self.urlQR.pixel_size),(self.frameWidth-5,self.frameHeight-5)],fill=(0,0,0),width=5)

        #details thing
        imageDraw.text((self.urlQR.pixel_size,self.urlQR.pixel_size+5),"[Details]",fill=(0,0,0),font=subTitleFont)
        
        detailsText = f"PiInk is an E Ink based picture frame. The E Ink \nframe allows images to remain on the frame while \npower is shut off. The frame can be controlled \nby accessing the WebUI listed above via \nthe QR code or at {self.hostname}.local . "
        imageDraw.text((15,self.urlQR.pixel_size+50),detailsText,fill=(0,0,0),font=font)
        self.deleteImage()
        print(self.urlQR.pixel_size)
        print( os.getcwd())
        script_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(script_directory, "img/infoImage.png")
        print(image_path)
        #infoImage.show()
        infoImage.save(image_path)



