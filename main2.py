import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from PIL import Image, ImageTk


class OneSide(tk.Frame):
    def __init__(self, master=None, button_text='', image_path='', entry_placeholder=''):
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
        self.name.pack(fill='x')

        self.canvas = tk.Canvas(self)
        self.find_image(self.image_path)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack(before=self.name)

        self.entry = ttk.Entry(self, foreground="#8B8B8B")
        self.entry.placeholder = entry_placeholder
        self.entry.insert(0, self.entry.placeholder)
        self.entry.pack(fill='x', pady=30)

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

class Center(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief='raised')
        self.master = master

        self.encrypt = tk.Button(self, text="Зашифровать",
                              # bg="green",
                              # fg='white',
                              command=self.encrypt
                              )
        self.encrypt.pack()

        self.decrypt = tk.Button(self, text="Расшифровать",
                              # bg="green",
                              # fg='white',
                              command=self.decrypt
                              )
        self.decrypt.pack(pady=10)

        self.name = tk.Entry(self)
        self.name.insert(0, "Сколько бит заменять?")
        self.name.config(state='disabled')
        self.name.pack(fill='x')

        self.entry = ttk.Entry(self, foreground="#8B8B8B")
        self.entry.placeholder = "Введите количество бит"
        self.entry.insert(0, self.entry.placeholder)
        self.entry.pack(fill='x')

    def encrypt(self):
        print(1)

    def decrypt(self):
        print(1)


root = tk.Tk()
left_side = OneSide(root, 'Load', 'web/tmp/input.bmp', "Введите сообщение")
center = Center(root)
right_side = OneSide(root, 'Save', 'web/tmp/sample_1280×853.bmp')
left_side.pack(side='left', padx=10)
center.pack(side='left', padx=10)
right_side.pack(side='right', padx=10)
root.mainloop()
