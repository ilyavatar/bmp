import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


class OneSide(tk.Frame):
    def __init__(self, master=None, button_text='', image_path=''):
        tk.Frame.__init__(self, master, relief='raised')
        self.image = None
        self.photo = None
        self.button_text = button_text
        self.image_path = image_path
        self.master = master

        self.edit = tk.Button(self, text=button_text,
                              foreground='red',
                              activebackground='white',
                              command=self.click_button
                              )
        self.edit.pack()

        self.name = tk.Entry(self)
        self.name.insert(0, self.image_path)
        self.name.config(state='disabled')
        self.name.pack(side='bottom', fill='x')

        self.canvas = tk.Canvas(self)
        self.find_image(self.image_path)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack(before=self.name, side='bottom')

    def find_image(self, image_path):
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    def click_button(self):
        if self.button_text == 'Load':
            self.image_path = filedialog.askopenfilename()
            if self.image_path != "":
                self.name.insert(0, self.image_path)
                self.find_image(self.image_path)
                self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)


root = tk.Tk()
left_side = OneSide(root, 'Load', 'web/tmp/input.bmp')
right_side = OneSide(root, 'Save', 'web/tmp/sample_1280×853.bmp')
left_side.pack(side='left', padx=10)
right_side.pack(side='left', padx=10)
root.mainloop()
