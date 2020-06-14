#!/usr/bin/env python3

import guizero

app = guizero.App(title="hello world")

welcome_message = guizero.Text(app, text="Welcome to my app")
my_name = guizero.TextBox(app)

def say_my_name():
    welcome_message.value = my_name.value

def change_text_size(slider_value):
    welcome_message.size = slider_value

update_text = guizero.PushButton(
    app,
    command=say_my_name,
    text="Display my name")

text_size = guizero.Slider(app, command=change_text_size, start=10, end=80)

app.display()
