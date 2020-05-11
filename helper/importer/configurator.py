import tkinter
from tkinter.filedialog import askopenfilename


class Configurator:
    def __init__(self, window,f,fs,fsc):
        self.window = window
        self.window.title("Configuration")
        self.validation = True
        self.filename=f
        self.filenameStock = fs
        self.filenameScenario = fsc

        tkinter.Label(self.window, text="Environment").grid(row=0)
        tkinter.Label(self.window, text="Stock").grid(row=1)
        tkinter.Label(self.window, text="Scenario").grid(row=2)

        entry = tkinter.Entry(self.window, textvariable=self.filename)
        entry.insert(0, self.filename)
        entry2 = tkinter.Entry(self.window, textvariable=self.filenameStock)
        entry2.insert(0, self.filenameStock)
        entry3 = tkinter.Entry(self.window, textvariable=self.filenameScenario)
        entry3.insert(0, self.filenameScenario)

        entry.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        entry3.grid(row=2, column=1)



        self.button = tkinter.Button(self.window, text='Open', command=self.set_filename)
        self.button1 = tkinter.Button(self.window, text='Open', command=self.set_filenameStock)
        self.button2 = tkinter.Button(self.window, text='Open', command=self.set_filenameScenario)

        self.button.grid(row=0, column=2)
        self.button1.grid(row=1, column=2)
        self.button2.grid(row=2, column=2)

         # Button that lets the user blur the image
        self.btn_ok=tkinter.Button(window, text="Ok", command=self.ok_image)
        self.btn_ok.grid(row=3, column=0)

        self.btn_err = tkinter.Button(window, text="Annuler", command=self.err_image)
        self.btn_err.grid(row=3, column=2)

        self.window.mainloop()
    def ok_image(self):

        self.window.destroy()
        self.validation = True

    def err_image(self):
        self.validation = False
        self.window.destroy()

    def set_filename(self):
        self.filename = (askopenfilename())

    def set_filenameStock(self):
        self.filenameStock = (askopenfilename())

    def set_filenameScenario(self):
        self.filenameScenario = (askopenfilename())

    def getFile(self):
        return self.filename,self.filenameStock,self.filenameScenario
        # Create a window and pass it to the Application object
