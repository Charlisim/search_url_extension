
from Tkinter import *
import re
from main_gui import *
class App(Frame):


    def callback(self):
        print "called the callback"
    
    def processURL(self):
        url = self.url.get()
        extensions = self.extensions.get()
        extensions = re.split(',',extensions)
        forbbiden = self.forbbiden.get()
        forbbiden = re.split(',',forbbiden)
        u = urlExtension(url,extensions, forbbiden)
        result = u.searchLink()
        print result
        v = StringVar()
        v.set(result)
        print v.get()
        self.canvas = Text(height=10, width=80)
        self.canvas.insert(INSERT, v.get())
        self.canvas.pack()

 
    def createMenu(self):
        
        menu = Menu(self)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New" , command=self.callback)
        filemenu.add_command(label="Open...")

    def createWidgets(self,master):

        
    
        self.labelURL = Label(text="URL")
        self.labelURL.pack()
        
        self.url = Entry()
        self.url.grid()
        self.url.pack()        
        self.labelExtensions = Label(text="Extensions")
        self.labelExtensions.pack()
        self.extensions = Entry()

        self.extensions.pack()
        self.labelForbidden = Label(text="Forbbiden")
        self.labelForbidden.pack()

        self.forbbiden = Entry()
        self.forbbiden.pack()
 

        b = Button(master, text="Enviar", command=self.processURL)
        b.pack()


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(master)
        self.createMenu()
        


# create the application


myapp = App()
# menu = Menu(myapp)
# myapp.master.config(menu=menu)
# filemenu = Menu(menu)
# menu.add_cascade(label="File", menu=filemenu)
# filemenu.add_command(label="New")
# filemenu.add_command(label="Open...")
# filemenu.add_separator()
# filemenu.add_command(label="Exit")

# helpmenu = Menu(menu)
# menu.add_cascade(label="Help", menu=helpmenu)
# helpmenu.add_command(label="About...")
#
# here are method calls to the window manager class
#
myapp.master.title("Search URL")
myapp.master.geometry("500x500")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()