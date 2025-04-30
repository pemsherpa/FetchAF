import unittest
import os
import sys

if __name__ == '__main__':
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the base directory to the Python path
    sys.path.insert(0, base_dir)
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with non-zero code if there were failures
    sys.exit(not result.wasSuccessful()) 