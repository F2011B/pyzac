from pyzac import *


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
def publisher():
    return 20


@pyzac_decorator(pub_addr="tcp://127.0.0.1:2001")
def publishertwo():
    return 3


publisher()
publishertwo()
