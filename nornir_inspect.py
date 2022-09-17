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
    > This function takes an `AggregatedResult` object and prints a tree of the object's attributes and
    values.

    Args:
      nr_result (AggregatedResult): AggregatedResult
      vals (bool): bool = False. Defaults to False
      headings (bool): bool = False. Defaults to False
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

    return tree  # noqa: T001


def add_to_tree(branch: Any, nr_result: Union[AggregatedResult, MultiResult, Result]):
    """
    It takes a branch and a root object, and adds the root object's attributes to the branch.

    Args:
      branch (Any): Any
      nr_result (Union[AggregatedResult, MultiResult, Result]): The object to be printed.
    """
    for k, v in get_object_attributes(nr_result).items():
        branch.add(highlighter(f"{k} = {v}"))


def get_object_attributes(obj: Any) -> dict:
    """
    It returns a dictionary of all the attributes of an object, excluding private and special methods,
    builtin functions, and methods

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


def inspect_nornir(
    nr_result: AggregatedResult, vals: bool = True, headings: bool = True
):
    print(create_object_attribute_tree(nr_result, vals, headings))
