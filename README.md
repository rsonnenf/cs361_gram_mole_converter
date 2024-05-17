# Gram/Mole Converter

# Description
This program is a microservice I implemented for my CS 361 Software Engineering I class. This program uses ZeroMQ to receive a request from another program where the aim is to either convert a value representing the measurement of a substance in grams to a value in moles or vice-versa. 

## Communication Contract

### How to request data from this microservice

To request data, the main program will need to set up a request socket to send requests to the server set up by the microservice. Then, the request data must be compiled in the form of a dictionary, which is sent as a json file to the microservice. 

The following example shows how the microservice is called and how the appropriate data is prepared:

```
import zmq  
  
  
def request_conversion(conversion_type, mass_value, mass_unit, molar_mass):  
    context = zmq.Context()  
    socket = context.socket(zmq.REQ)  # REQ (REQUEST) socket for sending requests  
    socket.connect("tcp://localhost:5555")  # Connect to the server  
  
    # Prepare the request data    request = {  
        'conversion': conversion_type,  
        'mass': mass_value,  
        'unit': mass_unit,  
        'molar_mass': molar_mass  
    }  
  
    # Send the request  
    socket.send_json(request)
```

The arguments of the function call includethe following:

* `conversion_type` - the type of conversion to be made, i.e., "grams_to_moles" or "moles_to_grams". 
* `mass_value` - the number (and only the number) representing the mass to be converted of the substance
* `mass_unit` - the standard unit associated with the mass value, i.e., grams, kilograms etc. The following units are supported: 
	* "G" (giga)
	* "M" (mega)
	* "k" (kilo)
	* "h" (hecto)
	* "da" (deka)
	* "d" (deci)
	* "c" (centi)
	* "m" (milli)
	* "micro" (micro)
	* "n" (nano)
* `molar_mass` - the molar mass of the substance

### How to receive data from the microservice

To receive data, the following code should be added to the end of the above code, within the function:

```
response = socket.recv_json()  
return response
```

Accordingly, the full code (without calls) to properly call the microservice is:

```
import zmq  
  
  
def request_conversion(conversion_type, mass_value, mass_unit, molar_mass):  
    context = zmq.Context()  
    socket = context.socket(zmq.REQ)  # REQ (REQUEST) socket for sending requests  
    socket.connect("tcp://localhost:5555")  # Connect to the server  
  
    # Prepare the request data    request = {  
        'conversion': conversion_type,  
        'mass': mass_value,  
        'unit': mass_unit,  
        'molar_mass': molar_mass  
    }  
  
    # Send the request  
    socket.send_json(request)  
  
    # Wait for the reply  
    response = socket.recv_json()  
    return response
```

Example calls to the microservice include:

```
request_conversion('grams_to_moles', 1, 'g', 18.015)  

request_conversion('moles_to_grams', 0.555, 'moles', 18.015)

request_conversion('grams_to_moles', 1, 'k', 18.015)
```
