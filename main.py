import eel


@eel.expose
def cls_func(cls):
    if (cls.startswith('Загрузить')):
        print('ЗагрузОчка')
    elif (cls.startswith('Сохранить')):
        with open('output.txt', 'w') as file:
            file.write('Сохранил какие-то данные')


# Set web files folder
eel.init('web')

# @eel.expose                         # Expose this function to Javascript
# def say_hello_py(x):
#     print('Hello from %s' % x)
#
# say_hello_py('Python World!')
# eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('main_page.html', mode="chrome")  # Start
