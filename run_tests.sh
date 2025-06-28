#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

# Run the test suite
pytest test_pink_morsel_visualizer.py

# Capture pytest exit code
TEST_EXIT_CODE=$?

# Exit with code 0 if all tests passed, else 1
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed!"
  exit 0
else
  echo "❌ Some tests failed."
  exit 1
fi
