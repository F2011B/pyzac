pyzac python-zero-mq-actor
==========================

|Doc status| |Build Status| |Codacy Badge| |Code style: black|

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

.. |Doc status| image:: https://readthedocs.org/projects/pyzac/badge/?version=latest
   :target: https://pyzac.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/F2011B/pyzac.svg?branch=master
   :target: https://travis-ci.org/F2011B/pyzac
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/313cc391a41040cab9d8119fbbcc483a
   :target: https://app.codacy.com/app/F2011B/pyzac?utm_source=github.com&utm_medium=referral&utm_content=F2011B/pyzac&utm_campaign=Badge_Grade_Dashboard
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black