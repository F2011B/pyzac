import zmq
from multiprocessing import Process
import functools
import inspect

started_processes = list()

debuglist = list()

cstatekey = "pyzac_state"


lrsocket = {}

c_def_argvalue = 0


def add_debug_info(debugmessage):
    debuglist.add(debugmessage)


def try_get_default_state(func):
    signature = inspect.signature(func)
    param_dict = {k: v for k, v in signature.parameters.items()}
    if cstatekey in param_dict:
        return True, param_dict[cstatekey].default
    else:
        return False, ""


def create_sub_socket(sub_addr, cntx):
    sock_sub = cntx.socket(zmq.SUB)
    sock_sub.connect(sub_addr)
    sock_sub.setsockopt(zmq.SUBSCRIBE, b"")
    return sock_sub


def extract_func_parameters(input_sockets):
    for param in input_sockets:
        try:
            input_sockets[param].recv_pyobj(flags=zmq.NOBLOCK)
            # check for a message, this will not block
        except zmq.Again as e:

            pass


def _try_receive_arg_from_socket(sub_socket):
    try:
        argvalue = sub_socket.recv_pyobj(flags=zmq.NOBLOCK)
        # check for a message, this will not block
    except zmq.Again as e:
        try:
            argvalue = lrsocket[sub_socket]
        except:
            pass
        pass
    return argvalue


def partial_sub(func, sub_socket, def_arg_value=c_def_argvalue):
    lrsocket[sub_socket] = def_arg_value

    def newfunc(*fargs, **fkeywords):
        argvalue = _try_receive_arg_from_socket(sub_socket)
        return func(argvalue, *fargs, **fkeywords)

    newfunc.func = func
    newfunc.sub_socket = sub_socket
    return newfunc


def _pub_wrapper(func, pub_socket, param_name):
    """
    Pub_wrapper is used to add the zero_mq publish part to the function.
    :param func:
    :param pub_socket: socket which is used for mapping values to parameters
    :param param_name: name of the parameter which is mapped onto the socket
    :return:
    """
    # sock_pub.send_pyobj(func_res)

    # f = functools.partial(, func, pub_addr, sub_addr)
    return


def _new_wrap(func, pub_addr, sub_addr):
    # first add all sub wrappers
    # second wrap func with pub_addr_wrapper
    # then return the new function this is called
    # in a while loop
    return


def _simple_wrap_pyzmq(func, pub_addr="", sub_addr=""):
    def notstring(value):
        return type(value) != str

    # if notstring(pub_addr):
    #    pub_addr = ""

    # if notstring(sub_addr):
    #    pub_addr = ""

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
            print("in while ")
            add_debug_info("sub " + str(func_pars))

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
                print("pub_sub ")
            if only_pub:
                func_res = func()
                print("send data " + str(func_res))
        if pub:
            add_debug_info("pub " + str(func_res))
            sock_pub.send_pyobj(func_res)


def _wrap_pyzmq(func, pub_addr="", sub_addr={}):
    """
    :param func:
    :param pub_addr: all generated results are distributed to that address
    :param sub_addr: dictionary mapping parameters to sockets, key is parameter name value equal to address
    :return:

    """
    context = zmq.Context()
    usestate, state = try_get_default_state(func)

    def notdict(value):
        return type(value) != dict

    if notdict(pub_addr) and notdict(sub_addr):
        _simple_wrap_pyzmq(func, pub_addr, sub_addr)

    func_pars = {}
    if usestate:
        func_pars[cstatekey] = state
    in_sockets = {}
    for sub in sub_addr:
        in_sockets[sub] = create_sub_socket(sub_addr[sub], context)

    pub = not (pub_addr == "")

    if pub:
        sock_pub = context.socket(zmq.PUB)
        sock_pub.bind(pub_addr)

    while True:
        func_pars = extract_func_parameters(in_sockets)
        func_res = None
        if usestate:
            func_pars[cstatekey] = state
            func_res = func(**func_pars)
            state = func_res
        if pub:
            sock_pub.send_pyobj(func_res)


def pyzac_decorator(pub_addr="", sub_addr=""):
    def decorator_pyzeromq(func):
        @functools.wraps(func)
        def wrapper_process(*args, **kwargs):
            # partial is used to generate a function with no parameters
            # from _wrap_pyzmq and the input parameters are fixed to
            # func pub_addr and sub_addr
            f = functools.partial(_wrap_pyzmq, func, pub_addr, sub_addr)
            new_process = Process(target=f)
            new_process.start()
            # next line is used to track the started processes
            started_processes.append(new_process)

        return wrapper_process

    return decorator_pyzeromq
