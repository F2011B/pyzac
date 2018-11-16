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


if __name__ == "__main__":

    test_decorators()
    print("Processes stoped")
