from datetime import datetime
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

class MainFrame(tk.Tk):
    """
    Frame principal
    """
    def __init__(self):
        tk.Tk.__init__(self) 
        self.configMain()

        conteiner = tk.Frame()
        conteiner.grid(row=0, column=0, sticky = 'nsew')
        
        self.mode=tk.StringVar()
        self.mode.set('Clock')

        self.listing = {}
        for page in (Clock,Wheater , Options):
            page_name = page.__name__
            frame = page(parent = conteiner, controller= self)
            frame.grid(row=0, column=0, sticky = 'nsew')
            self.listing[page_name] = frame
         
        self.up_frame('Options')

    def configMain(self):
        """
        Configuración de la ventana principal
        """
        positionX = self.winfo_screenwidth() - 200
        positionY = 60
        self.geometry("+{}+{}".format(positionX, positionY))
        self.attributes('-alpha', 0.8)
        self.configure(background='white')
        self.wm_attributes('-transparentcolor', 'white')
        self.attributes("-topmost", True)
        self.overrideredirect(True)

    def up_frame(self, page_name):
        """
        Muestra la ventana
        """
        page = self.listing[page_name]
        page.tkraise()
    


class Wheater(tk.Frame):
    """
    Frame del clima
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = controller.mode

        r = requests.get("https://www.metaweather.com/api/location/468739/")
        clima = r.json().get("consolidated_weather")[0]
        humedad = clima.get("humidity")
        codigo = clima.get("weather_state_abbr")
        temperatura = "{:.1f}".format(clima.get("the_temp"))
        i = requests.get("https://www.metaweather.com/static/img/weather/png/64/{}.png".format(codigo))
        
        icono = Image.open(BytesIO(i.content)) 
    
        global img
        img = ImageTk.PhotoImage(icono)
        imgLabel = tk.Label(self,image=img)
        imgLabel.grid(column=0,row=0, columnspan=2, sticky="s")
        tempLabel = tk.Label(self, text=(str(temperatura) + "°C"), font=("Helvetica 10"))
        tempLabel.grid(column=0, row=1)
        humeLabel = tk.Label(self, text=(str(humedad)+"%"), font=("Helvetica 10"))
        humeLabel.grid(column=1, row=1)


class Clock(tk.Frame):
    """
    Frame del reloj
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = controller.mode
        
        timeLabel = tk.Label(self, font=("Helvetica 30 bold"))
        timeLabel.pack()
        def getTime():
            t = datetime.now()
            global current 
            current=t.strftime("%H:%M")
            timeLabel.config(text=current)
            timeLabel.after(2000,getTime)
        getTime()


class Options(tk.Frame):
    """
    Frame de opciones
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = controller.mode

        self.listing=controller.listing

        self.selected=tk.StringVar()
        self.selected.set(None)
        
        for label, value in self.listing.items():
            tk.Radiobutton(self, text=label, variable=self.selected,value=label, command=lambda:controller.up_frame(self.selected.get())).pack()

        qButton = tk.Button(self, text="Exit", command=self.quit,)
        qButton.pack()
    
    
def goOptions(event):
    app.up_frame('Options')


if __name__ == '__main__':
    app = MainFrame()
    app.bind("<Button-1>",goOptions)
    app.mainloop()

