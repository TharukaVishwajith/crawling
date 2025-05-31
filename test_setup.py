"""
Simple test script to verify the initial setup works correctly
"""
import unittest
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import config
from browser_utils import BrowserManager

class TestInitialSetup(unittest.TestCase):
    """Test cases for initial setup and navigation"""
    
    def setUp(self):
        """Set up test environment"""
        self.browser_manager = None
    
    def tearDown(self):
        """Clean up after tests"""
        if self.browser_manager:
            self.browser_manager.close()
    
    def test_config_loaded(self):
        """Test that configuration is loaded correctly"""
        self.assertIsNotNone(config.BROWSER_CONFIG)
        self.assertIsNotNone(config.WAIT_CONFIG)
        self.assertIsNotNone(config.WEBSITE_CONFIG)
        self.assertIn("base_url", config.WEBSITE_CONFIG)
        print("✓ Configuration loaded successfully")
    
    def test_browser_manager_initialization(self):
        """Test that BrowserManager can be initialized"""
        try:
            self.browser_manager = BrowserManager(headless=True)
            self.assertIsNotNone(self.browser_manager)
            print("✓ BrowserManager initialized successfully")
        except Exception as e:
            self.fail(f"BrowserManager initialization failed: {str(e)}")
    
    def test_chromedriver_exists(self):
        """Test that ChromeDriver executable exists"""
        chrome_driver_path = Path.cwd() / "chromedriver"
        self.assertTrue(chrome_driver_path.exists(), "ChromeDriver not found")
        print("✓ ChromeDriver found")
    
    def test_directories_created(self):
        """Test that required directories exist or can be created"""
        directories = [config.DATA_DIR, config.LOGS_DIR, config.REPORTS_DIR]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            self.assertTrue(directory.exists(), f"Directory {directory} could not be created")
        
        print("✓ All required directories exist")

def run_quick_test():
    """Run a quick test to verify setup"""
    print("Running quick setup verification...")
    print("=" * 50)
    
    try:
        # Test 1: Config loading
        print("1. Testing configuration loading...")
        assert config.BROWSER_CONFIG is not None
        assert config.WEBSITE_CONFIG is not None
        print("   ✓ Configuration loaded")
        
        # Test 2: ChromeDriver existence
        print("2. Checking ChromeDriver...")
        chrome_driver_path = Path.cwd() / "chromedriver"
        assert chrome_driver_path.exists(), "ChromeDriver not found"
        print("   ✓ ChromeDriver found")
        
        # Test 3: Directory creation
        print("3. Creating required directories...")
        directories = [config.DATA_DIR, config.LOGS_DIR, config.REPORTS_DIR]
        for directory in directories:
            directory.mkdir(exist_ok=True)
        print("   ✓ Directories created")
        
        # Test 4: Browser manager initialization (without starting browser)
        print("4. Testing BrowserManager initialization...")
        browser_manager = BrowserManager(headless=True)
        assert browser_manager is not None
        print("   ✓ BrowserManager ready")
        
        print("=" * 50)
        print("🎉 All setup verification tests passed!")
        print("You can now run: python main.py")
        return True
        
    except Exception as e:
        print(f"❌ Setup verification failed: {str(e)}")
        print("Please check the setup instructions in README.md")
        return False

if __name__ == "__main__":
    # Run quick test by default
    if len(sys.argv) == 1 or sys.argv[1] == "quick":
        success = run_quick_test()
        sys.exit(0 if success else 1)
    
    # Run full unittest suite
    elif sys.argv[1] == "full":
        unittest.main(argv=[sys.argv[0]])
    
    else:
        print("Usage:")
        print("  python test_setup.py          # Run quick verification")
        print("  python test_setup.py quick    # Run quick verification")
        print("  python test_setup.py full     # Run full test suite") 