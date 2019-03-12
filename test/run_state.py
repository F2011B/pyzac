from pyzac import *
import time


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
def publisher():
    time.sleep(20)
    return 2


@pyzac_decorator(
    pub_addr="tcp://127.0.0.1:2001",
    pos_sub_addr=["tcp://localhost:2000"],
    pyzac_state={"second": 10},
)
def subscriber(result, pyzac_state):
    # print(result * pyzac_state["second"])
    if pyzac_state["second"] > 100000:
        pyzac_state["second"] = 2
        return 2
    pyzac_state["second"] = result * pyzac_state["second"]
    return None  # result * pyzac_state["second"]


@pyzac_decorator(pos_sub_addr=["tcp://localhost:2001"])
def subscribertwo(result):
    print(result)


publisher()
subscriber()
subscribertwo()
