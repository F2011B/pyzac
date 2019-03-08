.. pyzac documentation master file, created by
   sphinx-quickstart on Fri Mar  8 20:45:14 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyzac's documentation!
=================================
pyzac is the realisation of an function related actor model
using zmq for message passing.
It was inspired by elixir and erlang's actor model.

Basic Concept
-------------
pyzac uses zeromq to create a mesho of interconnected actors. Those
actors are created by decorating a function with a pyzac decorator.
There exist three cases of actors: 1. The function does not contain any
input parameters. Therefore the decorated function only publishes its
returned values by the decorator to a specified address. 2. The function
contains parameters but does not return any values. In that case the
applied decorator only receives mesages and converts them to the
function paramters. 3. The function returns values and contains
parameters. In that case the applied decorator receives

This decorator is used to license to another actor or in case the
function does not have any parameters it is used to publish the function
results. The package should be placed at pypi in the near future.


.. toctree::
   :maxdepth: 3
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
