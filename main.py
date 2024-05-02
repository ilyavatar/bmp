import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

HEADER_SIZE = 44
degree = 8
decode_text_len = 0


def configure_ok_button(event):
    decode_text = left_side.text.get(1.0, "end-1c").replace(' ', '')
    state_encode = "disabled"
    if decode_text != '':
        state_encode = "active"

    center.encode.configure(state=state_encode)


class Center(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief='raised')

        self.encode = tk.Button(self, text='Зашифровать',
                                foreground='blue',
                                activebackground='white',
                                command=self.encode,
                                state="disabled"
                                )
        self.encode.pack()

        self.decode = tk.Button(self, text='Расшифровать',
                                foreground='blue',
                                activebackground='white',
                                command=self.decode,
                                state="disabled"
                                )
        self.decode.pack()


    def encode(self):
        text_to_encode = left_side.text.get(1.0, "end-1c")
        input_file = open("input.bmp", 'rb')

        text_len = len(text_to_encode) - 1

        header = input_file.read(HEADER_SIZE)
        data_size = os.stat("input.bmp").st_size
        if text_len > data_size * degree / 8.0 - HEADER_SIZE:
            print("Too big text to encode")
            input_file.close()
            return False

        text = text_to_encode
        output_file = open('output.bmp', 'wb')
        output_file.write(header)

        text_mask, sample_mask = self.create_masks(degree)

        i = 0
        while True:
            if i >= len(text):
                break

            txt_symbol = text[i]
            txt_symbol = ord(txt_symbol)

            for step in range(0, 8, degree):
                sample = int.from_bytes(input_file.read(1), sys.byteorder) & sample_mask
                bits = txt_symbol & text_mask
                bits >>= (8 - degree)
                sample |= bits

                output_file.write(sample.to_bytes(1, sys.byteorder))
                txt_symbol = txt_symbol << degree
                i += 1

        output_file.write(input_file.read())

        input_file.close()
        output_file.close()

        right_side.image_path = "output.bmp"
        right_side.name["text"] = right_side.image_path
        right_side.find_image(right_side.image_path)
        right_side.c_image = right_side.canvas.create_image(0, 0, anchor='nw', image=right_side.photo)
        right_side.canvas.pack(before=right_side.name)

        global decode_text_len
        decode_text_len = text_len

        return True


    def decode(self):
        right_side.text.configure(state="normal")
        right_side.text.delete("1.0", "end-1c")
        right_side.text.configure(state="disabled")
        symbols_to_read = decode_text_len + 1

        input_file = open('input.bmp', 'rb')

        data_size = os.stat('input.bmp').st_size
        if symbols_to_read >= data_size * degree / 8 - HEADER_SIZE:
            print("Too many symbols to read")
            input_file.close()
            return False

        text = ''
        input_file.seek(HEADER_SIZE)

        _, sample_mask = self.create_masks(degree)
        sample_mask = ~sample_mask

        # data = input_file.read(data_size)

        read = 0
        while read < symbols_to_read:
            symbol = 0
            for step in range(0, 8, degree):
                sample = int.from_bytes(input_file.read(1), sys.byteorder) & sample_mask
                symbol <<= degree
                symbol |= sample

            if chr(symbol) == '\n' and len(os.linesep) == 2:
                read += 1

            read += 1
            text += (chr(symbol))

        input_file.close()
        right_side.text.configure(state="normal")
        right_side.text.insert("1.0", text)
        right_side.text.configure(state="disabled")
        return True, text

    def create_masks(self, degree):
        text_mask = 0b11111111
        img_mask = 0b11111111

        text_mask <<= (8 - degree)
        text_mask %= 256
        img_mask >>= degree
        img_mask <<= degree

        return text_mask, img_mask


class OneSide(tk.Frame):
    def __init__(self, master=None, button_text='', image_path='', entry_placeholder='', state_text_field='normal'):
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

        self.canvas = tk.Canvas(self)
        self.find_image(self.image_path)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack()

        self.name = tk.Label(self, text=self.image_path)
        self.name.pack(fill='x')

        self.placeholder = tk.Label(self, text=entry_placeholder, anchor="w")
        self.placeholder.pack(fill='x')

        self.text = tk.Text(self, width=50, state=state_text_field)
        self.text.bind("<KeyRelease>", configure_ok_button)
        self.text.pack(after=self.canvas, side='bottom', fill='x')

    def find_image(self, image_path):
        try:
            self.image = Image.open(image_path)
            scalled = self.image.resize((320, 250))
            self.photo = ImageTk.PhotoImage(scalled)
        except AttributeError as ignore:
            pass

    def click_button(self):
        if self.button_text == 'Загрузить изображение из файла':
            self.image_path = filedialog.askopenfilename()
            if self.image_path != "":
                self.name["text"] = self.image_path
                self.find_image(self.image_path)
                self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
                self.canvas.pack()
                shutil.copyfile(self.image_path, "input.bmp")
                center.decode.configure(state="active")
        elif self.button_text == "Сохранить изображение в файл":
            save_image_path = filedialog.asksaveasfilename(defaultextension='bmp')
            if save_image_path is None:
                return
            shutil.copyfile("output.bmp", save_image_path)
            right_side.text.insert("1.0", save_image_path)


root = tk.Tk()
left_side = OneSide(root, 'Загрузить изображение из файла', '', "Введите сообщение для кодирования")
center = Center(root)
right_side = OneSide(root, 'Сохранить изображение в файл', '', 'Раскодированное сообщение', 'disabled')
left_side.pack(side='left', padx=10)
center.pack(side='left', padx=20)
right_side.pack(side='left', padx=10)
root.mainloop()
