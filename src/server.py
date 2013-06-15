#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, static_file, template
from spatialite_routing import Route
import argparse

kml_template = open("template.kml", "r").read()
dbfile = "routing.sqlite"

@route('/')
def index():
    route = Route(dbfile)
    center = route.get_center()
    route.close()
    return template("index.html", center_x = center[0], center_y = center[1])

@route('/js/<path:path>')
def js(path):
    return static_file(path, root='js')

@route('/hello')
def hello():
    return "Everyday a star is born (Can you say New York City?) Clap for 'em, clap for 'em, clap for 'em, hey"

@route('/route/<start>/<end>')
def route(start, end):
    # ex: 7.4218041,43.736974400000001, 7.4186261,43.725380600000001
    route = Route(dbfile)
    lat_from, lng_from = tuple(map(float, start.split(",")))
    lat_to, lng_to = tuple(map(float, end.split(",")))
    path = route.route(lat_from, lng_from, lat_to, lng_to)
    route.close()
    return template(kml_template, path=path)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("database")
    args = parser.parse_args()
    dbfile = args.database
    run(host='localhost', port=8080, debug=True)
