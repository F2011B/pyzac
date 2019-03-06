from pyzac import *


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000"])
def subscriber(result):
    add_debug_info("in subscriber")
    print(result)


subscriber()
