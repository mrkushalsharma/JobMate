# run_tests.py
import pytest
import sys

if __name__ == "__main__":
    # Include coverage options directly in the command
    sys.exit(pytest.main(["-v",  "tests/"]))