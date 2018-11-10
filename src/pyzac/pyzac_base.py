import zmq
from multiprocessing import Process
import functools

started_processes = list()


def _wrap_pyzmq(func, pub_addr, sub_addr):
    context = zmq.Context()
    sock_sub = context.socket(zmq.SUB)
    sock_sub.connect(sub_addr)
    sock_pub = context.socket(zmq.PUB)
    sock_pub.connect(pub_addr)
    while True:
        func_pars = sock_sub.recv_pyobj()
        func_res = func(**func_pars)
        sock_pub.send_pyobj(func_res)


def pyzac_decorator(pub_addr, sub_addr):
    def decorator_pyzeromq(func):
        @functools.wraps(func)
        def wrapper_process(*args, **kwargs):
            f = functools.partial(_wrap_pyzmq, func, pub_addr, sub_addr)
            new_process = Process(target=f)
            new_process.start()
            started_processes.append(new_process)

        return wrapper_process

    return decorator_pyzeromq
