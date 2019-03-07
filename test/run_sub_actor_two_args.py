from pyzac import *


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2000", "tcp://localhost:2001"])
def subscriber(result, second):
    print(result * second)


@pyzac_decorator(
    pos_sub_addr=["tcp://localhost:2000"],
    key_sub_addr={"second": "tcp://localhost:2001"},
)
def subscribertwo(result, second=10):
    print(result * second)


# subscriber()
subscribertwo()
