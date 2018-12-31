import zmq
from multiprocessing import Process
import functools
import inspect

started_processes = list()

debuglist = list()

cstatekey = "pyzac_state"


lrsocket = {}

c_def_argvalue = 0
c_def_blank = ""


def add_debug_info(debugmessage):
    debuglist.append(debugmessage)


def create_sub_socket(sub_addr, cntx):
    sock_sub = cntx.socket(zmq.SUB)
    sock_sub.connect(sub_addr)
    sock_sub.setsockopt_string(zmq.SUBSCRIBE, "")
    # sock_sub.setsockopt(zmq.SUBSCRIBE, b"")
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


def partial_sub(func, sub_socket, keyargname=c_def_blank, def_arg_value=c_def_argvalue):
    lrsocket[sub_socket] = def_arg_value

    def newfunc(*fargs, **fkeywords):
        argvalue = _try_receive_arg_from_socket(sub_socket)
        add_debug_info(argvalue)
        if keyargname != c_def_blank:
            newkeywords = {keyargname: argvalue}
            newkeywords.update(fkeywords)
            return func(*fargs, **newkeywords)
        else:
            return func(argvalue, *fargs, **fkeywords)

    newfunc.func = func
    newfunc.sub_socket = sub_socket
    return newfunc


def _pub_wrapper(func, pub_socket):
    """
    Pub_wrapper is used to add the zero_mq publish part to the function.
    :param func:
    :param pub_socket: socket which is used for mapping values to parameters
    :param param_name: name of the parameter which is mapped onto the socket
    :return:
    """

    def newfunc():
        try:
            func_res = func()
            print(func_res)
            print(pub_socket)
            # print(pub_socket.get(zmq.ZMQ_LAST_ENDPOINT))
            pub_socket.send_pyobj(func_res)
        except:
            print("exception")
            Exception("Cannot send pub")
            pass
        return func_res

    newfunc.func = func
    newfunc.pub_socket = pub_socket
    return newfunc


def get_pos_and_key_names(func):
    params = inspect.signature(func).parameters
    pos_arg_names = [k for k in params if params[k].default == inspect._empty]
    key_arg_names = [k for k in params if params[k].default != inspect._empty]
    return pos_arg_names, key_arg_names


def _wrap_pyzmq(func, pub_addr="", pos_sub_addr=[], key_sub_addr={}):
    """
    :param func:
    :param pub_addr: all generated results are distributed to that address
    :param sub_addr: dictionary mapping parameters to sockets, key is parameter name value equal to address
    :return:

    """
    context = zmq.Context()

    posnames, keynames = get_pos_and_key_names(func)

    _check_mapping_of_args(key_sub_addr, keynames, pos_sub_addr, posnames)
    in_sockets = _create_socket_mapping(context, key_sub_addr, pos_sub_addr, posnames)

    pub = not (pub_addr == "")

    newfunc = _create_partial_func(func, in_sockets, key_sub_addr, posnames)

    if pub:
        newfunc = create_pub_func(context, newfunc, pub_addr)

    while True:
        newfunc()


def create_pub_func(context, newfunc, pub_addr):
    sock_pub = context.socket(zmq.PUB)
    sock_pub.bind(pub_addr)
    newfunc = _pub_wrapper(newfunc, sock_pub)
    return newfunc


def _create_partial_func(func, in_sockets, key_sub_addr, posnames):
    newfunc = func
    for sub in posnames:
        newfunc = partial_sub(newfunc, in_sockets[sub])
    for key in key_sub_addr:
        newfunc = partial_sub(newfunc, in_sockets[key], keyargname=key)
    return newfunc


def _create_socket_mapping(context, key_sub_addr, pos_sub_addr, posnames):
    in_sockets = {}
    counter = 0
    for posname in posnames:
        in_sockets[posname] = create_sub_socket(pos_sub_addr[counter], context)
        counter += 1
    for sub in key_sub_addr:
        in_sockets[sub] = create_sub_socket(key_sub_addr[sub], context)
    return in_sockets


def _check_mapping_of_args(key_sub_addr, keynames, pos_sub_addr, posnames):
    not_key_args_mapped = not len(key_sub_addr.keys()) == len(keynames)
    not_pos_args_mapped = not len(posnames) == len(pos_sub_addr)
    if not_key_args_mapped or not_pos_args_mapped:
        if not_key_args_mapped:
            raise Exception("key args not mapped")
        if not_pos_args_mapped:
            raise Exception("pos args not mapped")


def pyzac_decorator(pub_addr="", pos_sub_addr=[], key_sub_addr={}):
    def decorator_pyzeromq(func):
        @functools.wraps(func)
        def wrapper_process(*args, **kwargs):
            # partial is used to generate a function with no parameters
            # from _wrap_pyzmq and the input parameters are fixed to
            # func pub_addr and sub_addr
            f = functools.partial(
                _wrap_pyzmq, func, pub_addr, pos_sub_addr, key_sub_addr
            )
            new_process = Process(target=f)
            new_process.start()
            # next line is used to track the started processes
            started_processes.append(new_process)

        return wrapper_process

    return decorator_pyzeromq
