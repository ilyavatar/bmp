import shutil
import eel
import wx

# @eel.expose
# def cls_func(cls):
#     if (cls.startswith('Загрузить')):
#         print('ЗагрузОчка')
#     elif (cls.startswith('Сохранить')):
#         with open('output.txt', 'w') as file:
#             file.write('Сохранил какие-то данные')

@eel.expose
def downloadImage(wildcard="*"):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        # Сделать всякие проверки (например, что это bmp файл)
        name = dialog.GetFilename()
        shutil.copyfile(path, "web/tmp/input.bmp")
    else:
        name = "error.png"
    dialog.Destroy()
    return [name, "input.bmp"]

@eel.expose
def saveImage(wildcard="*"):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

# @eel.expose
# def encrypt(text, bit):

# @eel.expose
# def encrypt(text, bit):


# Set web files folder
eel.init('web')

# @eel.expose                         # Expose this function to Javascript
# def say_hello_py(x):
#     print('Hello from %s' % x)
#
# say_hello_py('Python World!')
# eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('main_page.html', mode="chrome")  # Start
