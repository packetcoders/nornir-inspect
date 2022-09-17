import pytest
from nornir import InitNornir
from nornir.core.task import Result

from nornir_inspect import create_object_attribute_tree, get_object_attributes


def test_get_object_attributes(dummy_class):
    obj_attr = get_object_attributes(dummy_class)
    assert list(obj_attr.keys()) == ["x"]
    assert list(obj_attr.values()) == [1]


def test_create_object_attribute_tree(nr_result):
    tree = create_object_attribute_tree(nr_result)
    assert len(tree.children) == 6
    assert tree.__class__.__name__ == "Tree"

def test_create_object_attribute_tree_without_values_headings(nr_result):
    tree = create_object_attribute_tree(nr_result, vals=False, headings=False)
    assert len(tree.children) == 3
    assert tree.__class__.__name__ == "Tree"

@pytest.mark.parametrize(
    ("index", "children", "label"),
    [
        (0, 0, "failed = False"),
        (1, 0, "failed_hosts = {}"),
        (2, 0, "name = task_1"),
        (3, 4, "<class 'nornir.core.task.MultiResult'> ['node1']"),
        (4, 4, "<class 'nornir.core.task.MultiResult'> ['node2']"),
        (5, 4, "<class 'nornir.core.task.MultiResult'> ['node3']"),
    ],
)
def test_create_object_attribute_tree_level_1(index, children, label, nr_result):
    tree = create_object_attribute_tree(nr_result)
    assert tree.children[index].label.plain == label
    assert len(tree.children[index].children) == children
    assert tree.children[index].__class__.__name__ == "Tree"


@pytest.mark.parametrize(
    ("index_1", "index_2", "children", "label"),
    [
        (3, 0, 0, "failed = False"),
        (3, 1, 0, "failed_hosts = {}"),
        (3, 2, 0, "name = task_1"),
        (3, 3, 10, "<class 'nornir.core.task.Result'> [0]"),
        (4, 0, 0, "failed = False"),
        (4, 1, 0, "failed_hosts = {}"),
        (4, 2, 0, "name = task_1"),
        (4, 3, 10, "<class 'nornir.core.task.Result'> [0]"),
        (5, 0, 0, "failed = False"),
        (5, 1, 0, "failed_hosts = {}"),
        (5, 2, 0, "name = task_1"),
        (5, 3, 10, "<class 'nornir.core.task.Result'> [0]"),
    ],
)
def test_create_object_attribute_tree_level_2(
    index_1, index_2, children, label, nr_result
):
    tree = create_object_attribute_tree(nr_result)
    assert tree.children[index_1].children[index_2].label.plain == label
    assert len(tree.children[index_1].children[index_2].children) == children
    assert tree.children[index_1].__class__.__name__ == "Tree"


