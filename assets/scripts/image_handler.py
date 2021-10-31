from urllib.request import urlopen
from urllib.error import URLError
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from io import BytesIO

IMAGE_PATH = 'assets/images'


def dynamic_button_image(button, rest:str, active:str) -> None:
    """Make button image change on different states"""
    
    def change_image(image):
        button.configure(image=image)
        button.image = image
        
    button.bind("<Leave>", lambda event: change_image(rest))
    button.bind("<Enter>", lambda event: change_image(active))
    
    change_image(rest)


class PhotoImage:
    def __init__(self, source:str,
                 width:int, height:int,
                 mode='path',
                 roundCornerRadius:int=0, makeCircle:bool=False,
                 rotation:int=0, cropToSize:bool=False,
                 urlRetries:int=3):
        
        """Gets an image from specified path or url (auto fills path to image directory)

        Options:
        \nsource            - path or url to image
        \nmode              - path or url
        \nwidth and height
        \nroundCornerRadius - radius of rounded edges (0 is off, 12 is good for smooth corners)
        \nmakeCircle        - crop image into a transparent circle
        \nrotation          - return the image rotated by this value
        \ncropToSize        - crops image to width/height arguments (sometimes produces black bars)"""
            
        self.width, self.height = int(width), int(height)  # pillow only excepts integers for resizing
        
        if (mode == 'path'):
            path = f"{IMAGE_PATH}/{source}"
            self.image = Image.open(fp=path)
            
        elif (mode == 'url'):
            try: 
                with urlopen(source) as u: rawData = u.read()
                self.image = Image.open(BytesIO(rawData))
                
            except URLError as e:
                if (urlRetries == 0):
                    self.image = PhotoImage(source="urlerror.png", width=width, height=height, mode="path").get(maketk=False)
                
                else:
                    self.image = PhotoImage(source=source, width=width, height=height, mode='url', urlRetries=urlRetries-1).get(maketk=False)
        
        else:
            raise TypeError(f"mode {mode} is invalid")
        
        if (cropToSize):
            self.crop_to_size()
        
        self.image = self.image.resize((self.width, self.height), resample=Image.ANTIALIAS)
        
        if (roundCornerRadius > 0) & (not makeCircle):
            self.cut_corners(rad=roundCornerRadius)
            
        if (makeCircle) & (roundCornerRadius <= 0):
            self.image = self.crop_transparent_circle(self.image, 4)
            
        if (rotation != 0):
            self.rotate(rotation)
        
        
    def get(self, maketk:bool=True):
        if (maketk):
            return ImageTk.PhotoImage(self.image)
        else:
            return self.image
        
        
    def rotate(self, rotation) -> None:
        """Rotates image to specified rotation"""
        self.image = self.image.rotate(rotation)
        
        
    def crop_to_size(self) -> None:
        """Crops image to fit in specified dimensions"""
        
        cropW, cropH = self.width * 20, self.height * 20
        imageW, imageH = self.image.size        
        
        while (cropW > imageW):
            cropW -= 10
            
        while (cropH > imageH):
            cropH -= 10
            
        if (self.width == self.height) & (cropW > cropH):
            cropW = cropH
            
        elif (self.width == self.height) & (cropW < cropH):
            cropH = cropW
            
        left = int((imageW-cropW) // 2)
        top = int((imageH-cropH) // 2)
        right = int((imageW+cropW) // 2)
        bottom = int((imageH+cropH) // 2)
        self.image = self.image.crop((left, top, right, bottom))
        
        
    def cut_corners(self, rad):
        """Trims corners of square image to round edges"""
        
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', self.image.size, "white")
        w, h = self.image.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        self.image.putalpha(alpha)
        
        # TODO: apply filter to rounded corners so they arent rough

        
        
    def crop_transparent_circle(self, blur_radius, offset=0):
        """Crops image into circle with transparent background"""
        
        offset = blur_radius * 2 + offset
        mask = Image.new('L', self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, self.image.size[0] - offset, self.image.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2))
        
        result = self.image.copy()
        result.putalpha(mask)
        self.image = result
