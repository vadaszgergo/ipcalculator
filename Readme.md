# IP Calculator python application with HTML frontend

A Python application suite to perform various IP address-related calculations.


## Features
1. **IP complement calculator:**

Once given various IP ranges (`10.0.0.0/24`, `130.10.0.0/16`, `192.168.1.1/32`) the application calculates what are all other IP ranges which are not part of the given ranges. Example would be for `0.0.0.0/1` complement range would be `128.0.0.0/1`.


2. **IP consolidator calculator:** 

Once given various single IP addresses (`10.1.1.0`, `10.1.1.1`, `10.1.1.2`, `10.1.1.3`) the application calculates the biggest subnet range, that contains all given ip addresses, in this example it would result in `10.1.1.0/30`.


3. **Combined application for both:**

Single application combining the 2 calculators: single html frontend which contains both calculators in a html page.

