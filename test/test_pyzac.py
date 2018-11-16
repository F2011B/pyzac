from pyzac import pyzac_decorator
from pyzac import started_processes


def test_content():
    assert "pyzac_decorator" in dir(pyzac)
    assert "started_processes" in dir(pyzac)
    assert not ("_wrap_pyzmq" in dir(pyzac))


def test_decorators():
    @pyzac_decorator(pub_addr="tcp://127.0.0.1:2000")
    def publisher():
        return 20

    @pyzac_decorator(sub_addr="tcp://localhost:2000")
    def subscriber(result):
        print(result)

    publisher()
    subscriber()


if __name__ == "__main__":
    from time import sleep

    test_decorators()
    sleep(1)
    for p in started_processes:
        p.terminate()
        p.join()
    print("Processes stoped")
