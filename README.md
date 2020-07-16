Icecast python client
=======================

Using Python 3.7

based on [python-shout3](https://pypi.org/project/python-shout3/) 

### Icecast basic setup

`sudo  apt-get install icecast2`

setup icecast2 xml config file

`sudo nano /etc/icecast2/icecast.xml`

[Icecast Docs](https://www.icecast.org/docs/icecast-trunk/basic_setup/)

## Installation and run

`Please note: you must install libshout3 and libshout3-dev before installing python-shout3 package!`

`sudo apt-get install libshout3, libshout3-dev`

$ pip install -r requirements.txt

$ python client.py
