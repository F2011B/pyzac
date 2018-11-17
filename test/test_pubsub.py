from pyzac import pyzac_decorator
from pyzac import started_processes
from time import sleep


def test_decorators():
    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return 20

    @pyzac_decorator(sub_addr="tcp://localhost:2000")
    def subscriber(result):
        assert result == 20

    publisher()
    subscriber()
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
    test_state()
