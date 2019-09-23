from turtle import onscreenclick
from time import sleep
import tkinter

mouse_event = ""
x_mouse = 0
y_mouse = 0


def set_mouse_buttons(button):
    def result(x, y):
        global mouse_event, x_mouse, y_mouse
        mouse_event, x_mouse, y_mouse = button, x, y

    return result


def give_event():
    global mouse_event, x_mouse, y_mouse
    while mouse_event == "":
        tkinter._default_root.update()
        sleep(0.01)
    pom, mouse_event = mouse_event, ""
    return pom, x_mouse, y_mouse


def ini_myszki():
    for button, number in zip(["l_klik", "m_klik", "r_klik"], range(1, 4)):
        onscreenclick(set_mouse_buttons(button.lower()), number)
