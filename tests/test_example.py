import subprocess


def test_nornir_inspect_example(expected_inspect_output):
    """Test the Nornir inspect output"""
    script_result = subprocess.run(
        "example/nr_run_task.py", capture_output=True, text=True
    )
    assert script_result.returncode == 0
    # Add end of line characters to prevent VSCode auto-formatting line.
    assert (
        script_result.stdout.replace("diff = ", "diff = ''") == expected_inspect_output
    )
