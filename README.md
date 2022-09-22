# Nornir Inspect
Nornir inspect is a Python library for inspecting the Nornir result structure.

## Install

```
pip install nornir-inspect

or

poetry add nornir-inspect
```

## Usage

<details>
  <summary>Nornir setup steps</summary>

```python
from nornir import InitNornir
from nornir.core.task import Result, Task

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
     n = number + 1
     return Result(host=task.host, result=f"{n}")


result = nr.run(task=task_1, number=1)
```
</details>


```python
from nornir_inspect import nornir_inspect

nornir_inspect(result)

<class 'nornir.core.task.AggregatedResult'>
├── failed = False
├── failed_hosts = {}
├── name = task_1
├── <class 'nornir.core.task.MultiResult'> ['node1']
│   ├── failed = False
│   ├── failed_hosts = {}
│   ├── name = task_1
│   └── <class 'nornir.core.task.Result'> [0]
│       ├── changed = False
│       ├── diff =
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
│       ├── diff =
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
        ├── diff =
        ├── exception = None
        ├── failed = False
        ├── host = node3
        ├── name = task_1
        ├── result = 2
        ├── severity_level = 20
        ├── stderr = None
        └── stdout = None
```

### Addtional Options
* `vals` (bool): If True, the values of the attributes will be printed. Defaults to True.
* `headings`(bool): If True, the first line of the output will include the objects key name or list postion. Defaults to True.


