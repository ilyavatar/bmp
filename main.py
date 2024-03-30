import shutil
import eel
import wx
import os
import platform
import getpass

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
    system = platform.system()
    userName = getpass.getuser()
    print(system)
    path = "~"
    if system == "Darwin":
        path = os.path.expanduser("~/Downloads")
    elif system == "Windows":
        path = os.path.expanduser(r"C:/Users/" + userName + r"/Downloads")
    elif system == "Linux":
        path = os.path.expanduser("/home/" + userName + "/Загрузки")

    shutil.copyfile("web/tmp/result.bmp", path + "/result.bmp")


@eel.expose
def encrypt(text, bit):
#     Алгоритм кодирования
    filePath = "web/tmp/input.bmp"
    # with open(filePath, 'w') as f:
    #     print(f)
    #
    # f.close()
    shutil.copyfile("web/tmp/input.bmp", "web/tmp/result.bmp")

@eel.expose
def decrypt(text, bit):
    #     Алгоритм декодирования
    # filePath = "web/tmp/input.bmp"
    # with open(filePath, 'w') as f:
    #     print(f)
    #
    # f.close()
    shutil.copyfile("web/tmp/input.bmp", "web/tmp/result.bmp")

# Set web files folder
eel.init('web')

eel.start('main_page.html', mode="chrome")  # Start
