#! /usr/bin/env python
# -*- python -*-

import sys
import re
from main_gui import *
py2 = py30 = py31 = False
version = sys.hexversion
if version >= 0x020600F0 and version < 0x03000000 :
	py2 = True    # Python 2.6 or 2.7
	from Tkinter import *
	import ttk
elif version >= 0x03000000 and version < 0x03010000 :
	py30 = True
	from tkinter import *
	import ttk
elif version >= 0x03010000:
	py31 = True
	from tkinter import *
	import tkinter.ttk as ttk
else:
	print ("""
	You do not have a version of python supporting ttk widgets..
	You need a version >= 2.6 to execute PAGE modules.
	""")
	sys.exit()



def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root
	root = Tk()
	root.title('Search URL')
	root.geometry('800x600+800+329')
	w = New_Toplevel_1 (root)
	init()
	root.mainloop()

w = None
def create_New_Toplevel_1 (root):
	'''Starting point when module is imported by another program.'''
	global w, w_win
	if w: # So we have only one instance of window.
		return
	w = Toplevel (root)
	w.title('New_Toplevel_1')
	w.geometry('379x282+674+329')
	w_win = New_Toplevel_1 (w)
	init()
	return w_win

def destroy_New_Toplevel_1 ():
	global w
	w.destroy()
	w = None




def init():
	pass


	


def Enviar():
		print ('Enviar')

def TODO():
		print ('TODO')
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print ' - rClickbinder, something wrong'
        pass




class New_Toplevel_1:
	def processURL(self):
		url = self.url.get()
		extension = self.extension.get()
		extension = re.split(',',extension)
		forbbiden = self.forbbiden.get()
		forbbiden = re.split(',',forbbiden)
		u = urlExtension(url,extension, forbbiden)
		resultado = u.searchLink()
		print resultado
		resultado = re.split(',', resultado)
		

		v = StringVar()
		v.set(resultado)
		print v.get()
		self.labelResultado = Label()
		self.labelResultado.place(relx=0.03,rely=0.53,height=19,width=92)
		self.labelResultado.configure(text='''Resultado''')
		self.listaURLS = Listbox()
		self.listaURLS.place(relx=0.05,rely=0.55,relheight=0.37,relwidth=0.69)
		self.listaURLS.configure(selectmode="multiple")
		for r in resultado:
			self.listaURLS.insert(END, r)

		


	

	def __init__(self, master=None):
		# Set background of toplevel window to match
		# current style
		style = ttk.Style()
		theme = style.theme_use()
		default = style.lookup(theme, 'background')
		master.bind('<Button-3>',rClicker, add='')
		master.configure(background=default)

		self.labelURL = Label (master)
		self.labelURL.place(relx=0.05,rely=0.1,height=19,width=28)
		self.labelURL.configure(text='''URL''')

		self.url = Entry (master)
		self.url.place(relx=0.15,rely=0.09,relheight=0.06,relwidth=0.32)


		self.extension = Entry (master)
		self.extension.place(relx=0.15,rely=0.16,relheight=0.06,relwidth=0.32)
		self.extension.configure(selectbackground="#c4c4c4")

		self.labelExtension = Label (master)
		self.labelExtension.place(relx=0.05,rely=0.16,height=19,width=62)
		self.labelExtension.configure(text='''Extension''')


		self.forbbiden = Entry (master)
		self.forbbiden.place(relx=0.15,rely=0.24,relheight=0.06,relwidth=0.32)
		self.forbbiden.configure(selectbackground="#c4c4c4")

		self.labelForbbiden = Label (master)
		self.labelForbbiden.place(relx=0.05,rely=0.24,height=19,width=45)
		self.labelForbbiden.configure(activebackground="#f9f9f9")
		self.labelForbbiden.configure(text='''Excluir''')

		self.Button1 = Button (master)
		self.Button1.place(relx=0.17,rely=0.35,height=37,width=117)
		self.Button1.configure(command=self.processURL)
		self.Button1.configure(text='''Enviar''')

		

       







if __name__ == '__main__':
	vp_start_gui()


