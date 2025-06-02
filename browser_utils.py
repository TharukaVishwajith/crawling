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
        Setup and configure Chrome browser with advanced stealth and anti-detection capabilities
        
        Returns:
            webdriver.Chrome: Configured Chrome driver instance
        """
        try:
            self.logger.info("Setting up Chrome browser with advanced stealth capabilities...")
            
            # Chrome options configuration
            chrome_options = Options()
            
            # Page load strategy - use 'normal' for full compatibility with heavy sites
            chrome_options.page_load_strategy = "normal"  # Changed from 'eager' for better compatibility
            self.logger.info("✓ Set page_load_strategy to 'normal' for full compatibility")
            
            # Set headless mode from config (now False for better stealth)
            if config.BROWSER_CONFIG["headless"]:
                chrome_options.add_argument("--headless")
                self.logger.info("✓ Running in headless mode")
            else:
                self.logger.info("✓ Running in visible mode for better stealth")
            
            # ADVANCED STEALTH: Setup persistent cache directories
            cache_dir = "/tmp/bestbuy_stealth_cache"
            Path(cache_dir).mkdir(exist_ok=True)
            
            chrome_options.add_argument(f"--user-data-dir={cache_dir}")
            chrome_options.add_argument(f"--disk-cache-dir={cache_dir}")
            chrome_options.add_argument(f"--profile-directory=BestBuyProfile")
            self.logger.info(f"✓ Setup persistent stealth profile at {cache_dir}")
            
            # Add all configured options from config
            for option in config.BROWSER_CONFIG["chrome_options"]:
                chrome_options.add_argument(option)
            
            # Set window size to common resolution for better stealth
            window_size = config.BROWSER_CONFIG["window_size"]
            chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            
            # Set realistic user agent
            chrome_options.add_argument(f"--user-agent={config.BROWSER_CONFIG['user_agent']}")
            
            # ADVANCED STEALTH PREFERENCES
            prefs = {
                # Media settings for stealth
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "geolocation": 1,  # Allow geolocation for more realistic behavior
                    "media_stream": 1,  # Allow media for more realistic behavior
                    "plugins": 1,  # Allow plugins
                    "popups": 2,
                },
                
                # Performance optimizations that don't trigger detection
                "profile.default_content_settings.popups": 0,
                "profile.content_settings.exceptions.automatic_downloads.*.setting": 2,
                "profile.default_content_settings.multiple_automatic_downloads": 2,
                
                # Language and locale settings for stealth
                "intl.accept_languages": "en-US,en;q=0.9",
                "profile.managed_default_content_settings": {
                    "images": 1  # Allow images to avoid detection (BestBuy may check)
                },
                
                # Enable hardware acceleration for performance
                "profile.content_settings.exceptions.hardware_acceleration": 1,
                
                # Disable password manager popups but keep functionality
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False,
                
                # Stealth browsing preferences
                "profile.default_content_settings": {
                    "mouselock": 1,
                    "mixed_script": 1,
                    "ssl_cert_decisions": 1
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # ADVANCED ANTI-DETECTION MEASURES
            chrome_options.add_experimental_option("excludeSwitches", [
                "enable-automation", 
                "enable-logging",
                "disable-popup-blocking",
                "test-type"
            ])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Add debug port for stealth (randomized)
            debug_port = random.randint(9222, 9999)
            chrome_options.add_argument(f"--remote-debugging-port={debug_port}")
            
            # Setup Chrome service with local chromedriver
            chrome_driver_path = Path.cwd() / "chromedriver"
            if not chrome_driver_path.exists():
                raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")
            
            service = Service(str(chrome_driver_path))
            
            # Create driver instance
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # ENHANCED STEALTH JAVASCRIPT INJECTIONS
            # Hide webdriver property
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            # Override automation indicators
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            # Add realistic chrome object
            self.driver.execute_script("""
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                };
            """)
            
            # Override permissions API
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' })
                    }),
                });
            """)
            
            # STEALTH TIMEOUTS - Longer for heavy sites like BestBuy
            self.driver.implicitly_wait(config.WAIT_CONFIG["implicit_wait"])
            self.driver.set_page_load_timeout(config.WAIT_CONFIG["page_load_timeout"])
            self.driver.set_script_timeout(config.WAIT_CONFIG["script_timeout"])
            self.logger.info(f"✓ Set stealth timeouts: page_load={config.WAIT_CONFIG['page_load_timeout']}s")
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, config.WAIT_CONFIG["explicit_wait"])
            
            # RANDOMIZE VIEWPORT AND BROWSER FINGERPRINT
            self._randomize_browser_fingerprint()
            
            self.logger.info("✅ Chrome browser setup completed with advanced stealth capabilities")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to setup browser: {str(e)}")
            raise
    
    def _randomize_browser_fingerprint(self):
        """Randomize browser fingerprint to avoid detection"""
        try:
            # Randomize screen resolution within realistic bounds
            screen_width = random.randint(1366, 1920)
            screen_height = random.randint(768, 1080)
            
            # Inject randomized screen properties
            self.driver.execute_script(f"""
                Object.defineProperty(screen, 'width', {{
                    get: () => {screen_width}
                }});
                Object.defineProperty(screen, 'height', {{
                    get: () => {screen_height}
                }});
                Object.defineProperty(screen, 'availWidth', {{
                    get: () => {screen_width}
                }});
                Object.defineProperty(screen, 'availHeight', {{
                    get: () => {screen_height - 40}
                }});
            """)
            
            # Randomize timezone
            timezones = ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles']
            timezone = random.choice(timezones)
            
            self.driver.execute_script(f"""
                Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {{
                    value: function() {{
                        return {{
                            timeZone: '{timezone}',
                            locale: 'en-US'
                        }};
                    }}
                }});
            """)
            
            # Add random mouse movements to appear more human
            self._add_human_like_movements()
            
            self.logger.info("✓ Browser fingerprint randomized for stealth")
            
        except Exception as e:
            self.logger.warning(f"Could not randomize browser fingerprint: {e}")
    
    def _add_human_like_movements(self):
        """Add subtle mouse movements to simulate human behavior"""
        try:
            # Small random mouse movements
            actions = ActionChains(self.driver)
            for _ in range(3):
                x_offset = random.randint(-10, 10)
                y_offset = random.randint(-10, 10)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.3))
            actions.perform()
            
        except Exception as e:
            self.logger.debug(f"Could not add human-like movements: {e}")
    
    def navigate_to_website(self, url: str) -> bool:
        """
        Navigate to specified URL with enhanced stealth and human-like behavior
        
        Args:
            url (str): Target URL to navigate to
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            
            if not self.driver:
                raise ValueError("Browser not initialized. Call setup_browser() first.")
            
            # STEALTH: Add pre-navigation delay
            pre_nav_delay = random.uniform(1.0, 3.0)
            time.sleep(pre_nav_delay)
            
            # Navigate to URL
            self.driver.get(url)
            
            # STEALTH: Add realistic post-navigation behavior
            self._simulate_human_page_interaction()
            
            # Wait for page to load with enhanced waiting
            self.wait_for_page_load()
            
            # STEALTH: Random scroll to simulate reading
            self._simulate_human_scrolling()
            
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
    
    def _simulate_human_page_interaction(self):
        """Simulate human-like interaction after page load"""
        try:
            # Random delay to simulate page scanning
            scan_delay = random.uniform(2.0, 4.0)
            time.sleep(scan_delay)
            
            # Simulate mouse movement patterns
            actions = ActionChains(self.driver)
            
            # Random movements across the page
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 500) 
                actions.move_by_offset(x - 400, y - 250)  # Center around middle
                actions.pause(random.uniform(0.5, 1.5))
            
            actions.perform()
            
        except Exception as e:
            self.logger.debug(f"Could not simulate human interaction: {e}")
    
    def _simulate_human_scrolling(self):
        """Simulate human-like scrolling behavior"""
        try:
            # Random scroll pattern
            scroll_actions = random.randint(2, 4)
            
            for _ in range(scroll_actions):
                # Random scroll amount
                scroll_amount = random.randint(200, 600)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                
                # Random pause between scrolls
                pause_time = random.uniform(1.0, 2.5)
                time.sleep(pause_time)
            
            # Scroll back to top sometimes
            if random.random() < 0.3:
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.logger.debug(f"Could not simulate scrolling: {e}")
    
    def _human_like_delay(self):
        """Enhanced human-like delay with variable patterns"""
        delay = random.uniform(
            config.RATE_LIMIT_CONFIG["min_delay"],
            config.RATE_LIMIT_CONFIG["max_delay"]
        )
        time.sleep(delay)
        
        # Occasionally add longer pauses to simulate reading/thinking
        if random.random() < 0.1:  # 10% chance
            thinking_pause = random.uniform(5.0, 10.0)
            self.logger.debug(f"Adding thinking pause: {thinking_pause:.1f}s")
            time.sleep(thinking_pause)
    
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
        Safely click an element with retry logic and human-like behavior
        
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
            
            # STEALTH: Add pre-click delay and mouse movement
            self._simulate_mouse_movement_to_element(element)
            
            # Scroll element into view gradually (more human-like)
            self._smooth_scroll_to_element(element)
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(element)
            )
            
            # STEALTH: Add slight delay before clicking
            time.sleep(random.uniform(0.3, 0.8))
            
            # Try regular click first
            try:
                element.click()
                self.logger.debug("Element clicked successfully")
                
                # STEALTH: Add post-click delay
                time.sleep(random.uniform(0.5, 1.2))
                return True
                
            except ElementClickInterceptedException:
                # Try JavaScript click if regular click fails
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.debug("Element clicked using JavaScript")
                
                # STEALTH: Add post-click delay
                time.sleep(random.uniform(0.5, 1.2))
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            return False
    
    def _simulate_mouse_movement_to_element(self, element):
        """Simulate realistic mouse movement to an element"""
        try:
            actions = ActionChains(self.driver)
            
            # Get element location
            location = element.location
            size = element.size
            
            # Calculate target point (slightly randomized within element)
            target_x = location['x'] + random.randint(5, size['width'] - 5)
            target_y = location['y'] + random.randint(5, size['height'] - 5)
            
            # Move to element in steps (more human-like)
            steps = random.randint(3, 6)
            for i in range(steps):
                step_x = target_x // steps
                step_y = target_y // steps
                actions.move_by_offset(step_x, step_y)
                actions.pause(random.uniform(0.05, 0.15))
            
            actions.perform()
            
        except Exception as e:
            self.logger.debug(f"Could not simulate mouse movement: {e}")
    
    def _smooth_scroll_to_element(self, element):
        """Smoothly scroll to element like a human would"""
        try:
            # Get element position
            element_y = element.location['y']
            current_scroll = self.driver.execute_script("return window.pageYOffset;")
            
            # Calculate scroll distance
            viewport_height = self.driver.execute_script("return window.innerHeight;")
            target_scroll = max(0, element_y - viewport_height // 2)
            
            # Smooth scroll in steps
            if abs(target_scroll - current_scroll) > 100:  # Only if significant scroll needed
                steps = random.randint(5, 10)
                scroll_diff = target_scroll - current_scroll
                
                for i in range(steps):
                    intermediate_scroll = current_scroll + (scroll_diff * (i + 1) / steps)
                    self.driver.execute_script(f"window.scrollTo(0, {intermediate_scroll});")
                    time.sleep(random.uniform(0.05, 0.15))
            else:
                # Small scroll, just do it normally
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                
            time.sleep(random.uniform(0.3, 0.7))
            
        except Exception as e:
            self.logger.debug(f"Could not smooth scroll: {e}")
            # Fallback to regular scroll
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
    
    def human_like_type(self, element_or_locator: Union[object, tuple], text: str, clear_first: bool = True) -> bool:
        """
        Type text with human-like delays and patterns
        
        Args:
            element_or_locator: WebElement object or locator tuple
            text (str): Text to type
            clear_first (bool): Whether to clear the field first
            
        Returns:
            bool: True if typing successful
        """
        try:
            # Get element if locator provided
            if isinstance(element_or_locator, tuple):
                element = self.wait_for_element(element_or_locator, 10)
                if not element:
                    return False
            else:
                element = element_or_locator
            
            # Focus on element first
            self._focus_element_naturally(element)
            
            # Clear field if requested
            if clear_first:
                element.clear()
                time.sleep(random.uniform(0.2, 0.5))
            
            # Type with human-like delays
            for char in text:
                element.send_keys(char)
                
                # Variable typing delay based on character
                if char == ' ':
                    delay = random.uniform(0.15, 0.4)  # Longer pause for spaces
                elif char in '.,!?':
                    delay = random.uniform(0.2, 0.5)   # Pause for punctuation
                else:
                    delay = random.uniform(
                        config.RATE_LIMIT_CONFIG["human_typing_delay"][0],
                        config.RATE_LIMIT_CONFIG["human_typing_delay"][1]
                    )
                
                time.sleep(delay)
                
                # Occasionally pause longer (like thinking)
                if random.random() < 0.05:  # 5% chance
                    time.sleep(random.uniform(0.5, 1.5))
            
            # Small delay after typing
            time.sleep(random.uniform(0.3, 0.8))
            
            self.logger.debug(f"Successfully typed text: {text[:20]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to type text: {str(e)}")
            return False
    
    def _focus_element_naturally(self, element):
        """Focus on element in a natural way"""
        try:
            # Move mouse to element first
            self._simulate_mouse_movement_to_element(element)
            
            # Click to focus
            element.click()
            
            # Small delay after focus
            time.sleep(random.uniform(0.2, 0.5))
            
        except Exception as e:
            self.logger.debug(f"Could not focus element naturally: {e}")
            # Fallback to simple focus
            try:
                element.click()
            except:
                pass
    
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
    
    def handle_login_popup(self, timeout: int = 5) -> bool:
        """
        Handle login popup/modal that might appear on product pages
        
        Args:
            timeout (int): Timeout to wait for popup detection
            
        Returns:
            bool: True if popup was handled, False if no popup found
        """
        try:
            # First, try to handle JavaScript alert/confirm dialogs
            if self._handle_javascript_alert():
                return True
            
            # Then try to handle DOM-based modal popups
            if self._handle_modal_popup(timeout):
                return True
                
            return False
            
        except Exception as e:
            self.logger.debug(f"Error handling login popup: {e}")
            return False
    
    def _handle_javascript_alert(self) -> bool:
        """Handle JavaScript alert/confirm dialogs"""
        try:
            # Check if there's an alert present
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.logger.info(f"JavaScript alert detected: {alert_text}")
            
            # Dismiss the alert (equivalent to clicking Cancel/No)
            alert.dismiss()
            self.logger.info("✅ JavaScript alert dismissed")
            
            # Add delay after dismissing alert
            time.sleep(random.uniform(0.5, 1.0))
            return True
            
        except:
            # No alert present
            return False
    
    def _handle_modal_popup(self, timeout: int = 5) -> bool:
        """Handle DOM-based modal login popups"""
        try:
            # Common selectors for login/signup modals and close buttons
            modal_selectors = [
                # Generic modal close buttons
                'button[aria-label*="close"]',
                'button[aria-label*="Close"]',
                '[data-testid*="close"]',
                '[data-testid*="Close"]',
                '.close-button',
                '.modal-close',
                '.popup-close',
                
                # Login modal specific selectors
                '[data-testid="modal-close-button"]',
                '[aria-label="Close modal"]',
                '[aria-label="Close dialog"]',
                'button[title*="close"]',
                'button[title*="Close"]',
                
                # X buttons and icons
                'button:contains("×")',
                'span:contains("×")',
                '.fa-times',
                '.fa-close',
                
                # Cancel/Skip buttons
                'button:contains("Cancel")',
                'button:contains("Skip")',
                'button:contains("No thanks")',
                'button:contains("Maybe later")',
                'button:contains("Not now")',
                
                # BestBuy specific selectors (if known)
                '[data-track="modal_close"]',
                '.c-close-icon',
                '.sr-only:contains("Close")',
            ]
            
            # Try each selector
            for selector in modal_selectors:
                try:
                    # Handle CSS selectors with :contains() differently
                    if ':contains(' in selector:
                        # For :contains() selectors, we need to use XPath
                        text_content = selector.split(':contains("')[1].split('")')[0]
                        if selector.startswith('button'):
                            xpath_selector = f"//button[contains(text(), '{text_content}')]"
                        elif selector.startswith('span'):
                            xpath_selector = f"//span[contains(text(), '{text_content}')]"
                        else:
                            xpath_selector = f"//*[contains(text(), '{text_content}')]"
                        
                        element = self.wait_for_element((By.XPATH, xpath_selector), timeout=2)
                    else:
                        element = self.wait_for_element((By.CSS_SELECTOR, selector), timeout=2)
                    
                    if element and element.is_displayed():
                        self.logger.info(f"Found modal close button with selector: {selector}")
                        
                        # Use our stealth click method
                        if self.safe_click(element):
                            self.logger.info("✅ Modal popup dismissed successfully")
                            
                            # Wait a bit for modal to close
                            time.sleep(random.uniform(1.0, 2.0))
                            return True
                        
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # Try to detect modal by checking for overlay/backdrop
            overlay_selectors = [
                '.modal-overlay',
                '.popup-overlay', 
                '.backdrop',
                '.modal-backdrop',
                '[role="dialog"]',
                '[aria-modal="true"]'
            ]
            
            for overlay_selector in overlay_selectors:
                try:
                    overlay = self.wait_for_element((By.CSS_SELECTOR, overlay_selector), timeout=2)
                    if overlay and overlay.is_displayed():
                        self.logger.info(f"Modal overlay detected: {overlay_selector}")
                        
                        # Try to click outside the modal (on the overlay) to close it
                        try:
                            overlay.click()
                            self.logger.info("✅ Modal closed by clicking overlay")
                            time.sleep(random.uniform(1.0, 2.0))
                            return True
                        except:
                            pass
                            
                        # Try pressing Escape key
                        try:
                            from selenium.webdriver.common.keys import Keys
                            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                            self.logger.info("✅ Modal closed with Escape key")
                            time.sleep(random.uniform(1.0, 2.0))
                            return True
                        except:
                            pass
                            
                except Exception as e:
                    self.logger.debug(f"Overlay selector {overlay_selector} failed: {e}")
                    continue
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Error handling modal popup: {e}")
            return False
    
    def safe_navigate_with_popup_handling(self, url: str) -> bool:
        """
        Navigate to URL and automatically handle any login popups that appear
        
        Args:
            url (str): Target URL to navigate to
            
        Returns:
            bool: True if navigation successful
        """
        try:
            # First navigate normally
            success = self.navigate_to_website(url)
            if not success:
                return False
            
            # Wait a moment for any popups to appear or for main content to load
            time.sleep(random.uniform(2.0, 4.0))
            
            # Check if main-results div is already loaded (skip popup handling if so)
            main_results_loaded = False
            try:
                main_results_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "main-results"))
                )
                if main_results_element:
                    self.logger.info("✓ main-results div already loaded - skipping popup handling")
                    main_results_loaded = True
            except TimeoutException:
                self.logger.debug("main-results div not found - will check for popups")
                main_results_loaded = False
            
            # Only handle popups if main-results is not loaded
            if not main_results_loaded:
                # Try to handle any login popups
                popup_handled = self.handle_login_popup()
                if popup_handled:
                    self.logger.info("Login popup detected and dismissed")
                    # Wait a bit more after dismissing popup
                    time.sleep(random.uniform(1.0, 2.0))
            else:
                self.logger.info("Skipped popup handling - main content already loaded")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in safe navigation with popup handling: {e}")
            return False
    
    def monitor_and_dismiss_popups(self, duration: int = 10) -> None:
        """
        Monitor for popups for a specified duration and dismiss them
        Useful when interacting with pages that might trigger delayed popups
        
        Args:
            duration (int): How long to monitor in seconds
        """
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # Check for popups every 2 seconds
                if self.handle_login_popup():
                    self.logger.info("Popup detected and dismissed during monitoring")
                
                time.sleep(2)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.debug(f"Error during popup monitoring: {e}")
                time.sleep(2) 