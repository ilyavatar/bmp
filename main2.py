import os
import shutil
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

WAV_HEADER_SIZE = 44
degree = 8
decode_text_len = 0

def text_to_binary(event):
    return [int(format(ord(elem), 'b')) for elem in event]


def binary_to_text(event):
    return [chr(int(str(elem), 2)) for elem in event]


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

    def decode(self):
        right_side.text.configure(state="normal")
        right_side.text.delete("1.0", "end-1c")
        right_side.text.configure(state="disabled")
        symbols_to_read = decode_text_len + 1

        input_file = open('input.bmp', 'rb')

        wav_header = input_file.read(WAV_HEADER_SIZE)
        data_size = int.from_bytes(wav_header[40:44], byteorder='little')

        if symbols_to_read >= data_size * degree / 16:
            print("Too many symbols to read")
            input_file.close()
            return False

        text = ''

        _, sample_mask = self.create_masks(degree)
        sample_mask = ~sample_mask

        data = input_file.read(data_size)

        read = 0
        while read < symbols_to_read:
            two_symbols = 0
            for step in range(0, 16, degree):
                sample = int.from_bytes(data[:2], byteorder='little') & sample_mask
                data = data[2:]

                two_symbols <<= degree
                two_symbols |= sample
            first_symbol = two_symbols >> 8

            if first_symbol > 15 and first_symbol < 80 and first_symbol != 32:
                first_symbol += 1024
            text += (chr(first_symbol))
            read += 1

            if chr(first_symbol) == '\n' and len(os.linesep) == 2:
                read += 1

            if symbols_to_read - read > 0:
                second_symbol = two_symbols & 0b0000000011111111

                if second_symbol > 15 and second_symbol < 80 and second_symbol != 32:
                    second_symbol += 1024
                text += (chr(second_symbol))
                read += 1

                if chr(second_symbol) == '\n' and len(os.linesep) == 2:
                    read += 1

        input_file.close()
        right_side.text.configure(state="normal")
        right_side.text.insert("1.0", text)
        right_side.text.configure(state="disabled")
        print(text)
        return True, text

    def create_masks(self, degree):
        text_mask = 0b1111111111111111
        sample_mask = 0b1111111111111111

        text_mask <<= (16 - degree)
        text_mask %= 65536
        sample_mask >>= degree
        sample_mask <<= degree

        return text_mask, sample_mask

    def encode(self):
        text_file = left_side.text.get(1.0, "end-1c")
        input_file = open(left_side.image_path, 'rb')

        text_len = len(text_file) - 1

        wav_header = input_file.read(WAV_HEADER_SIZE)
        data_size = int.from_bytes(wav_header[40:44], byteorder='little')
        print(data_size)
        if text_len > data_size * degree / 16.0:
            print("Too big text to encode")
            input_file.close()
            return False

        text = text_file
        output_wav = open('output.bmp', 'wb')
        output_wav.write(wav_header)

        data = input_file.read(data_size)
        text_mask, sample_mask = self.create_masks(degree)
        i = 0
        while True:
            if i >= len(text):
                break

            txt_symbol = text[i]

            txt_symbol = ord(txt_symbol)

            txt_symbol <<= 8

            for step in range(0, 16, degree):
                if step == 8 and not txt_symbol:
                    break

                sample = int.from_bytes(data[:2], byteorder='little') & sample_mask
                data = data[2:]

                bits = txt_symbol & text_mask
                bits >>= (16 - degree)

                sample |= bits

                output_wav.write(sample.to_bytes(2, byteorder='little'))
                txt_symbol = (txt_symbol << degree) % 65536
                i += 1

        output_wav.write(data)
        output_wav.write(input_file.read())

        input_file.close()
        output_wav.close()

        right_side.image_path = "output.bmp"
        right_side.name["text"] = right_side.image_path
        right_side.find_image(right_side.image_path)
        right_side.c_image = right_side.canvas.create_image(0, 0, anchor='nw', image=right_side.photo)
        right_side.canvas.pack(before=right_side.name)

        global decode_text_len
        decode_text_len = text_len

        return True


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
