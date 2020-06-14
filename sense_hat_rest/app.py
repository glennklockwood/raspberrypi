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

    def post(self):
        return {}, 201

class Pixel(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('x', type=int, help="X coordinate of LED (0-7)")
        self.get_parser.add_argument('y', type=int, help="Y coordinate of LED (0-7)")

        self.post_parser = self.get_parser.copy()
        self.post_parser.add_argument('r', type=int, help="red component of desired color (0-255)", required=True)
        self.post_parser.add_argument('g', type=int, help="green component of desired color (0-255)", required=True)
        self.post_parser.add_argument('b', type=int, help="blue component of desired color (0-255)", required=True)

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

    def post(self, x, y):
        try:
            x = int(x)
            y = int(y)
        except ValueeError:
            abort(422, message="x, y must be integers")
        args = self.post_parser.parse_args(strict=True)
        self.check_coords(x=x, y=y)
        self.check_color(r=args['r'], g=args['g'], b=args['b'])
        sense.set_pixel(x, y, args['r'], args['g'], args['b'])
        return sense.get_pixel(x, y), 201

    @staticmethod
    def check_coords(x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            abort(404, message="x, y must be between 0 and 7")

    @staticmethod
    def check_color(r, g, b):
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or g > 255:
            abort(404, message="r, g, b must be between 0 and 255")

api.add_resource(Sense, '/sense')
api.add_resource(Pixel, '/sense/pixel/<x>/<y>')

if __name__ == '__main__':
    sense.clear()
    app.run('0.0.0.0', debug=True)
