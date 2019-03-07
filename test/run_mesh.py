from pyzac import *


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
def publisher():
    return 20


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2001")
def publishertwo():
    return 3


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000", "tcp://localhost:2001"])
def subscriber(result, second):
    print(result * second)


@pyzac_decorator(
    pos_sub_addr=["tcp://localhost:2000"],
    key_sub_addr={"second": "tcp://localhost:2001"},
)
def subscribertwo(result, second=10):
    print(result * second)


publisher()
publishertwo()
subscribertwo()
