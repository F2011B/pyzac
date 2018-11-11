import pyzac


def test_content():
    assert "pyzac_decorator" in dir(pyzac)
    assert "started_processes" in dir(pyzac)
    assert not ("_wrap_pyzmq" in dir(pyzac))
