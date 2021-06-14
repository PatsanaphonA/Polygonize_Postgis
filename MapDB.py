import os
import os.path
import sys
from osgeo import gdal
from PIL import Image, ImageOps
import datetime
import Process as pa
import DB
import DB_read_file as DBR
import Check_folder as Check_F 

Check_F.Check_folder()
x = datetime.datetime.now()
print(x)
#Map Location LOOP
#X1 = 564580
#Y1 = 816970
#http://ms.longdo.com/mapproxy/tms/1.0.0/dol/EPSG3857/17/204195/141028.png
zoom = 19 

get = [14.150687,100.254603,13.443849,100.971461]
Y1_num,X1_num = pa.deg2num(get[0],get[1],zoom+1)
Y2_num,X2_num = pa.deg2num(get[2],get[3],zoom+1)

X1 = X1_num - 78 #< make it continue from X location
Y1 = Y1_num + 0 #< make it continue from Y location

#X1 = 141195
#Y1 = 204343
X2 = X1 + 1
Y2 = Y1 + 1

#Loop num increase
#dissolve size
Getx = X1
Gety = Y1
Getx2 = X2
Gety2 = Y2

sumX = 50	#< change size of dissolve X
sumY = 50	#< change size of dissolve Y
i = X1 - sumX 	#< replace "X1 - sumX" to X2_num here for full donwload
o = Y1 + sumY 	#< replace "Y1 + sumY" to Y2_num here for full download
count = 1
#3700
#2900
#start Loop download
while Getx > i: 
	while Gety < o:
		#Map location FOR URL
		pa.ImageDownload(zoom,Gety,Getx)
		#Y,lon  X,lat  zoom
		Y1_tile,X1_tile = pa.num2deg(Gety,Getx,zoom+1)
		Y2_tile,X2_tile = pa.num2deg(Gety2,Getx2,zoom+1)
		
		#Add more read Line in .png  							 V       V
		command = ("convert test/Map.png -fuzz 85% -fill red +opaque none testoutput/BG/Map.png")
		os.system(command)
		command1 = ("convert testoutput/BG/Map.png -background none testoutput/Png/Map.png")
		os.system(command1)

		#Flip .png cause polygonize m ake .png flip. So let flip it first ,it will make it correct .png
		im = Image.open(r'testoutput/Png/Map.png')
		im_mirror = ImageOps.flip(im)
		im_mirror.save(r'testoutput/Flip/Map.png')

		#Give .png location and translate to .tif and CRS location
		command2 = ("gdal_translate -co 'WORLDFILE=YES' -a_srs EPSG:4326 -a_ullr " + str(X1_tile) + " " + str(Y1_tile) + " " + str(X2_tile) + " " + str(Y2_tile) + " testoutput/Flip/Map.png testoutput/Tiff/Map.png")		
		os.system(command2)

		#Polygonize sent to DB                               V
		command3 = ('gdal_polygonize.py testoutput/Tiff/Map.png -f PostgreSQL PG:" dbname = \'' + DBR.db + '\' user = \'' + DBR.user + '\' host= \'' + DBR.host + '\' port = \'' + DBR.port + '\' password = \'' + DBR.passwd + '\'" map2')
		os.system(command3)

		Gety += 1
		Gety2 = Gety + 1
		print(count)
		if(count % 50 == 0):
			pa.Checkdissolve()
		count += 1
	#Finish X
	pa.Checkdissolve()
	pa.dissolve()
	Getx -= 1
	Getx2 = Getx + 1
	Gety = Y1
	Gety2 = Gety + 1

#Dissolve table
DB.DBclose()
b = datetime.datetime.now()
print(b-x)

#limite off : 
#ALTER SYSTEM SET jit=off; = OFF
# select pg_reload_conf(); = T
# show jit; = OFF

