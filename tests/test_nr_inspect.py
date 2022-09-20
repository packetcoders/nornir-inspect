import pytest

from nornir_inspect import (
    create_object_attribute_tree,
    get_object_attributes,
    nornir_inspect,
)


def test_get_object_attributes(dummy_class):
    """Test creating a dict of object attributes."""
    obj_attr = get_object_attributes(dummy_class)
    assert list(obj_attr.keys()) == ["x"]
    assert list(obj_attr.values()) == [1]


def test_create_object_attribute_tree(nr_result):
    """Test the tree object."""
    tree = create_object_attribute_tree(nr_result)

    assert len(tree.children) == 6
    assert tree.__class__.__name__ == "Tree"


def test_create_object_attribute_tree_without_values_headings(nr_result):
    """Test the tree object without the values and headings."""
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
    """Test the 1st level of the tree object."""
    tree = create_object_attribute_tree(nr_result)

    assert tree.children[index].label.plain == label
    assert len(tree.children[index].children) == children
    assert tree.children[index].__class__.__name__ == "Tree"


@pytest.mark.parametrize("index_1", [3, 4, 5])
@pytest.mark.parametrize(
    ("index_2", "children", "label"),
    [
        (0, 0, "failed = False"),
        (1, 0, "failed_hosts = {}"),
        (2, 0, "name = task_1"),
        (3, 10, "<class 'nornir.core.task.Result'> [0]"),
    ],
)
def test_create_object_attribute_tree_level_2(
    index_1, index_2, children, label, nr_result
):
    """Test the 2nd level of the tree object."""
    tree = create_object_attribute_tree(nr_result)

    assert tree.children[index_1].children[index_2].label.plain == label
    assert len(tree.children[index_1].children[index_2].children) == children
    assert tree.children[index_1].__class__.__name__ == "Tree"


def test_nornir_inspect_output(nr_result, expected_inspect_output, capsys):
    """Test the Nornir inspect output"""
    nornir_inspect(nr_result)
    captured_output = capsys.readouterr().out

    assert isinstance(captured_output, str)
    assert len(str(captured_output).splitlines()) == 49
    # Add end of line characters to prevent VSCode auto-formatting line.
    assert captured_output.replace("diff = ", "diff = ''") == expected_inspect_output
