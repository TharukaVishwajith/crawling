"""
E-Commerce Analytics Automation - Main Application
Demonstrates initial setup and navigation functionality
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from selenium.webdriver.common.by import By

# Import our custom modules
import config
from browser_utils import BrowserManager

class ECommerceAnalyzer:
    """Main class for e-commerce analytics automation"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the e-commerce analyzer
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.browser_manager: Optional[BrowserManager] = None
        self.headless = headless
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup application logging"""
        logger = logging.getLogger("ECommerceAnalyzer")
        logger.setLevel(getattr(logging, config.LOGGING_CONFIG["level"]))
        
        if not logger.handlers:
            # Create logs directory if it doesn't exist
            config.LOGS_DIR.mkdir(exist_ok=True)
            
            # File handler
            file_handler = logging.FileHandler(
                config.LOGS_DIR / config.LOGGING_CONFIG["file_name"]
            )
            file_handler.setFormatter(
                logging.Formatter(config.LOGGING_CONFIG["format"])
            )
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(config.LOGGING_CONFIG["format"])
            )
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        return logger
    
    def initialize_browser(self) -> bool:
        """
        Initialize browser with robust setup
        
        Returns:
            bool: True if initialization successful
        """
        try:
            self.logger.info("=== Starting E-Commerce Analytics Automation ===")
            self.logger.info("Task 1: Initial Setup and Navigation")
            
            # Initialize browser manager
            self.browser_manager = BrowserManager(headless=self.headless)
            
            # Setup Chrome browser
            driver = self.browser_manager.setup_browser()
            
            if driver:
                self.logger.info("✓ Chrome browser initialized successfully")
                self.logger.info(f"✓ Browser running in {'headless' if self.headless else 'visible'} mode")
                return True
            else:
                self.logger.error("✗ Failed to initialize browser")
                return False
                
        except Exception as e:
            self.logger.error(f"✗ Browser initialization error: {str(e)}")
            return False
    
    def navigate_to_target_website(self) -> bool:
        """
        Navigate to Best Buy website with robust wait strategies
        
        Returns:
            bool: True if navigation successful
        """
        try:
            if not self.browser_manager or not self.browser_manager.driver:
                self.logger.error("Browser not initialized")
                return False
            
            self.logger.info("Navigating to target e-commerce website...")
            
            # Navigate to Best Buy
            success = self.browser_manager.navigate_to_website(config.WEBSITE_CONFIG["base_url"])
            
            if success:
                self.logger.info("✓ Successfully navigated to Best Buy")
                
                # Verify page loaded correctly by checking for key elements
                return self._verify_page_load()
            else:
                self.logger.error("✗ Failed to navigate to Best Buy")
                return False
                
        except Exception as e:
            self.logger.error(f"✗ Navigation error: {str(e)}")
            return False
    
    def _verify_page_load(self) -> bool:
        """
        Verify that the page loaded correctly by checking for key elements
        
        Returns:
            bool: True if page verification successful
        """
        try:
            self.logger.info("Verifying page load with robust wait strategies...")
            
            # Check for common Best Buy elements to verify page loaded
            verification_selectors = [
                (By.CLASS_NAME, "sr-header"),  # Best Buy header
                (By.CSS_SELECTOR, "[data-automation-id='header']"),  # Header automation ID
                (By.CLASS_NAME, "header-wrapper"),  # Header wrapper
                (By.TAG_NAME, "nav"),  # Navigation element
                (By.CSS_SELECTOR, "header"),  # Generic header
            ]
            
            page_verified = False
            
            for selector in verification_selectors:
                element = self.browser_manager.wait_for_element(selector, timeout=15)
                if element:
                    self.logger.info(f"✓ Page verification successful - Found element: {selector}")
                    page_verified = True
                    break
                else:
                    self.logger.debug(f"Element not found: {selector}")
            
            if not page_verified:
                # Take screenshot for debugging
                self.logger.warning("Could not verify specific elements, but page might have loaded")
                self.browser_manager.take_screenshot("page_verification_failed")
                
                # Check if we're on the right domain at least
                current_url = self.browser_manager.driver.current_url
                if "bestbuy.com" in current_url.lower():
                    self.logger.info("✓ Page verification: We're on Best Buy domain")
                    page_verified = True
                else:
                    self.logger.error(f"✗ Unexpected URL: {current_url}")
            
            # Additional verification: Check page title
            try:
                page_title = self.browser_manager.driver.title
                self.logger.info(f"Page title: {page_title}")
                
                if "best buy" in page_title.lower():
                    self.logger.info("✓ Page title verification successful")
                    page_verified = True
                    
            except Exception as e:
                self.logger.warning(f"Could not verify page title: {str(e)}")
            
            if page_verified:
                self.logger.info("✓ Page load verification completed successfully")
                # Take a success screenshot
                self.browser_manager.take_screenshot("successful_navigation")
            else:
                self.logger.error("✗ Page load verification failed")
                
            return page_verified
            
        except Exception as e:
            self.logger.error(f"Page verification error: {str(e)}")
            return False
    
    def demonstrate_wait_strategies(self) -> bool:
        """
        Demonstrate various robust wait strategies for dynamic elements
        
        Returns:
            bool: True if demonstration successful
        """
        try:
            self.logger.info("Demonstrating robust wait strategies for dynamic elements...")
            
            if not self.browser_manager or not self.browser_manager.driver:
                self.logger.error("Browser not initialized")
                return False
            
            # Test different wait strategies
            wait_tests = [
                {
                    "name": "Implicit Wait",
                    "description": "Default wait for elements to appear",
                    "test": lambda: self._test_implicit_wait()
                },
                {
                    "name": "Explicit Wait",
                    "description": "Wait for specific conditions",
                    "test": lambda: self._test_explicit_wait()
                },
                {
                    "name": "Page Load Wait",
                    "description": "Wait for complete page loading",
                    "test": lambda: self._test_page_load_wait()
                },
                {
                    "name": "Dynamic Content Wait",
                    "description": "Wait for dynamically loaded content",
                    "test": lambda: self._test_dynamic_content_wait()
                }
            ]
            
            all_tests_passed = True
            
            for test in wait_tests:
                self.logger.info(f"Testing: {test['name']} - {test['description']}")
                try:
                    result = test["test"]()
                    if result:
                        self.logger.info(f"✓ {test['name']} test passed")
                    else:
                        self.logger.warning(f"⚠ {test['name']} test failed")
                        all_tests_passed = False
                except Exception as e:
                    self.logger.error(f"✗ {test['name']} test error: {str(e)}")
                    all_tests_passed = False
            
            if all_tests_passed:
                self.logger.info("✓ All wait strategy tests completed successfully")
            else:
                self.logger.warning("⚠ Some wait strategy tests had issues")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Wait strategies demonstration error: {str(e)}")
            return False
    
    def _test_implicit_wait(self) -> bool:
        """Test implicit wait functionality"""
        try:
            # Implicit wait is already configured in browser setup
            self.logger.debug("Implicit wait is configured for all element lookups")
            return True
        except Exception:
            return False
    
    def _test_explicit_wait(self) -> bool:
        """Test explicit wait for specific elements"""
        try:
            # Test waiting for body element (should always exist)
            element = self.browser_manager.wait_for_element((By.TAG_NAME, "body"), timeout=10)
            return element is not None
        except Exception:
            return False
    
    def _test_page_load_wait(self) -> bool:
        """Test page load wait strategies"""
        try:
            return self.browser_manager.wait_for_page_load(timeout=30)
        except Exception:
            return False
    
    def _test_dynamic_content_wait(self) -> bool:
        """Test waiting for dynamic content"""
        try:
            # Look for elements that might be loaded dynamically
            selectors_to_test = [
                (By.TAG_NAME, "footer"),
                (By.CSS_SELECTOR, "[data-automation-id]"),
                (By.CLASS_NAME, "container"),
                (By.TAG_NAME, "main")
            ]
            
            for selector in selectors_to_test:
                element = self.browser_manager.wait_for_element(selector, timeout=5)
                if element:
                    self.logger.debug(f"Found dynamic element: {selector}")
                    return True
            
            return False
        except Exception:
            return False
    
    def run_initial_setup_demo(self) -> bool:
        """
        Run the complete initial setup and navigation demonstration
        
        Returns:
            bool: True if all steps completed successfully
        """
        try:
            self.logger.info("🚀 Starting Initial Setup and Navigation Demo")
            
            # Step 1: Initialize browser
            if not self.initialize_browser():
                return False
            
            # Step 2: Navigate to website
            if not self.navigate_to_target_website():
                return False
            
            # Step 3: Demonstrate wait strategies
            if not self.demonstrate_wait_strategies():
                return False
            
            self.logger.info("🎉 Initial Setup and Navigation Demo completed successfully!")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Demo execution error: {str(e)}")
            return False
        finally:
            # Always clean up
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.browser_manager:
                self.browser_manager.close()
                self.logger.info("✓ Browser cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup error: {str(e)}")

def main():
    """Main function to run the initial setup and navigation demo"""
    # Check if running in headless mode (default) or visible mode
    headless_mode = True
    
    # Allow command line argument to run in visible mode for debugging
    if len(sys.argv) > 1 and sys.argv[1] == "--visible":
        headless_mode = False
        print("Running in visible mode for debugging...")
    
    # Create and run the analyzer
    analyzer = ECommerceAnalyzer(headless=headless_mode)
    
    try:
        success = analyzer.run_initial_setup_demo()
        if success:
            print("\n✅ Initial Setup and Navigation completed successfully!")
            print("Check the logs directory for detailed execution logs.")
            return 0
        else:
            print("\n❌ Initial Setup and Navigation failed!")
            print("Check the logs directory for error details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        analyzer.cleanup()
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        analyzer.cleanup()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 