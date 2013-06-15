#!/usr/bin/python

from pysqlite2 import dbapi2 as sqlite

class Route:
    def __init__(self, db):
        self.conn = sqlite.connect(db)
        self.conn.enable_load_extension(True)
        self.conn.load_extension("libspatialite.so.3")

    def route(self, lat_from, lng_from, lat_to, lng_to):
        node_from = self.geoloc(lat_from, lng_from)
        node_to = self.geoloc(lat_to, lng_to)
        kml = self.route_query(node_from, node_to)
        self.close()
        return kml

    def geoloc(self, lat, lng):
        cur = self.conn.cursor()
        query = """SELECT node_from  
        FROM roads 
        order by distance(geometry, PointFromText('Point({} {})')) limit 1
        """.format(lat, lng)
        cur.execute(query)
        rec = cur.fetchone()
        print "Loc : {}".format(rec[0])
        return rec[0]

    def get_center(self):
        cur = self.conn.cursor()
        query = """
            SELECT X(center) as x, Y(center) as y FROM (
                SELECT ST_Transform(
                    SetSrid(Centroid(Extent(geometry)), 4326), 
                  3785) as center FROM roads
            )
        """
        cur.execute(query)
        rec = cur.fetchone()
        return rec

    def close(self):        
        self.conn.close()

    def route_query(self, node_from, node_to):
        cur = self.conn.cursor()
        query = 'SELECT askml(geometry) FROM "roads_net" where nodeFrom=? and nodeTo=? limit 1'
        cur.execute(query, (node_from, node_to))
        rec = cur.fetchone()
        return rec[0]

if __name__ == "__main__":
    route = Route()
    print route.geoloc(7.4218041,43.736974400000001)
    #print route.route(7.4218041,43.736974400000001, 7.4186261,43.725380600000001)
    #7.4216203,43.736849599999999 7.4215651,43.736816900000001 7.4215168,43.736761399999999 7.4214475,43.736682000000002 7.4213402,43.736496000000002 7.4211953,43.736148999999997 7.4211465,43.735773100000003 7.421157,43.735433899999997 7.421162,43.735385700000002 7.4211865,43.735176199999998 7.4212222,43.734875799999998 7.4212424,43.734785100000003 7.4213188,43.734441699999998 7.4213423,43.734383999999999 7.4215012,43.733899000000001 7.4216019,43.733663999999997 7.4217763,43.733321799999999 7.4218826,43.7331407 7.4220069,43.732986799999999 7.4222349,43.7326999 7.4223137,43.732551399999998 7.4223248,43.732435799999998 7.4222652,43.732311299999999 7.4221807,43.7322335 7.421501,43.731947400000003 7.4206102,43.7316954 7.4194352,43.731430600000003 7.4189799,43.731278699999997 7.4186151,43.731162400000002 7.4183756,43.731031100000003 7.4180572,43.730805799999999 7.4173598,43.730294100000002 7.4171084,43.730106599999999 7.4170402,43.729990299999997 7.417043,43.729931999999998 7.4171105,43.729916500000002 7.4172141,43.729860299999999 7.4173184,43.729753199999998 7.4176344,43.729473900000002 7.4178142,43.729165999999999 7.4178638,43.7289806 7.4179185,43.728759099999998 7.4179525,43.728374700000003 7.4179606,43.728278400000001 7.418175,43.728275699999998 7.4183683,43.728231899999997 7.4185473,43.7281482 7.4187007,43.728017100000002 7.4187493,43.727892799999999 7.4187849,43.7277676 7.4187437,43.727617600000002 7.4186843,43.727511 7.4186683,43.727488899999997 7.4184226,43.727359900000003 7.4182314,43.7273481 7.4181583,43.727179499999998 7.4180258,43.726906100000001 7.4177405,43.726593999999999 7.4171611,43.726399999999998 7.4173937,43.726275200000003 7.4180361,43.7258274 7.4185815,43.725452400000002 

