import psycopg2
from psycopg2 import Error
import math
import os
import os.path
import sys
import configparser
import math
import DB_read_file as a
import DB as database
#create table polygon

create_table_query = ('''
		select (ST_DUMP(ST_UNION(ST_BUFFER((wkb_geometry),0.00000005)))).geom as wkb_geometry
		from map2
		WHERE ST_Area(wkb_geometry::geography) > 3;
		
		drop table map2;
		''')
		
#insert table polygon
Make_insert = ('''
		with dissolve as (select (ST_DUMP(ST_UNION(ST_BUFFER((wkb_geometry),0.00000005)))).geom AS wkb_geometry
		from map2
		WHERE ST_Area(wkb_geometry::geography) > 3)
		select a.wkb_geometry
		from dissolve a
		WHERE not EXISTS (
			SELECT b.wkb_geometry 
			FROM mapedit2 b
			WHERE a.wkb_geometry = b.wkb_geometry or ST_Within(a.wkb_geometry,b.wkb_geometry));

		drop table map2;
		''')

Dissolve_script= ('''
	select (ST_DUMP(ST_Simplify(ST_UNION(ST_BUFFER((wkb_geometry),0.00000005)),0.000005))).geom as wkb_geometry
	from mapedit2;

	''')

getDB = database.DBConnect()
cursor = getDB.cursor()

#check table exists or not
def checkTableExists(dbcon, tablename):
    cursor.execute('''
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        '''.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    return False

#Clean image
def Checkdissolve():
	if (checkTableExists('vector','map2')) :
		if (checkTableExists('vector','mapedit2')) :
			cursor.execute('''insert into mapedit2(wkb_geometry) '''+ Make_insert)
			getDB.commit()
			#print("Table Insert")
		else :
			cursor.execute('''create table mapedit2 as '''+ create_table_query)
			getDB.commit()
			#print("Table Create")

def dissolve():
	if (checkTableExists('vector','mapdissolve2')) :
		dissolve = ('''drop table mapdissolve2; ''')
		cursor.execute(dissolve)
		getDB.commit()
	dissolve = ('''create table mapdissolve2 as ''' + Dissolve_script)
	cursor.execute(dissolve)
	getDB.commit()

#calculate Tile numbers to lon./lat.
def num2deg(xtile, ytile, zoom):
		n = 2.0 ** zoom
		lon_deg = xtile / n * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
		lat_deg = math.degrees(lat_rad)
		lat_deg = lat_deg * -1
		return (lat_deg, lon_deg)

#caluculate lat, lon to tile numbers
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 + math.log((math.tan(lat_rad)) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


#Download Image .png
def ImageDownload(zoom , Gety, Getx):
	#print("start loading")
	url = ("http://ms.longdo.com/mapproxy/tms/1.0.0/dol/EPSG3857/" + str(zoom) + "/" + str(Gety) + "/" + str(Getx) + ".png")
	#print(url)
	Dload = ("curl -o test/Map.png " + url)
	os.system(Dload)

	#print("finish loading")


#curl -o test/Map.png http://ms.longdo.com/mapproxy/wmts/dol/GLOBAL_WEBMERCATOR/19/408150/282985.png
