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
    pub = not (pub_addr == "")
    sub = not (sub_addr == "")
    only_pub = pub and (not sub)
    only_sub = sub and (not pub)
    pub_sub = sub and pub

    context = zmq.Context()

    if sub:
        sock_sub = context.socket(zmq.SUB)
        sock_sub.connect(sub_addr)
        sock_sub.setsockopt(zmq.SUBSCRIBE, b"")
    if pub:
        sock_pub = context.socket(zmq.PUB)
        sock_pub.bind(pub_addr)

    usestate, state = try_get_default_state(func)
    while True:
        func_res = ""
        func_pars = []
        if sub:
            func_pars = sock_sub.recv_pyobj()

        if usestate:
            if only_sub:
                func_res = func(func_pars, pyzac_state=state)
            if pub_sub:
                func_res = func(func_pars, pyzac_state=state)
            if only_pub:
                func_res = func(pyzac_state=state)
            state = func_res
        else:
            if only_sub:
                func_res = func(func_pars)
            if pub_sub:
                func_res = func(func_pars)
            if only_pub:
                func_res = func()
                # print("send data " + str(func_res))
        if pub:
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
