import pytest
from nornir import InitNornir
from nornir.core.task import Result
import re

@pytest.fixture(scope="session")
def dummy_class():
    """Fixture for a dummy class for extracting attributes from."""

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
    """Fixture for Nornir setup."""
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
    """Fixture for running a Nornir task to create a Nornir result tree."""

    def task_1(task, number):
        n = number + 1
        return Result(host=task.host, result=f"{n}")

    return nr_init.run(task=task_1, number=1)


@pytest.fixture(scope="session")
def expected_inspect_output():
    return """<class 'nornir.core.task.AggregatedResult'>
├── failed = False
├── failed_hosts = {}
├── name = task_1
├── <class 'nornir.core.task.MultiResult'> ['node1']
│   ├── failed = False
│   ├── failed_hosts = {}
│   ├── name = task_1
│   └── <class 'nornir.core.task.Result'> [0]
│       ├── changed = False
│       ├── diff = ''
│       ├── exception = None
│       ├── failed = False
│       ├── host = node1
│       ├── name = task_1
│       ├── result = 2
│       ├── severity_level = 20
│       ├── stderr = None
│       └── stdout = None
├── <class 'nornir.core.task.MultiResult'> ['node2']
│   ├── failed = False
│   ├── failed_hosts = {}
│   ├── name = task_1
│   └── <class 'nornir.core.task.Result'> [0]
│       ├── changed = False
│       ├── diff = ''
│       ├── exception = None
│       ├── failed = False
│       ├── host = node2
│       ├── name = task_1
│       ├── result = 2
│       ├── severity_level = 20
│       ├── stderr = None
│       └── stdout = None
└── <class 'nornir.core.task.MultiResult'> ['node3']
    ├── failed = False
    ├── failed_hosts = {}
    ├── name = task_1
    └── <class 'nornir.core.task.Result'> [0]
        ├── changed = False
        ├── diff = ''
        ├── exception = None
        ├── failed = False
        ├── host = node3
        ├── name = task_1
        ├── result = 2
        ├── severity_level = 20
        ├── stderr = None
        └── stdout = None
"""
