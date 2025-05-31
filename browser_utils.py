"""
Browser utilities for E-Commerce Analytics Automation
Handles browser setup, navigation, and wait strategies
"""
import logging
import time
import random
from typing import Optional, List, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)
from pathlib import Path
import config

class BrowserManager:
    """Manages Chrome browser instance with robust setup and navigation capabilities"""
    
    def __init__(self, headless: bool = True):
        """
        Initialize the browser manager
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.headless = headless
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for browser operations"""
        logger = logging.getLogger(__name__)
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
    
    def setup_browser(self) -> webdriver.Chrome:
        """
        Setup and configure Chrome browser with optimal settings
        
        Returns:
            webdriver.Chrome: Configured Chrome driver instance
        """
        try:
            self.logger.info("Setting up Chrome browser with fast loading optimizations...")
            
            # Chrome options configuration
            chrome_options = Options()
            
            # FAST LOADING OPTIMIZATION: Use eager page load strategy
            chrome_options.page_load_strategy = "eager"  # DOMContentLoaded ⇒ stop, skip fonts/images
            self.logger.info("✓ Set page_load_strategy to 'eager' for faster loading")
            
            # Set headless mode
            if self.headless:
                chrome_options.add_argument("--headless")
                self.logger.info("✓ Running in headless mode")
            
            # CACHING OPTIMIZATION: Setup persistent cache directories
            cache_dir = "/tmp/bo_cache"  # Use consistent cache dir from user's make_driver
            Path(cache_dir).mkdir(exist_ok=True)
            
            chrome_options.add_argument(f"--user-data-dir={cache_dir}")    # persistent profile
            chrome_options.add_argument(f"--disk-cache-dir={cache_dir}")   # disk cache
            self.logger.info(f"✓ Setup persistent cache at {cache_dir}")
            
            # Add all configured options from config
            for option in config.BROWSER_CONFIG["chrome_options"]:
                chrome_options.add_argument(option)
            
            # Additional performance optimizations from user's make_driver function
            performance_options = [
                "--disable-images",                    # Block images for faster loading
                "--disable-plugins",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-features=TranslateUI",
                "--aggressive-cache-discard",
                "--memory-pressure-off"
            ]
            
            for option in performance_options:
                chrome_options.add_argument(option)
            
            # Set window size
            window_size = config.BROWSER_CONFIG["window_size"]
            chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            
            # Set user agent
            chrome_options.add_argument(f"--user-agent={config.BROWSER_CONFIG['user_agent']}")
            
            # Chrome preferences for faster loading
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "geolocation": 2,
                    "media_stream": 2,
                    "plugins": 2,              # Block plugins
                    "popups": 2,               # Block popups
                },
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings": {
                    "images": 2                # Block images for faster loading
                },
                # Disable various features for speed
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 2,
                "profile.default_content_settings.multiple_automatic_downloads": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Exclude automation flags
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Setup Chrome service with local chromedriver
            chrome_driver_path = Path.cwd() / "chromedriver"
            if not chrome_driver_path.exists():
                raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")
            
            service = Service(str(chrome_driver_path))
            
            # Create driver instance
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # FAST TIMEOUT OPTIMIZATION: Set shorter timeouts (similar to user's 25s timeout)
            self.driver.implicitly_wait(5)        # Reduced from config default
            self.driver.set_page_load_timeout(25) # Use timeout from user's make_driver
            self.driver.set_script_timeout(15)    # Reduced timeout
            self.logger.info("✓ Set optimized timeouts: page_load=25s, script=15s, implicit=5s")
            
            # Initialize WebDriverWait with shorter timeout
            self.wait = WebDriverWait(self.driver, 15)  # Reduced from config default
            
            # Execute script to hide automation flags
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.logger.info("✅ Chrome browser setup completed with fast loading optimizations")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to setup browser: {str(e)}")
            raise
    
    def navigate_to_website(self, url: str) -> bool:
        """
        Navigate to specified URL with error handling and validation
        
        Args:
            url (str): Target URL to navigate to
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            
            if not self.driver:
                raise ValueError("Browser not initialized. Call setup_browser() first.")
            
            # Navigate to URL
            self.driver.get(url)
            
            # Add random delay to mimic human behavior
            self._human_like_delay()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Verify navigation success
            current_url = self.driver.current_url
            self.logger.info(f"Successfully navigated to: {current_url}")
            
            return True
            
        except TimeoutException:
            self.logger.error(f"Timeout while navigating to {url}")
            return False
        except WebDriverException as e:
            self.logger.error(f"WebDriver error during navigation: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during navigation: {str(e)}")
            return False
    
    def wait_for_element(self, locator: tuple, timeout: Optional[int] = None) -> Optional[object]:
        """
        Wait for element to be present and visible with robust error handling
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "selector")
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            WebElement or None: Found element or None if not found
        """
        try:
            wait_time = timeout or config.WAIT_CONFIG["explicit_wait"]
            custom_wait = WebDriverWait(self.driver, wait_time)
            
            # Wait for element to be present and visible
            element = custom_wait.until(
                EC.visibility_of_element_located(locator)
            )
            
            self.logger.debug(f"Element found: {locator}")
            return element
            
        except TimeoutException:
            self.logger.warning(f"Element not found within {wait_time}s: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"Error waiting for element {locator}: {str(e)}")
            return None
    
    def wait_for_elements(self, locator: tuple, timeout: Optional[int] = None) -> List:
        """
        Wait for multiple elements to be present
        
        Args:
            locator (tuple): Locator tuple (By.METHOD, "selector")
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            List: List of found elements (empty if none found)
        """
        try:
            wait_time = timeout or config.WAIT_CONFIG["explicit_wait"]
            custom_wait = WebDriverWait(self.driver, wait_time)
            
            elements = custom_wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
            
        except TimeoutException:
            self.logger.warning(f"No elements found within {wait_time}s: {locator}")
            return []
        except Exception as e:
            self.logger.error(f"Error waiting for elements {locator}: {str(e)}")
            return []
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for page to fully load using multiple strategies
        
        Args:
            timeout (int, optional): Custom timeout in seconds
            
        Returns:
            bool: True if page loaded successfully
        """
        try:
            wait_time = timeout or config.WAIT_CONFIG["page_load_timeout"]
            
            # Wait for document ready state
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for jQuery if present
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda driver: driver.execute_script("return jQuery.active == 0")
                )
            except:
                pass  # jQuery might not be present
            
            # Additional delay for dynamic content
            time.sleep(config.RATE_LIMIT_CONFIG["page_load_delay"])
            
            self.logger.debug("Page load completed")
            return True
            
        except TimeoutException:
            self.logger.warning("Page load timeout")
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for page load: {str(e)}")
            return False
    
    def safe_click(self, element_or_locator: Union[object, tuple], timeout: int = 10) -> bool:
        """
        Safely click an element with retry logic and error handling
        
        Args:
            element_or_locator: WebElement object or locator tuple
            timeout (int): Timeout for finding element
            
        Returns:
            bool: True if click successful
        """
        try:
            # Get element if locator provided
            if isinstance(element_or_locator, tuple):
                element = self.wait_for_element(element_or_locator, timeout)
                if not element:
                    return False
            else:
                element = element_or_locator
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(element)
            )
            
            # Try regular click first
            try:
                element.click()
                self.logger.debug("Element clicked successfully")
                return True
            except ElementClickInterceptedException:
                # Try JavaScript click if regular click fails
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.debug("Element clicked using JavaScript")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            return False
    
    def _human_like_delay(self):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(
            config.RATE_LIMIT_CONFIG["min_delay"],
            config.RATE_LIMIT_CONFIG["max_delay"]
        )
        time.sleep(delay)
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take screenshot for debugging purposes
        
        Args:
            filename (str): Screenshot filename
            
        Returns:
            bool: True if screenshot taken successfully
        """
        try:
            screenshot_path = config.LOGS_DIR / f"{filename}.png"
            self.driver.save_screenshot(str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return False
    
    def close(self):
        """Close browser and clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")
        finally:
            self.driver = None
            self.wait = None
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close() 