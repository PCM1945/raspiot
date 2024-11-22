# raspiot
A raspberry pi iot playground for thinkering with python APIs and AMQP

# Pre requisites 
* raspberry py 3 B ver 1.2 1 GB 
* Debian bullseye (legacy 64 bits lite) 
    * note: dht sensor lib with bad compatibility when tested with other raspbian versions
* python 3.9.2

# install dependencies  
```console
$ sudo apt-get install python3-dev
```
```console
$ pip install --upgrade pip setuptools wheel
```

# Running the API 
 The idea is that it will aromatically be running when the pi is powered on however, to manually  run the api use the following command: 
```console
$ python3 main.py 
```