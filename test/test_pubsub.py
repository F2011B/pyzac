from pyzac import pyzac_decorator
from pyzac import started_processes
from pyzac import assertlist
from pyzac import debuglist
from pyzac import partial_sub
from pyzac import add_debug_info
from pyzac import create_pub_func
from pyzac import create_sub_socket
from multiprocessing import Process
import zmq
from time import sleep


def test_partial_sub():
    class mocksocket:
        def recv_pyobj(self, flags="notused"):
            return 20

    a = mocksocket()

    def atest(myparam, myparamtwo):
        return myparam * myparamtwo

    testval = partial_sub(atest, a)(1)
    assert testval == 20


def test_partial_sub_addition():
    counter = 20

    class mocksocket:
        def recv_pyobj(self, flags="notused"):
            nonlocal counter
            counter = counter + 1
            return counter

    a = mocksocket()

    def atest(myparam, myparamtwo):
        return myparam * myparamtwo

    myfunc = partial_sub(partial_sub(atest, a), a)
    testval = myfunc()
    assert testval == 21 * 22
    testval = myfunc()
    assert testval == 23 * 24
    testval = myfunc()
    assert testval == 25 * 26


def test_zmq():
    recfile = open("test.txt", "w")

    def pub_func():
        context = zmq.Context()
        #       socket = context.socket(zmq.PUB)
        #      socket.bind("tcp://127.0.0.1:2000")

        # Allow clients to connect before sending data
        #     sleep(1)
        #    socket.send_pyobj(20)

        def atest():
            sleep(1)
            return 20

        context = zmq.Context()
        newfunc = create_pub_func(context, atest, "tcp://127.0.0.1:2000")
        newfunc()

    def sub_func():
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        # We can connect to several endpoints if we desire, and receive from all.
        socket.connect("tcp://127.0.0.1:2000")

        # We must declare the socket as of type SUBSCRIBER, and pass a prefix filter.
        # Here, the filter is the empty string, wich means we receive all messages.
        # We may subscribe to several filters, thus receiving from all.
        socket.setsockopt(zmq.SUBSCRIBE, b"")

        message = socket.recv_pyobj()
        print(message)

    print("start_new_func")
    pub_process = Process(target=pub_func)
    pub_process.start()
    print("start_sub_func")
    rec_process = Process(target=sub_func)
    rec_process.start()
    sleep(2)
    pub_process.terminate()
    pub_process.join()
    rec_process.terminate()
    rec_process.join()


def test_partial_pub_zmq():
    def atest():
        return 20

    def run_newfunc():
        context = zmq.Context()
        newfunc = create_pub_func(context, atest, "tcp://127.0.0.1:5000")
        while True:
            assert 20 == newfunc()

    def run_receive():
        subcontext = zmq.Context()
        sub_socket = create_sub_socket("tcp://127.0.0.1:5000", subcontext)
        while True:
            testobj = sub_socket.recv_pyobj()
            print(testobj)
            assert testobj == 20

    pub_process = Process(target=run_newfunc)
    pub_process.start()
    sleep(1)
    rec_process = Process(target=run_receive)
    rec_process.start()
    sleep(1)
    pub_process.terminate()
    pub_process.join()
    rec_process.terminate()
    rec_process.join()


def test_partial_pub_sub_zmq():
    def atest():
        return 20

    def get_test(avalue):
        assert (avalue == 20) or (avalue == 0)

    def run_newfunc():
        context = zmq.Context()
        newfunc = create_pub_func(context, atest, "tcp://127.0.0.1:5000")
        while True:
            assert 20 == newfunc()

    def run_receive():
        subcontext = zmq.Context()
        sub_socket = create_sub_socket("tcp://127.0.0.1:5000", subcontext)

        recfunc = partial_sub(get_test, sub_socket)
        while True:
            recfunc()

    pub_process = Process(target=run_newfunc)
    pub_process.start()
    sleep(1)
    rec_process = Process(target=run_receive)
    rec_process.start()
    sleep(1)
    pub_process.terminate()
    pub_process.join()
    rec_process.terminate()
    rec_process.join()


# assert len(reclist) > 0


def test_partial_sub_addition_keyarg():
    """
    This function is used to test the keyargument
    handling in the partial_sub function.
    """
    startcounter = 20
    counter = startcounter

    class mocksocket:
        def recv_pyobj(self, flags="notused"):
            nonlocal counter
            counter = counter + 1
            return counter

    a = mocksocket()

    def atest(myparam, myparamtwo=0):
        return myparam * myparamtwo

    myfunc = partial_sub(partial_sub(atest, a), a, keyargname="myparamtwo")
    # the myfunc has to be called multiple times to simulate multiple receive operations
    # for the encapsulated sockets
    testval = myfunc()
    assert testval == (startcounter + 1) * (startcounter + 2)
    testval = myfunc()
    assert testval == (startcounter + 3) * (startcounter + 4)
    testval = myfunc()
    assert testval == (startcounter + 5) * (startcounter + 6)


def test_decorators():
    @pyzac_decorator(pub_addr="tcp://localhost:2000")
    def publisher():
        add_debug_info("in publisher")
        return 20

    @pyzac_decorator(pos_sub_addr=["tcp://localhost:2000"])
    def subscriber(result):
        add_debug_info("in subscriber")
        print(result)
        # assert result == 20

    publisher()
    sleep(1)
    subscriber()
    sleep(1)

    # assert len(debuglist) != 0
    # for dinfo in debuglist:
    #     print(dinfo)

    # assert len(assertlist) != 0
    # for dinfo in assertlist:
    #    print(dinfo)

    for p in started_processes:
        p.terminate()
        p.join()


#
# def test_paramsubmap_decorators():
#     @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
#     def publisher():
#         # print("hello")
#         return 20
#
#     @pyzac_decorator(pos_sub_addr=["tcp://localhost:2000"])
#     def subscriber(result):
#         print(result)
#         assert result == 20
#
#     publisher()
#     sleep(1)
#     subscriber()
#
#     assert len(assertlist) != 0
#     for dinfo in assertlist:
#         print(dinfo)
#
#     for dinfo in debuglist:
#         print(dinfo)
#
#     for p in started_processes:
#         p.terminate()
#         p.join()

#
# def test_decorator_mesh():
#     @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
#     def publisher():
#         return 20
#
#     @pyzac_decorator(
#         pos_sub_addr="tcp://localhost:2000", pub_addr="tcp://127.0.0.1:2001"
#     )
#     def filter(result):
#         assert result == 30
#         return 40
#
#     @pyzac_decorator(pos_sub_addr="tcp://localhost:2001")
#     def end_point(result):
#         assert result == 40
#
#     publisher()
#     sleep(1)
#     filter()
#     sleep(1)
#     end_point()
#     sleep(1)
#
#     assert len(assertlist) != 0
#     for dinfo in assertlist:
#         print(dinfo)
#
#     for p in started_processes:
#         p.terminate()
#         p.join()


def test_state():
    count = 0
    std_pub_val = 20

    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return std_pub_val

    @pyzac_decorator(pos_sub_addr="tcp://localhost:2000")
    def subscriber(result, pyzac_state=0):
        nonlocal count
        if count == 1:
            assert pyzac_state > 0
            assert pyzac_state == std_pub_val
        if count == 2:
            assert pyzac_state == 2 * std_pub_val
        count = count + 1
        print(count)
        return result + pyzac_state

    publisher()
    sub = subscriber
    sub()
    sleep(1)
    for p in started_processes:
        p.terminate()
        p.join()
        print("Processes stoped")


if __name__ == "__main__":
    test_decorator_mesh()
    test_state()
