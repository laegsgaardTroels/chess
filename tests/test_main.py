import os
import subprocess


def test_main():
    """Used to test the __main__.py script."""
    subprocess.run([os.environ['PYTHON_INTERPRETER'], '-m', 'chess'])
