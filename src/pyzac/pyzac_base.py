import zmq
from multiprocessing import Process
import functools
import inspect

started_processes = list()


def get_pyzac_state(func):
    signature = inspect.signature(func)
    for k, v in signature.parameters.items():
        if k == "pyzac_state":
            return v.default


def try_get_default_state(func):
    funcargs = inspect.getargspec(func).args
    usestate = "pyzac_state" in funcargs
    if usestate:
        return True, get_pyzac_state(func)
    else:
        return False, ""


def _wrap_pyzmq(func, pub_addr="", sub_addr=""):
    nopub = pub_addr == ""
    nosub = sub_addr == ""
    if nopub and nosub:
        return

    context = zmq.Context()

    if not nosub:
        sock_sub = context.socket(zmq.SUB)
        sock_sub.connect(sub_addr)
    if not nopub:
        sock_pub = context.socket(zmq.PUB)
        sock_pub.connect(pub_addr)

    hasstate, state = try_get_default_state(func)
    while True:
        if not nosub:
            func_pars = sock_sub.recv_pyobj()

        if hasstate:
            func_res = func(pyzac_state=state, **func_pars)
            state = func_res
        else:
            func_res = func(**func_pars)

        sock_pub.send_pyobj(func_res)


def pyzac_decorator(pub_addr="", sub_addr=""):
    def decorator_pyzeromq(func):
        @functools.wraps(func)
        def wrapper_process(*args, **kwargs):
            f = functools.partial(_wrap_pyzmq, func, pub_addr, sub_addr)
            new_process = Process(target=f)
            new_process.start()
            started_processes.append(new_process)

        return wrapper_process

    return decorator_pyzeromq
