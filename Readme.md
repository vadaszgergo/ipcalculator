# IP Calculator python application with HTML frontend

A Python application suite to perform various IP address-related calculations.


## Features
**Standard IP calculator:**

A similar tool like the command line ipcalc. It gives you details about subnet, netmask, host min and max, etc.

**IP complement calculator:**

Once given various IP ranges (`10.0.0.0/24`, `130.10.0.0/16`, `192.168.1.1/32`) the application calculates what are all other IP ranges which are not part of the given ranges. Example would be for `0.0.0.0/1` complement range would be `128.0.0.0/1`.


**IP consolidator calculator:** 

Once given various single IP addresses (`10.1.1.0`, `10.1.1.1`, `10.1.1.2`, `10.1.1.3`) the application calculates the biggest subnet range, that contains all given ip addresses, in this example it would result in `10.1.1.0/30`.


### Installation

1. Running locally with python
```
# Clone this repository
git clone https://github.com/vadaszgergo/ipcalculator.git

# Change directory to ip-tools
cd ip-tools
python3 app.py

# It will run on localhost port 5000
Running on http://127.0.0.1:5000
```

2. Build your own docker image and run it

```
# Change directory to the application
cd ip-tools

# Build the docker image from the application directoy
docker build -t yourapplicationname .

# Run the local docker image
docker run -p 5000:5000 yourapplicationname
```

3. Running without the source code, pulling from docker hub

```
# IP Tools application
docker run -p 5000:5000 vadaszgergo/ip-tools:latest
```
