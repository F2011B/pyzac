from pyzac import *


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000"])
def subscriber(result):
    add_debug_info("in subscriber")
    print(result)


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2001"])
def subscriber_two(result):
    add_debug_info("in subscriber")
    print(result)


try:
    subscriber()
    subscriber_two()
except:
    print(debuglist)
