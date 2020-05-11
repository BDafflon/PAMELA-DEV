import tkinter

import PIL
from PIL import ImageTk


class LauncherGui:
    def __init__(self, window, window_title, imgcv):
        self.window = window
        self.window.title(window_title)
        self.validation = True

         # Load an image using OpenCV
        self.cv_img = imgcv

         #Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, no_channels = self.cv_img.shape

         # Create a canvas that can fit the above image
        self.canvas = tkinter.Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()

         # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

         # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

         # Button that lets the user blur the image
        self.btn_ok=tkinter.Button(window, text="Ok", width=50, command=self.ok_image)
        self.btn_ok.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_err = tkinter.Button(window, text="Annuler", width=50, command=self.err_image)
        self.btn_err.pack(anchor=tkinter.CENTER, expand=True)

        self.window.mainloop()
    def ok_image(self):
        self.window.destroy()
        self.validation = True

    def err_image(self):
        self.window.destroy()
        self.validation = False
 # Create a window and pass it to the Application object
