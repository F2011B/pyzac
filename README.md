# pyzac python-zero-mq-actor
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Basic Concept
 pyzac uses zeromq to create a mesho of interconnected actors.
 Those actors are created by decorating a function with a pyzac decorator.
 There exist three cases of actors:
 1. The function does not contain any input parameters. Therefore the 
    decorated function only publishes its returned values by the decorator 
    to a specified address.
 2. The function contains parameters but does not return any values.
    In that case the applied decorator only receives mesages and converts them to 
    the function paramters.
 3. The function returns values and contains parameters. 
    In that case the applied decorator receives 
 
 This decorator is used to license to another actor or in case the function 
 does not have any parameters it is used to publish the function results.
 
 
  
