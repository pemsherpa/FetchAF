# Standard library imports
import os
import sys
import unittest

# Third-party imports
import coverage

def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    # Start coverage measurement
    cov = coverage.Coverage(
        source=['app.py'],
        omit=['tests/*', '*/__pycache__/*']
    )
    cov.start()

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage measurement and generate report
    cov.stop()
    cov.save()
    
    print('\nCoverage Summary:')
    cov.report()
    
    # Generate HTML coverage report
    cov.html_report(directory='htmlcov')
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1) 