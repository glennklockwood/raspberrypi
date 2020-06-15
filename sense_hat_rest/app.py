#!/usr/bin/env python3
"""Crumby REST API for the Sense Hat

Adapted from the example in the Flask-RESTful documentation
"""

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

import sense_hat

app = Flask(__name__)
api = Api(app)
sense = sense_hat.SenseHat()

class Sense(Resource):
    def get(self):
        return {}

class Humidity(Resource):
    def get(self):
        return {
            "value": sense.get_humidity(),
            "units": "percent"
        }

class Temperature(Resource):
    def get(self):
        return {
            "value": sense.get_temperature_from_humidity(),
            "units": "celsius",
            "from": "humidity"
        }

class Pressure(Resource):
    def get(self):
        return {
            "value": sense.get_pressure(),
            "units": "millibar"
        }

class Pixel(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('x', type=int, help="X coordinate of LED (0-7)")
        self.get_parser.add_argument('y', type=int, help="Y coordinate of LED (0-7)")

        self.put_parser = self.get_parser.copy()
        self.put_parser.add_argument('r', type=int, help="red component of desired color (0-255)", required=True)
        self.put_parser.add_argument('g', type=int, help="green component of desired color (0-255)", required=True)
        self.put_parser.add_argument('b', type=int, help="blue component of desired color (0-255)", required=True)

    def get(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            abort(422, message="x, y must be integers")
        self.check_coords(x=x, y=y)
        return sense.get_pixel(x, y)

    def delete(self, x, y):
        self.check_coords(x=x, y=y)
        sense.set_pixel(x, y, 0, 0, 0)
        return sense.get_pixel(x, y), 204

    def put(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueeError:
            abort(422, message="x, y must be integers")
        args = self.put_parser.parse_args(strict=True)
        self.check_coords(x=x, y=y)
        check_color(r=args['r'], g=args['g'], b=args['b'])
        sense.set_pixel(x, y, args['r'], args['g'], args['b'])
        return sense.get_pixel(x, y), 201

    @staticmethod
    def check_coords(x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            abort(404, message="x, y must be between 0 and 7")

def check_color(r=None, g=None, b=None, *args):
    if args:
        abort(404, message="must specify only r, g, b")
    if r is None or g is None or b is None:
        abort(404, message="must specify r, g, and b")
    if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or g > 255:
        abort(404, message="r, g, b must be between 0 and 255")

class Pixels(Resource):
    def get(self):
        pixels = sense.get_pixels()
        return [
            {"x": i % 8, "y": i // 8, "r": j[0], "g": j[1], "b": j[2]} for i, j in enumerate(pixels)
        ]

class DisplayMessage(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('text_string', type=str, required=True, help="Message to scroll")
        self.put_parser.add_argument('scroll_speed', type=float, help="Speed at which text should scroll in seconds")
        self.put_parser.add_argument('text_colour', type=int, action='append', help="List containing the R-G-B (red, green, blue) colour of the text")
        self.put_parser.add_argument('back_colour', type=int, action='append', help="List containing the R-G-B (red, green, blue) colour of the background")

    def put(self):
        """This is currently blocking"""
        args = self.put_parser.parse_args()
        for arg in 'text_colour', 'back_colour':
            if args.get(arg) is not None:
                check_color(*args[arg])
        valid_args = {}
        for valid_arg in 'text_string', 'scroll_speed', 'text_colour', 'back_colour':
            if args.get(valid_arg) is not None:
                valid_args[valid_arg] = args[valid_arg]
        
        sense.show_message(**valid_args)
        return { "message": "OK" }, 204

class DisplayLetter(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('s', type=str, required=True, help="Message to scroll")
        self.put_parser.add_argument('text_colour', type=int, action='append', help="List containing the R-G-B (red, green, blue) colour of the text")
        self.put_parser.add_argument('back_colour', type=int, action='append', help="List containing the R-G-B (red, green, blue) colour of the background")

    def put(self):
        """This is currently blocking"""
        args = self.put_parser.parse_args()
        for arg in 'text_colour', 'back_colour':
            if args.get(arg) is not None:
                check_color(*args[arg])
        valid_args = {}
        for valid_arg in 's', 'text_colour', 'back_colour':
            if args.get(valid_arg) is not None:
                valid_args[valid_arg] = args[valid_arg]
        
        sense.show_letter(**valid_args)
        return { "message": "OK" }, 204

api.add_resource(Sense, '/sense')
api.add_resource(DisplayMessage, '/sense/display/message')
api.add_resource(DisplayLetter, '/sense/display/letter')
api.add_resource(Pixels, '/sense/display/pixel')
api.add_resource(Pixel, '/sense/display/pixel/<x>/<y>')
api.add_resource(Humidity, '/sense/humidity')
api.add_resource(Pressure, '/sense/pressure')
api.add_resource(Temperature, '/sense/temperature')

if __name__ == '__main__':
    sense.clear()
    app.run('0.0.0.0', debug=True)
