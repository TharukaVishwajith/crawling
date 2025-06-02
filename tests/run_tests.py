"""
Test Runner for E-Commerce Analytics Pipeline

This script provides a convenient way to run all unit tests or specific test modules.
It includes options for coverage reporting and verbose output.

Usage:
    python tests/run_tests.py                    # Run all tests
    python tests/run_tests.py --module analytics # Run specific module tests
    python tests/run_tests.py --coverage         # Run with coverage
    python tests/run_tests.py --verbose          # Run with verbose output
"""

import unittest
import sys
import argparse
from pathlib import Path
import importlib

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def discover_tests(test_dir="tests", pattern="test_*.py"):
    """Discover and return all test cases."""
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir, pattern=pattern)
    return suite


def run_specific_module_tests(module_name):
    """Run tests for a specific module."""
    test_module_map = {
        'analytics': 'test_analytics_pipeline',
        'data': 'test_data_processor', 
        'report': 'test_report_generator',
        'dashboard': 'test_dashboard_generator',
        'browser': 'test_browser_utils'
    }
    
    if module_name not in test_module_map:
        print(f"Unknown module: {module_name}")
        print(f"Available modules: {', '.join(test_module_map.keys())}")
        return False
    
    test_module_name = test_module_map[module_name]
    
    try:
        # Import the test module
        test_module = importlib.import_module(f"tests.{test_module_name}")
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"Failed to import test module {test_module_name}: {e}")
        return False


def run_all_tests(verbosity=1):
    """Run all discovered tests."""
    suite = discover_tests()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_with_coverage():
    """Run tests with coverage reporting."""
    try:
        import coverage
    except ImportError:
        print("Coverage package not installed. Install with: pip install coverage")
        return False
    
    # Start coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Run tests
    success = run_all_tests(verbosity=2)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\n" + "="*50)
    print("COVERAGE REPORT")
    print("="*50)
    
    # Show coverage report
    cov.report(show_missing=True)
    
    # Generate HTML coverage report
    html_dir = Path("tests/coverage_html")
    html_dir.mkdir(exist_ok=True)
    cov.html_report(directory=str(html_dir))
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    return success


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run unit tests for E-Commerce Analytics Pipeline')
    parser.add_argument('--module', '-m', 
                       choices=['analytics', 'data', 'report', 'dashboard', 'browser'],
                       help='Run tests for specific module only')
    parser.add_argument('--coverage', '-c', action='store_true',
                       help='Run tests with coverage reporting')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose test output')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List available test modules')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available test modules:")
        print("  analytics   - AnalyticsPipeline tests")
        print("  data        - DataProcessor tests")
        print("  report      - ReportGenerator tests")
        print("  dashboard   - DashboardGenerator tests")
        print("  browser     - BrowserManager tests")
        return
    
    print("🧪 E-Commerce Analytics Pipeline - Unit Tests")
    print("=" * 60)
    
    if args.coverage:
        print("Running tests with coverage analysis...")
        success = run_with_coverage()
    elif args.module:
        print(f"Running tests for module: {args.module}")
        success = run_specific_module_tests(args.module)
    else:
        print("Running all tests...")
        verbosity = 2 if args.verbose else 1
        success = run_all_tests(verbosity)
    
    print("\n" + "="*60)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main() 