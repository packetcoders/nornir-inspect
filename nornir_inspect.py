import types
from typing import Any, Union

from nornir.core.task import AggregatedResult, MultiResult, Result
from rich import print
from rich.highlighter import ReprHighlighter
from rich.pretty import Pretty
from rich.tree import Tree

highlighter = ReprHighlighter()


def create_object_attribute_tree(
    nr_result: AggregatedResult,
    vals: bool = True,
    headings: bool = True,
) -> Tree:
    """
    Take an `AggregatedResult` object and prints a tree of the object's attributes and
    values.

    Args:
      nr_result (AggregatedResult): AggregatedResult
      vals (bool): bool = True. Defaults to False
      headings (bool): bool = True. Defaults to False
    """
    # AggregatedResult
    tree = Tree(Pretty(type(nr_result)))

    if vals:
        add_to_tree(tree, nr_result)

    # MultiResults
    for k, v in nr_result.items():
        if headings:
            branch_1 = tree.add(highlighter(f"{type(v)} ['{k}']"))
        else:
            branch_1 = tree.add(highlighter(f"{type(v)}"))

        if vals:
            add_to_tree(branch_1, nr_result)

        # Results
        for index, item in enumerate(v):
            if headings:
                branch_3 = branch_1.add(highlighter(f"{(type(item))} [{index}]"))
            else:
                branch_3 = branch_1.add(highlighter(f"{type(item)}"))

            if vals:
                add_to_tree(branch_3, item)

    return tree


def add_to_tree(branch: Any, nr_result: Union[AggregatedResult, MultiResult, Result]):
    """
    Take a branch and a root object, and adds the root object's attributes to the branch.

    Args:
      branch (Any): Any
      nr_result (Union[AggregatedResult, MultiResult, Result]): The object to be printed.
    """
    for k, v in get_object_attributes(nr_result).items():
        branch.add(highlighter(f"{k} = {v}"))


def get_object_attributes(obj: Any) -> dict:
    """
    Return a dictionary of all the attributes of an object, excluding private and special methods
    builtin functions, and methods.

    Args:
      obj (Any): Any

    Returns:
      A dictionary of the attributes of the object.
    """
    dir(obj).sort()

    obj_attr = dict()

    for a in dir(obj):
        # exclude private and special methods
        if a.startswith("_") or a.startswith("__"):
            pass
        # exclude builtin functions
        elif isinstance(getattr(obj, a), types.BuiltinFunctionType):
            pass
        # exclude methods
        elif isinstance(getattr(obj, a), types.MethodType):
            pass
        else:
            obj_attr.update({a: getattr(obj, a)})

    return obj_attr


def nornir_inspect(
    nr_result: AggregatedResult, vals: bool = True, headings: bool = True
):
    """
    Take a Nornir result object and prints out a tree of the attributes and methods of the object.

    Args:
      nr_result (AggregatedResult): The Nornir result object to inspect
      vals (bool): If True, the values of the attributes will be printed. Defaults to True
      headings (bool): If True, the first line of the output will be a list of the headings. Defaults to
    True
    """
    print(create_object_attribute_tree(nr_result, vals, headings))  # noqa: T001
