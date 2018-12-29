from pyzac import pyzac_decorator
from pyzac import started_processes
from pyzac import debuglist
from pyzac import partial_sub
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


def test_decorators():
    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return 20

    @pyzac_decorator(sub_addr="tcp://localhost:2000")
    def subscriber(result):
        assert result == 20

    publisher()
    subscriber()

    for dinfo in debuglist:
        print(dinfo)

    for p in started_processes:
        p.terminate()
        p.join()


def test_paramsubmap_decorators():
    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        print("hello")
        return 20

    @pyzac_decorator(sub_addr={"result": "tcp://localhost:2000"})
    def subscriber(result):
        print("Hello")
        assert result == 20

    publisher()
    sleep(1)
    subscriber()

    for dinfo in debuglist:
        print(dinfo)

    for p in started_processes:
        p.terminate()
        p.join()


def test_decorator_mesh():
    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return 20

    @pyzac_decorator(sub_addr="tcp://localhost:2000", pub_addr="tcp://127.0.0.1:2001")
    def filter(result):
        assert result == 20
        return 40

    @pyzac_decorator(sub_addr="tcp://localhost:2001")
    def end_point(result):
        assert result == 40

    publisher()
    sleep(1)
    filter()
    sleep(1)
    end_point()
    sleep(1)
    for p in started_processes:
        p.terminate()
        p.join()


def test_state():
    count = 0
    std_pub_val = 20

    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return std_pub_val

    @pyzac_decorator(sub_addr="tcp://localhost:2000")
    def subscriber(result, pyzac_state=0):
        nonlocal count
        if count == 1:
            assert pyzac_state > 0
            assert pyzac_state == std_pub_val
        if count == 2:
            assert pyzac_state == 2 * std_pub_val
        count = count + 1
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
