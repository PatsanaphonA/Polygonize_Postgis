# Polygonize title deep in Docker

Use a python script for call Polygonize on gdal to create polygon by title deep

## System Comnent

1. GDAL
2. Imagemagick
3. Python
4. PostGIS

### Python requirement

- GDAL==3.1.0 (default from docker image)
- Numpy==1.17.4 (default from docker image)
- Wand==0.6.1
- PIL Image==1.5.2
- Psycopg2>=2.7.6
- Configparser==5.0.0

## Docker installation

1. docker-compose build
2. docker-compose run

### Docker image

Python GDAL docker image: osgeo/gdal:ubuntu-full-latest
PostGIS docker image: postgis/postgis

# MacOS Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) and [Homebrew](https://brew.sh/) to instsall library and other.

### Install by using requirements.txt

Use [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip3 install -r requirements.txt
```

### Install Pillow

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow

```

### Install Magick wand

```bash
brew install imagemagick@6
or
brew install imagemagick
```


### Installing Gdal

>>>
#### Gdal on Macos(catalina)

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install gdal 

gdal-config --version 
Ex:3.0.4

pip3 install — upgrade pip 

pip3 install gdal==3.0.4 

```

>>>

#### Python-Psycopge2 on MacOS

```bash
brew install postgresql
```




## Create config file

1. First open TextEdit or Notepad
2. Copy Example code from down below
3. Paste change config
4. Save File name **Database.conf**


>>>

Example: 
[postgresql]
 host = <<**HOSTNAME**>>
 user = <<**USERNAME**>>
 passwd = <<**PASSWORD**>>
 db = <<**DATABASENAME**>>
 port = <<**PORT**>>

>>>


## Reference 

- Requirements.txt
    - https://medium.com/@boscacci/why-and-how-to-make-a-requirements-txt-f329c685181e
- Magick wand
    - https://stackoverflow.com/questions/24803747/how-to-use-or-install-magickwand-on-mac-os-x
- Gdal
    - https://medium.com/@vascofernandes_13322/how-to-install-gdal-on-macos-6a76fb5e24a4
    - https://stackoverflow.com/questions/37294127/python-gdal-2-1-installation-on-ubuntu-16-04/37314991
    - https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
    - https://medium.com/@egiron/how-to-install-gdal-and-qgis-on-macos-catalina-ca690dca4f91
- Psycopg2
    - https://pypi.org/project/psycopg2/
    - https://stackoverflow.com/questions/33866695/install-psycopg2-on-mac-osx-10-9-5
    - https://stackoverflow.com/questions/11583714/install-psycopg2-on-ubuntu
- Pillow
    - https://stackoverflow.com/questions/20060096/installing-pil-with-pip/21151777
    - https://pillow.readthedocs.io/en/latest/installation.html
