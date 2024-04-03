import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

WAV_HEADER_SIZE = 44
degree = 8

def text_to_binary(event):
    return [int(format(ord(elem), 'b')) for elem in event]


def binary_to_text(event):
    return [chr(int(str(elem), 2)) for elem in event]


class Centre(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief='raised')

        self.encode = tk.Button(self, text='Зашифровать',
                              foreground='blue',
                              activebackground='white',
                              command=self.click_button
                              )
        self.encode.pack()

        self.decode = tk.Button(self, text='Расшифровать',
                              foreground='blue',
                              activebackground='white',
                              command=self.decode_wav
                              )
        self.decode.pack()

    def decode_wav(self):
        """
        This function takes symbols_to_read bytes from encoded WAV audio file and
        retrieves hidden information from them with a given degree.
        Single portion of data can be written only in 2 bytes by one so maximum
        information portion size is 16 bits.
        Thus text size should be less than (data_size * degree / 16)

        :param input_wav_name: name of WAV input audio file
        :param symbols_to_read:
        :return: True if function succeeds else False
        """

        symbols_to_read = 10

        input_wav = open('test.bmp', 'rb')

        wav_header = input_wav.read(WAV_HEADER_SIZE)
        data_size = int.from_bytes(wav_header[40:44], byteorder='little')

        if symbols_to_read >= data_size * degree / 16:
            print("Too many symbols to read")
            input_wav.close()
            return False

        text = ''

        _, sample_mask = self.create_masks(degree)
        sample_mask = ~sample_mask

        data = input_wav.read(data_size)

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

        input_wav.close()
        print(text)
        return True, text
    def create_masks(self, degree):
        """
        Create masks for taking bits from text bytes and
        putting them to image bytes.

        :param degree: number of bits from byte that are taken to encode text data in audio
        :return:  mask for a text and a mask for a sample
        """
        text_mask = 0b1111111111111111
        sample_mask = 0b1111111111111111

        text_mask <<= (16 - degree)
        text_mask %= 65536
        sample_mask >>= degree
        sample_mask <<= degree

        return text_mask, sample_mask

    def click_button(self):

        text_file = 'abcfghmkwf'
        input_wav = open(left_side.image_path, 'rb')

        text_len = len(text_file) - 1

        wav_header = input_wav.read(WAV_HEADER_SIZE)
        data_size = int.from_bytes(wav_header[40:44], byteorder='little')
        print(data_size)
        if text_len > data_size * degree / 16.0:
            print("Too big text to encode")
            input_wav.close()
            return False

        text = text_file
        output_wav = open('test.bmp', 'wb')
        output_wav.write(wav_header)

        data = input_wav.read(data_size)
        text_mask, sample_mask = self.create_masks(degree)
        i = 0
        while True:
            if i == len(text):
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
        output_wav.write(input_wav.read())

        input_wav.close()
        output_wav.close()

        return True


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

        self.canvas = tk.Canvas(self)
        self.find_image(self.image_path)
        self.c_image = self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.pack()

        self.name = tk.Entry(self)
        self.name.insert(0, self.image_path)
        self.name.config(state='disabled')
        self.name.pack(fill='x')

        self.text = tk.Text(self)
        self.text.pack(after=self.canvas, side='bottom', fill='x')

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
centre = Centre(root)
right_side = OneSide(root, 'Save', 'web/tmp/sample_1280×853.bmp')
left_side.pack(side='left', padx=10)
centre.pack(side='left', padx=10)
right_side.pack(side='left', padx=10)
root.mainloop()
