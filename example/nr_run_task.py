#!/usr/bin/env python

from nornir import InitNornir
from nornir.core.task import Result, Task

from nornir_inspect import nornir_inspect

nr = InitNornir(
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


def task_1(task: Task, number: int) -> Result:
    """
    "Given a task and a number, return a result with the number incremented by one."

    The function takes two arguments:

    - `task`: A `Task` object.
    - `number`: An integer

    Args:
      task (Task): Task
      number (int): int - This is the parameter that will be passed to the task.

    Returns:
      A Result object with the host and result.
    """
    n = number + 1
    return Result(host=task.host, result=f"{n}")


result = nr.run(task=task_1, number=1)

if __name__ == "__main__":
    nornir_inspect(nr_result=result)
