#!/usr/bin/env python3

import guizero

app = guizero.App(title="My second GUI app", width=300, height=200, layout="grid")

combo_label = guizero.Text(app, text="Which film?", grid=[0, 0], align='left')
film_choice = guizero.Combo(app, options=['Star Wars', 'Frozen', 'Lion King'], grid=[1, 0], align="left")

cbox_label = guizero.Text(app, text="Seat Type", grid=[0, 1], align='left')
vip_seat = guizero.CheckBox(app, text="VIP seat?", grid=[1, 1], align='left')

row_choice = guizero.ButtonGroup(
    app,
    options=[
        ["Front", "F"],
        ["Middle", "M"],
        ["Back", "B"]
    ],
    selected="M",
    horizontal=True,
    grid=[1, 2],
    align="left")

def do_booking():
    print(film_choice.value)
    print(vip_seat.value)
    print(row_choice.value)
    guizero.info("Booking", "Thank you for booking")

book_seats = guizero.PushButton(app, command=do_booking, text="Book Seat", grid=[1, 3], align="left")

app.display()
