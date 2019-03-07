from pyzac import *


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000", "tcp://localhost:2001"])
def subscriber(result, second):
    print(result * second)


subscriber()
