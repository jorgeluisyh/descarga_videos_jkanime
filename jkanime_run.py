from tkinter import Tk
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename, askdirectory
from jkanime import *

print tryvar

import tkSimpleDialog

root = Tk()
root.withdraw()
iconpath=r"D:\JYUPANQUI\PROYECTOS\jkanime_descarga\favicon.ico"
# icon =  ImageTk.PhotoImage(Image.open(iconpath))


# root.tk.call('wm', 'iconphoto', root._w, icon)
answer = tkSimpleDialog.askstring("Jkanime", 
	"Ingresa el enlace de tu anime de jkanime",
                                parent=root)
print answer
filepath = askdirectory() # show an "Open" dialog box and return the path to the selected file
print(filepath)

mainjk(answer,filepath)