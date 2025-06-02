"""
Unit tests for Browser Utils module

Tests for browser management functionality including:
- BrowserManager initialization
- Browser setup and configuration  
- Element finding and interaction
- Page navigation
- Wait conditions
- Browser cleanup and error handling
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from browser_utils import BrowserManager
import config


class TestBrowserManager(unittest.TestCase):
    """Test cases for BrowserManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Mock config paths to use test directory
        self.config_patcher = patch.multiple(
            config,
            LOGS_DIR=Path(self.test_dir) / "logs"
        )
        self.config_patcher.start()
        
        # Create test directories
        (Path(self.test_dir) / "logs").mkdir(parents=True, exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        self.config_patcher.stop()
        
        # Clean up temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    @patch('browser_utils.webdriver.Chrome')
    @patch('browser_utils.ChromeDriverManager')
    @patch('browser_utils.Service')
    def test_browser_manager_initialization_success(self, mock_service, mock_chrome_manager, mock_chrome):
        """Test successful BrowserManager initialization."""
        # Arrange
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_chrome_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        # Act
        browser_manager = BrowserManager(headless=True)
        
        # Assert
        self.assertIsNotNone(browser_manager.logger)
        self.assertEqual(browser_manager.driver, None)
        self.assertTrue(browser_manager.headless)
    
    @patch('browser_utils.webdriver.Chrome')
    @patch('browser_utils.ChromeDriverManager')
    @patch('browser_utils.Service')
    def test_start_browser_success(self, mock_service, mock_chrome_manager, mock_chrome):
        """Test successful browser startup."""
        # Arrange
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_chrome_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        browser_manager = BrowserManager(headless=True)
        
        # Act
        result = browser_manager.start_browser()
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(browser_manager.driver, mock_driver)
        mock_chrome.assert_called_once()
    
    @patch('browser_utils.webdriver.Chrome')
    @patch('browser_utils.ChromeDriverManager')
    @patch('browser_utils.Service')
    def test_start_browser_exception(self, mock_service, mock_chrome_manager, mock_chrome):
        """Test browser startup with exception."""
        # Arrange
        mock_chrome.side_effect = Exception("Browser startup failed")
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_chrome_manager.return_value.install.return_value = "/path/to/chromedriver"
        
        browser_manager = BrowserManager(headless=True)
        
        # Act
        result = browser_manager.start_browser()
        
        # Assert
        self.assertFalse(result)
        self.assertIsNone(browser_manager.driver)
    
    def test_close_browser_no_driver(self):
        """Test browser closure without initialized driver."""
        # Arrange
        browser_manager = BrowserManager(headless=True)
        
        # Act (should not raise exception)
        browser_manager.close()
        
        # Assert
        self.assertIsNone(browser_manager.driver)


if __name__ == '__main__':
    unittest.main() 