import tkinter.ttk as ttk
from .image_handler import PhotoImage

class ProgressCircle(ttk.Label):
    def __init__(self, master, width:int, height:int, style:str="TLabel"):
        super().__init__(master, width=width+10, style=style)
        self.root = self.nametowidget(".")
        
        self._active = False
        self._images = [PhotoImage(source=f"progress_circle_{self.master.getTheme()}.png",
                                   width=width, height=height,
                                   rotation=rotation).get() for rotation in range(0,361) if rotation % 5 == 0]
        self._images = list(reversed(self._images))
        
        first = self._images[0]
        self.configure(image=first)
        self.image = first
        
        
    def play(self, interval:int=50):
        self._active = True
        
        def next_frame(frame:int):
            frame += 1 
            if frame >= len(self._images) - 1:
                frame = 0
                
            image = self._images[frame]
            self.configure(image=image)
            self.image = image
            
            if self._active:
                self.root.after(interval, lambda:next_frame(frame))
                
        next_frame(frame=0)
        
    
    def stop(self):
        self._active = False
            