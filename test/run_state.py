from pyzac import *


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
def publisher():
    return 20


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000"], pyzac_state={"second": 10})
def subscriber(result, second):
    print(result * second)
    if second > 10000:
        return 2
    return result * second


publisher()
subscriber()
