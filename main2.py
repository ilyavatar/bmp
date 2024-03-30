import tkinter as tk
from PIL import Image, ImageTk


class OneSide(tk.Frame):
    def __init__(self, master=None, button_text='', image_path=''):
        tk.Frame.__init__(self, master, relief='raised')
        self.master = master

        self.edit = tk.Button(self, text=button_text,
                              foreground='red',
                              activebackground='white'
                              )
        self.edit.pack()

        self.name = tk.Entry(self, text=image_path)
        self.name.insert(0, image_path)
        self.name.pack(side='bottom', fill='x')

        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack(before=self.name, side='bottom')


root = tk.Tk()
left_side = OneSide(root, 'Load', 'web/tmp/decrypt.bmp')
right_side = OneSide(root, 'Save', 'web/tmp/encrypt.bmp')
left_side.pack(side='left', padx=10)
right_side.pack(side='left', padx=10)
root.mainloop()
