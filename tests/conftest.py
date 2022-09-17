import pytest
from nornir import InitNornir
from nornir.core.task import Result


@pytest.fixture(scope="session")
def dummy_class():
    class DummyClass:
        def __init__(self, x, y):
            self.x = x
            self._y = y

        def __str__(self):
            pass

        def _a(self):
            pass

        def b(self):
            pass

    return DummyClass(x=1, y=2)


@pytest.fixture(scope="session")
def nr_init():
    return InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 10,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {"host_file": "tests/hosts.yaml"},
        },
        logging={"enabled": False},
    )


@pytest.fixture(scope="session")
def nr_result(nr_init):
    def task_1(task, number):
        n = number + 1
        return Result(host=task.host, result=f"{n}")

    return nr_init.run(task=task_1, number=1)
