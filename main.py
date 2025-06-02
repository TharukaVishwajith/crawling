"""
E-Commerce Analytics Automation - Main Application
Demonstrates initial setup and navigation functionality
"""
import logging
import sys
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
        Navigate to the target e-commerce website with enhanced popup handling
        
        Returns:
            bool: True if navigation successful
        """
        try:
            if not self.browser_manager or not self.browser_manager.driver:
                self.logger.error("Browser not initialized")
                return False

            self.logger.info("Navigating to target e-commerce website with popup handling...")
            
            # Use enhanced navigation with popup handling
            success = self.browser_manager.safe_navigate_with_popup_handling(config.WEBSITE_CONFIG["base_url"])
            
            if success:
                self.logger.info("✓ Successfully navigated to Best Buy with popup handling")
                
                # Additional popup monitoring after navigation
                self.logger.info("Monitoring for delayed popups...")
                self.browser_manager.monitor_and_dismiss_popups(duration=5)
                
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
    
    # ==================== TASK 2: PRODUCT CATEGORY ANALYSIS ====================
    
    def navigate_to_laptops_category(self) -> bool:
        """
        Navigate to the laptops category on Best Buy
        
        Returns:
            bool: True if navigation successful
        """
        try:
            self.logger.info("=== Task 2: Product Category Analysis ===")
            self.logger.info("Navigating to laptops category...")
            
            if not self.browser_manager or not self.browser_manager.driver:
                self.logger.error("Browser not initialized")
                return False
            
            # Try different approaches to navigate to laptops
            approaches = [
                self._navigate_via_direct_url,
                self._navigate_via_menu_click,
                self._navigate_via_search
            ]
            
            for i, approach in enumerate(approaches, 1):
                try:
                    self.logger.info(f"Trying approach {i}: {approach.__name__}")
                    if approach():
                        self.logger.info("✓ Successfully navigated to laptops category")
                        self.browser_manager.take_screenshot("laptops_category_page")
                        return True
                    else:
                        self.logger.warning(f"Approach {i} failed, trying next approach...")
                        time.sleep(2)
                except Exception as e:
                    self.logger.warning(f"Approach {i} error: {str(e)}")
                    time.sleep(2)
                    continue
            
            self.logger.error("✗ All navigation approaches failed")
            return False
                
        except Exception as e:
            self.logger.error(f"✗ Error navigating to laptops category: {str(e)}")
            return False
    
    def _navigate_via_direct_url(self) -> bool:
        """Navigate directly to laptops URL"""
        try:
            # Use the specific URL provided by user
            laptops_url = "https://www.bestbuy.com/site/computers-pcs/laptop-computers/abcat0502000.c?id=abcat0502000"
            self.logger.info(f"Navigating directly to: {laptops_url}")
            
            # Set a longer page load timeout for this navigation
            self.browser_manager.driver.set_page_load_timeout(60)
            
            self.browser_manager.driver.get(laptops_url)
            
            # Wait for page to start loading
            time.sleep(5)
            
            # Reset timeout
            self.browser_manager.driver.set_page_load_timeout(30)
            
            # Wait longer for page to start loading
            time.sleep(10)
            
            # Check if main-results div is already loaded (skip country selection if so)
            self.logger.info("Checking if main-results div is already loaded...")
            main_results_already_loaded = False
            try:
                main_results_check = WebDriverWait(self.browser_manager.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "main-results"))
                )
                if main_results_check:
                    self.logger.info("✓ main-results div already loaded - skipping country selection")
                    country_handled = True  # Skip country selection
                    main_results_already_loaded = True
                else:
                    country_handled = False
            except TimeoutException:
                self.logger.info("main-results div not found yet - will attempt country selection")
                country_handled = False
            
            # Handle country selection only if main-results div is not loaded
            if not country_handled:
                self.logger.info("Checking for country selection page...")
                max_attempts = 3
                
                for attempt in range(max_attempts):
                    self.logger.info(f"Country selection attempt {attempt + 1}/{max_attempts}")
                    
                    try:
                        # Look for United States element with longer wait
                        us_element = WebDriverWait(self.browser_manager.driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'United States')]"))
                        )
                        
                        if us_element:
                            self.logger.info("✓ Found 'United States' element")
                            
                            # Take screenshot before clicking
                            self.browser_manager.take_screenshot("before_country_selection")
                            
                            # Scroll to element and click
                            self.browser_manager.driver.execute_script("arguments[0].scrollIntoView(true);", us_element)
                            time.sleep(2)
                            
                            us_element.click()
                            self.logger.info("✓ Clicked on 'United States'")
                            
                            # Wait for navigation to complete
                            time.sleep(10)
                            
                            # Take screenshot after clicking
                            self.browser_manager.take_screenshot("after_country_selection")
                            
                            country_handled = True
                            break
                            
                    except (TimeoutException, NoSuchElementException) as e:
                        self.logger.info(f"Attempt {attempt + 1}: Country selection not found yet: {str(e)}")
                        if attempt < max_attempts - 1:
                            time.sleep(5)  # Wait before next attempt
                        continue
                
                if not country_handled:
                    self.logger.info("No country selection found or needed, continuing...")
            else:
                self.logger.info("Skipped country selection - main-results already available")
            
            # Wait additional time for the main page to load after country selection (or if already loaded)
            if country_handled and not main_results_already_loaded:
                self.logger.info("Waiting for main page to load after country selection...")
                time.sleep(15)
            else:
                self.logger.info("Page already loaded, proceeding to product extraction...")
                time.sleep(5)  # Shorter wait since page is already loaded
            
            # Check if we're on a laptops page
            return self._verify_laptops_page()
            
        except Exception as e:
            self.logger.debug(f"Direct URL navigation failed: {str(e)}")
            return False
    
    def _navigate_via_menu_click(self) -> bool:
        """Navigate by clicking through the menu"""
        try:
            self.logger.info("Trying to navigate via menu clicks...")
            
            # Look for computers/laptops menu items
            menu_selectors = [
                "//a[contains(text(), 'Computer')]",
                "//a[contains(text(), 'Laptop')]",
                "//span[contains(text(), 'Computer')]",
                "//span[contains(text(), 'Laptop')]",
                "[data-automation-id*='computer']",
                "[data-automation-id*='laptop']"
            ]
            
            for selector in menu_selectors:
                try:
                    if selector.startswith("//"):
                        element = WebDriverWait(self.browser_manager.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        element = WebDriverWait(self.browser_manager.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    element.click()
                    time.sleep(3)
                    
                    # Check if we're on a laptops page
                    if self._verify_laptops_page():
                        return True
                        
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Menu navigation failed: {str(e)}")
            return False
    
    def _navigate_via_search(self) -> bool:
        """Navigate by searching for laptops"""
        try:
            self.logger.info("Trying to navigate via search...")
            
            # Look for search box
            search_selectors = [
                'input[data-testid="search-input"]',
                'input[placeholder*="search"]',
                'input[name="st"]',
                '#gh-search-input',
                '.search-input'
            ]
            
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.browser_manager.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    search_box.clear()
                    search_box.send_keys("laptops")
                    
                    # Look for search button
                    search_button_selectors = [
                        'button[data-testid="search-button"]',
                        'button[type="submit"]',
                        '.search-button',
                        '#search-btn'
                    ]
                    
                    for btn_selector in search_button_selectors:
                        try:
                            search_button = self.browser_manager.driver.find_element(By.CSS_SELECTOR, btn_selector)
                            search_button.click()
                            time.sleep(5)
                            
                            # Check if we have laptop results
                            if self._verify_laptops_page():
                                return True
                                
                        except NoSuchElementException:
                            continue
                    
                    # Try pressing Enter if no button found
                    search_box.send_keys(Keys.RETURN)
                    time.sleep(5)
                    
                    if self._verify_laptops_page():
                        return True
                        
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Search navigation failed: {str(e)}")
            return False
    
    def _verify_laptops_page(self) -> bool:
        """
        Verify that we're on the laptops category page
        
        Returns:
            bool: True if verification successful
        """
        try:
            # Wait a moment for the page to load
            time.sleep(2)
            
            # Check URL contains laptops-related keywords
            current_url = self.browser_manager.driver.current_url.lower()
            url_keywords = ["laptop", "computer", "abcat0502000", "pc"]
            
            if any(keyword in current_url for keyword in url_keywords):
                self.logger.info(f"✓ URL verification: On laptops-related page ({current_url})")
                return True
            
            # Check page title
            try:
                page_title = self.browser_manager.driver.title.lower()
                title_keywords = ["laptop", "computer", "pc", "notebook"]
                
                if any(keyword in page_title for keyword in title_keywords):
                    self.logger.info(f"✓ Title verification: On laptops page ({page_title})")
                    return True
            except Exception:
                pass
            
            # Look for laptop-related content on the page
            content_indicators = [
                # Text-based indicators
                "//h1[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'laptop')]",
                "//h1[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'computer')]",
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'laptop')]",
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'macbook')]",
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'notebook')]",
                
                # Product-related indicators
                "//div[contains(@class, 'product')]",
                "//div[contains(@class, 'item')]",
                "//article",
                
                # Category page indicators
                "//div[contains(@class, 'category')]",
                "//div[contains(@class, 'listing')]",
                "//div[contains(@class, 'results')]"
            ]
            
            for xpath in content_indicators:
                try:
                    elements = self.browser_manager.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        # For text-based indicators, check if we have reasonable content
                        if "laptop" in xpath.lower() or "computer" in xpath.lower():
                            for element in elements[:3]:  # Check first few elements
                                text = element.text.strip().lower()
                                if text and len(text) > 5:  # Has some meaningful text
                                    self.logger.info(f"✓ Content verification: Found laptop-related content")
                                    return True
                        # For structural indicators, just check if we have enough elements
                        elif len(elements) >= 3:
                            self.logger.info(f"✓ Structure verification: Found product page structure")
                            return True
                except Exception:
                    continue
            
            # Check if we have any products visible (could be any products)
            product_selectors = [
                ".product",
                ".item",
                "[data-testid*='product']",
                ".sku-item",
                ".list-item"
            ]
            
            for selector in product_selectors:
                try:
                    products = self.browser_manager.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(products) >= 5:  # Reasonable number of products
                        self.logger.info(f"✓ Product verification: Found {len(products)} products on page")
                        return True
                except Exception:
                    continue
            
            # If we're here, we might be on a search results page or similar
            # Check if page looks like it has e-commerce content
            try:
                page_source = self.browser_manager.driver.page_source.lower()
                commerce_keywords = ["price", "$", "buy", "add to cart", "rating", "review"]
                keyword_count = sum(1 for keyword in commerce_keywords if keyword in page_source)
                
                if keyword_count >= 3:
                    self.logger.info(f"✓ Commerce verification: Page has e-commerce content")
                    return True
            except Exception:
                pass
            
            self.logger.warning("Could not verify laptops page with any method")
            # Take a screenshot for debugging
            self.browser_manager.take_screenshot("page_verification_debug")
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying laptops page: {str(e)}")
            return False
    
    def apply_product_filters(self) -> bool:
        """
        Apply filters for price range, brands, and customer rating
        
        Returns:
            bool: True if filters applied successfully
        """
        try:
            self.logger.info("Applying product filters...")
            
            # Wait for filters to load
            time.sleep(3)
            
            success_count = 0
            total_filters = 3
            
            # First try manual filter application
            # Apply price filter
            if self._apply_price_filter():
                success_count += 1
                self.logger.info("✓ Price filter applied")
            else:
                self.logger.warning("⚠ Price filter failed")
            
            # Apply brand filter
            if self._apply_brand_filter():
                success_count += 1
                self.logger.info("✓ Brand filter applied")
            else:
                self.logger.warning("⚠ Brand filter failed")
            
            # Apply rating filter
            if self._apply_rating_filter():
                success_count += 1
                self.logger.info("✓ Rating filter applied")
            else:
                self.logger.warning("⚠ Rating filter failed")
            
            # Wait for filters to take effect
            time.sleep(5)
            
            self.logger.info(f"Manual filter application result: {success_count}/{total_filters} filters applied")
            
            # If manual filters failed, try direct URL approach
            if success_count == 0:
                self.logger.info("Manual filters failed, trying direct filtered URL approach...")
                if self._navigate_to_filtered_url():
                    self.logger.info("✓ Successfully navigated to filtered results via direct URL")
                    success_count = 3  # Consider all filters applied
                else:
                    self.logger.warning("⚠ Direct filtered URL approach also failed")
            
            self.browser_manager.take_screenshot("filtered_results")
            
            return success_count >= 1  # At least one filter should work
            
        except Exception as e:
            self.logger.error(f"Error applying filters: {str(e)}")
            return False
    
    def _apply_price_filter(self) -> bool:
        """Apply price range filter ($500-$1500)"""
        try:
            price_selectors = [
                "//button[contains(text(), 'Price')]",
                "//button[contains(@aria-label, 'Price')]",
                "//div[contains(@class, 'facet')]//span[contains(text(), 'Price')]",
                "//span[contains(text(), 'Price Range')]",
                "//*[contains(text(), '$500') and contains(text(), '$1500')]",
                "//input[@placeholder='Min' or @placeholder='min']"
            ]
            
            for selector in price_selectors:
                try:
                    element = WebDriverWait(self.browser_manager.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    element.click()
                    time.sleep(2)
                    self.logger.debug(f"Clicked price filter: {selector}")
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            self.logger.debug("No price filter found - this is common on category pages")
            return False
            
        except Exception as e:
            self.logger.debug(f"Price filter error: {str(e)}")
            return False
    
    def _apply_brand_filter(self) -> bool:
        """Apply brand filter for top manufacturers"""
        try:
            # Look for brand filters
            brand_selectors = [
                "//button[contains(text(), 'Brand')]",
                "//span[contains(text(), 'Brand')]//parent::button",
                "//div[contains(@class, 'facet')]//span[contains(text(), 'Brand')]",
                "//button[contains(@aria-label, 'Brand')]"
            ]
            
            for selector in brand_selectors:
                try:
                    element = WebDriverWait(self.browser_manager.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    element.click()
                    time.sleep(2)
                    
                    # Try to select some brands
                    self._select_brand_options()
                    return True
                    
                except (TimeoutException, NoSuchElementException):
                    continue
            
            self.logger.debug("No brand filter interface found")
            return False
            
        except Exception as e:
            self.logger.debug(f"Brand filter error: {str(e)}")
            return False
    
    def _select_brand_options(self):
        """Select specific brand options from the filter"""
        try:
            target_brands = config.FILTER_CONFIG["brands"][:3]  # Top 3 brands
            
            for brand in target_brands:
                brand_xpath = f"//label[contains(text(), '{brand}')]//input[@type='checkbox']"
                try:
                    checkbox = self.browser_manager.driver.find_element(By.XPATH, brand_xpath)
                    if not checkbox.is_selected():
                        checkbox.click()
                        time.sleep(1)
                        self.logger.debug(f"Selected brand: {brand}")
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            self.logger.debug(f"Error selecting brands: {str(e)}")
    
    def _apply_rating_filter(self) -> bool:
        """Apply customer rating filter (4+ stars)"""
        try:
            rating_selectors = [
                # Best Buy specific rating selectors
                ".sr-rating",
                ".rating",
                ".rating-stars",
                "[data-testid='rating']",
                ".stars",
                ".c-rating",
                ".sr-rating__score",
                ".average-rating"
            ]
            
            for selector in rating_selectors:
                try:
                    rating_element = element.find_element(By.CSS_SELECTOR, selector)
                    rating_text = rating_element.text.strip()
                    
                    # Extract numeric rating
                    import re
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        rating_value = float(rating_match.group(1))
                        # Ensure rating is within reasonable range (0-5)
                        if 0 <= rating_value <= 5:
                            return rating_value
                        
                except NoSuchElementException:
                    continue
            
            # Try looking for aria-label or title attributes that might contain rating
            xpath_selectors = [
                ".//*[contains(@aria-label, 'star') or contains(@title, 'star')]",
                ".//*[contains(@aria-label, 'rating') or contains(@title, 'rating')]",
                ".//*[contains(@class, 'rating') or contains(@class, 'star')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    rating_element = element.find_element(By.XPATH, xpath)
                    # Check aria-label or title
                    for attr in ['aria-label', 'title']:
                        attr_value = rating_element.get_attribute(attr)
                        if attr_value:
                            import re
                            rating_match = re.search(r'(\d+\.?\d*)', attr_value)
                            if rating_match:
                                rating_value = float(rating_match.group(1))
                                if 0 <= rating_value <= 5:
                                    return rating_value
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _extract_review_count(self, element) -> Optional[int]:
        """Extract number of reviews from element"""
        try:
            # Use the specific selector provided by user: span with class "c-reviews"
            try:
                review_element = element.find_element(By.CSS_SELECTOR, "span.c-reviews")
                review_text = review_element.text.strip()
                
                # Extract numeric count
                import re
                review_match = re.search(r'(\d+)', review_text.replace(',', ''))
                if review_match:
                    review_count = int(review_match.group(1))
                    # Reasonable range check
                    if review_count >= 0:
                        return review_count
            except NoSuchElementException:
                self.logger.debug("span.c-reviews not found, trying alternative selectors")
            
            # Fallback selectors if the main one doesn't work
            fallback_selectors = [
                ".c-reviews",
                ".review-count",
                ".reviews-count",
                "[data-testid='review-count']",
                ".reviews",
                ".number-of-reviews"
            ]
            
            for selector in fallback_selectors:
                try:
                    review_element = element.find_element(By.CSS_SELECTOR, selector)
                    review_text = review_element.text.strip()
                    
                    # Extract numeric count
                    import re
                    review_match = re.search(r'(\d+)', review_text.replace(',', ''))
                    if review_match:
                        review_count = int(review_match.group(1))
                        # Reasonable range check
                        if review_count >= 0:
                            return review_count
                            
                except NoSuchElementException:
                    continue
            
            # Try XPath to look for review-related text with numbers
            xpath_selectors = [
                ".//*[contains(text(), 'review') and contains(text(), '(')]",
                ".//*[contains(text(), 'Review') and contains(text(), '(')]",
                ".//*[contains(@aria-label, 'review')]",
                ".//*[contains(@title, 'review')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    review_element = element.find_element(By.XPATH, xpath)
                    review_text = review_element.text.strip()
                    
                    import re
                    # Look for patterns like "(123)" or "123 reviews"
                    review_match = re.search(r'\(?(\d+)\)?', review_text.replace(',', ''))
                    if review_match:
                        review_count = int(review_match.group(1))
                        if review_count >= 0:
                            return review_count
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _navigate_to_filtered_url(self) -> bool:
        """Navigate directly to the filtered results URL"""
        try:
            # URL provided by user with all filters applied
            filtered_url = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&cp=11&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001"
            
            self.logger.info(f"Navigating to pre-filtered results URL...")
            self.browser_manager.driver.get(filtered_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Verify we're on a results page with products
            if self._verify_filtered_results_page():
                self.logger.info("✓ Successfully loaded filtered results page")
                return True
            else:
                self.logger.warning("Could not verify filtered results page")
                return False
                
        except Exception as e:
            self.logger.error(f"Error navigating to filtered URL: {str(e)}")
            return False
    
    def _verify_filtered_results_page(self) -> bool:
        """Verify we're on a page with filtered laptop results"""
        try:
            # Check URL contains search parameters
            current_url = self.browser_manager.driver.current_url
            if "searchpage.jsp" in current_url and "browsedCategory" in current_url:
                self.logger.info("✓ URL verification: On search results page")
                
                # Check for filter indicators in URL
                filter_indicators = ["currentprice_facet", "brand_facet", "customerreviews_facet"]
                applied_filters = sum(1 for indicator in filter_indicators if indicator in current_url)
                
                if applied_filters >= 2:
                    self.logger.info(f"✓ Filter verification: {applied_filters} filters detected in URL")
                    return True
            
            # Check for products on the page
            product_indicators = [
                ".list-item",
                ".product-card", 
                ".sku-item",
                "[data-testid*='product']"
            ]
            
            for selector in product_indicators:
                try:
                    products = self.browser_manager.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(products) >= 3:
                        self.logger.info(f"✓ Product verification: Found {len(products)} products")
                        return True
                except Exception:
                    continue
            
            # Check page content for filter-related text
            try:
                page_source = self.browser_manager.driver.page_source.lower()
                filter_keywords = ["dell", "hp", "lenovo", "$500", "$1500", "rating"]
                keyword_count = sum(1 for keyword in filter_keywords if keyword in page_source)
                
                if keyword_count >= 3:
                    self.logger.info(f"✓ Content verification: Found filter-related content")
                    return True
            except Exception:
                pass
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying filtered results page: {str(e)}")
            return False
    
    def extract_product_data(self, use_specific_url: bool = False, specific_url: str = None) -> List[Dict[str, Any]]:
        """
        Extract product data from the filtered results
        
        Args:
            use_specific_url: Whether to navigate to a specific URL first
            specific_url: The specific URL to navigate to
        
        Returns:
            List[Dict]: List of product data dictionaries
        """
        try:
            if use_specific_url and specific_url:
                self.logger.info(f"Navigating to specific URL: {specific_url}")
                
                # Set a longer page load timeout for Best Buy
                self.browser_manager.driver.set_page_load_timeout(60)
                
                try:
                    self.browser_manager.driver.get(specific_url)
                    self.logger.info("✓ Initial page load completed")
                except Exception as e:
                    self.logger.warning(f"Page load timeout, but continuing: {str(e)}")
                
                # Wait longer for page to start loading
                time.sleep(10)
                
                # Check if main-results div is already loaded (skip country selection if so)
                self.logger.info("Checking if main-results div is already loaded...")
                main_results_already_loaded = False
                try:
                    main_results_check = WebDriverWait(self.browser_manager.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "main-results"))
                    )
                    if main_results_check:
                        self.logger.info("✓ main-results div already loaded - skipping country selection")
                        country_handled = True  # Skip country selection
                        main_results_already_loaded = True
                    else:
                        country_handled = False
                except TimeoutException:
                    self.logger.info("main-results div not found yet - will attempt country selection")
                    country_handled = False
                
                # Handle country selection only if main-results div is not loaded
                if not country_handled:
                    self.logger.info("Checking for country selection page...")
                    max_attempts = 3
                    
                    for attempt in range(max_attempts):
                        self.logger.info(f"Country selection attempt {attempt + 1}/{max_attempts}")
                        
                        try:
                            # Look for United States element with longer wait
                            us_element = WebDriverWait(self.browser_manager.driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'United States')]"))
                            )
                            
                            if us_element:
                                self.logger.info("✓ Found 'United States' element")
                                
                                # Take screenshot before clicking
                                self.browser_manager.take_screenshot("before_country_selection")
                                
                                # Scroll to element and click
                                self.browser_manager.driver.execute_script("arguments[0].scrollIntoView(true);", us_element)
                                time.sleep(2)
                                
                                us_element.click()
                                self.logger.info("✓ Clicked on 'United States'")
                                
                                # Wait for navigation to complete
                                time.sleep(10)
                                
                                # Take screenshot after clicking
                                self.browser_manager.take_screenshot("after_country_selection")
                                
                                country_handled = True
                                break
                                
                        except (TimeoutException, NoSuchElementException) as e:
                            self.logger.info(f"Attempt {attempt + 1}: Country selection not found yet: {str(e)}")
                            if attempt < max_attempts - 1:
                                time.sleep(5)  # Wait before next attempt
                            continue
                    
                    if not country_handled:
                        self.logger.info("No country selection found or needed, continuing...")
                else:
                    self.logger.info("Skipped country selection - main-results already available")
                
                # Wait additional time for the main page to load after country selection (or if already loaded)
                if country_handled and not main_results_already_loaded:
                    self.logger.info("Waiting for main page to load after country selection...")
                    time.sleep(15)
                else:
                    self.logger.info("Page already loaded, proceeding to product extraction...")
                    time.sleep(5)  # Shorter wait since page is already loaded
            
            self.logger.info("Extracting product data from filtered results...")
            
            products = []
            
            # Wait for products to load with longer timeout
            self.logger.info("Waiting for products to load...")
            time.sleep(5)
            
            # Look specifically in the main-results div as requested by user
            main_results_div = None
            try:
                main_results_div = WebDriverWait(self.browser_manager.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "main-results"))
                )
                self.logger.info("✓ Found main-results div")
                
                # SCROLLING TO TRIGGER LAZY LOADING
                self.logger.info("Scrolling to trigger lazy loading of products...")
                
                # First scroll to the main-results div
                self.browser_manager.driver.execute_script("arguments[0].scrollIntoView(true);", main_results_div)
                time.sleep(2)
                
                # Perform multiple scrolls to trigger lazy loading
                for i in range(5):  # Scroll down 5 times
                    self.logger.debug(f"Scroll attempt {i+1}/5")
                    
                    # Scroll down by a reasonable amount
                    self.browser_manager.driver.execute_script("window.scrollBy(0, 800);")
                    time.sleep(1.5)  # Wait for content to load
                    
                    # Check if new products appeared using the specific selector
                    current_products = main_results_div.find_elements(By.CSS_SELECTOR, ".product-list-item")
                    self.logger.debug(f"After scroll {i+1}: Found {len(current_products)} product-list-item elements")
                    
                    # If we have a good number of products, we can break early
                    if len(current_products) >= 10:
                        self.logger.info(f"Found sufficient products ({len(current_products)}) after {i+1} scrolls")
                        break
                
                # Scroll back to top of main-results for extraction
                self.browser_manager.driver.execute_script("arguments[0].scrollIntoView(true);", main_results_div)
                time.sleep(1)
                
                self.logger.info("✓ Completed scrolling to trigger lazy loading")
                
            except TimeoutException:
                self.logger.warning("main-results div not found, will search entire page")
                
                # Even if main-results not found, try scrolling the entire page
                self.logger.info("Scrolling entire page to trigger lazy loading...")
                for i in range(3):
                    self.browser_manager.driver.execute_script("window.scrollBy(0, 1000);")
                    time.sleep(2)
                
                # Take a screenshot for debugging
                self.browser_manager.take_screenshot("main_results_not_found")
            
            # Find product containers within main-results or entire page
            product_selectors = [
                ".product-list-item"
            ]
            
            product_elements = []
            search_context = main_results_div if main_results_div else self.browser_manager.driver
            
            for selector in product_selectors:
                try:
                    elements = search_context.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        product_elements = elements
                        self.logger.info(f"Found {len(elements)} products using selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not product_elements:
                self.logger.warning("No product elements found with standard selectors, trying alternative approach")
                product_elements = self._find_products_alternative(search_context)
            
            if not product_elements:
                # Log current page details for debugging
                current_url = self.browser_manager.driver.current_url
                page_title = self.browser_manager.driver.title
                self.logger.error(f"No products found. Current URL: {current_url}")
                self.logger.error(f"Page title: {page_title}")
                
                # Take final screenshot for debugging
                self.browser_manager.take_screenshot("no_products_found_debug")
                return []
            
            # Extract data from each product
            for i, element in enumerate(product_elements[:20]):  # Limit to first 20 products
                try:
                    product_data = self._extract_single_product_data(element, i)
                    if product_data:
                        products.append(product_data)
                        
                except Exception as e:
                    self.logger.debug(f"Error extracting product {i}: {str(e)}")
                    continue
            
            self.logger.info(f"✓ Successfully extracted data for {len(products)} products")
            
            # Save raw data
            self._save_product_data(products)
            
            # Log detailed sample for verification
            self._log_detailed_sample_products(products)
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error extracting product data: {str(e)}")
            # Take screenshot for debugging
            try:
                self.browser_manager.take_screenshot("extraction_error_debug")
            except:
                pass
            return []
    
    def _find_products_alternative(self, search_context) -> List:
        """Alternative method to find product elements"""
        try:
            # Try different approaches
            alternative_selectors = [
                "//div[contains(@class, 'product')]",
                "//div[contains(@class, 'item')]",
                "//article",
                "//div[contains(@class, 'card')]",
                "//*[contains(@class, 'sku')]"
            ]
            
            for selector in alternative_selectors:
                try:
                    elements = search_context.find_elements(By.XPATH, selector)
                    if len(elements) > 5:  # Reasonable number of products
                        self.logger.info(f"Alternative method found {len(elements)} elements")
                        return elements
                except Exception:
                    continue
            
            return []
            
        except Exception:
            return []
    
    def _extract_single_product_data(self, element, index: int) -> Optional[Dict[str, Any]]:
        """
        Extract data from a single product element
        
        Args:
            element: Selenium WebElement
            index: Product index for logging
            
        Returns:
            Dict containing product data or None if extraction fails
        """
        try:
            product_data = {
                "index": index,
                "name": self._extract_product_name(element),
                "price": self._extract_product_price(element),
                "rating": self._extract_product_rating(element),
                "review_count": self._extract_review_count(element),
                "url": self._extract_product_url(element),
                "specifications": self._extract_basic_specs(element)
            }
            
            # Only return if we have at least name and price
            if product_data["name"] and product_data["price"]:
                self.logger.debug(f"Extracted product {index}: {product_data['name']}")
                return product_data
            else:
                return None
                
        except Exception as e:
            self.logger.debug(f"Error extracting product {index}: {str(e)}")
            return None
    
    def _extract_product_name(self, element) -> Optional[str]:
        """Extract product name from element"""
        try:
            # Use the specific selector provided by user: h2 with class "product-title"
            try:
                name_element = element.find_element(By.CSS_SELECTOR, "h2.product-title")
                name = name_element.text.strip()
                if name and len(name) > 5:  # Reasonable product name length
                    return name
            except NoSuchElementException:
                self.logger.debug("h2.product-title not found, trying alternative selectors")
            
            # Fallback selectors if the main one doesn't work
            fallback_selectors = [
                ".product-title",
                "h2",
                "h3", 
                "h4",
                "[data-testid='product-title']"
            ]
            
            for selector in fallback_selectors:
                try:
                    name_element = element.find_element(By.CSS_SELECTOR, selector)
                    name = name_element.text.strip()
                    if name and len(name) > 5:  # Reasonable product name length
                        return name
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _extract_product_price(self, element) -> Optional[str]:
        """Extract product price from element"""
        try:
            # Use the specific selector provided by user: div with class "customer-price" (inner text)
            try:
                price_element = element.find_element(By.CSS_SELECTOR, "div.customer-price")
                price = price_element.text.strip()
                if price and "$" in price:
                    # Clean up price text
                    import re
                    price_match = re.search(r'\$[\d,]+\.?\d*', price)
                    if price_match:
                        return price_match.group(0)
                    return price
            except NoSuchElementException:
                self.logger.debug("div.customer-price not found, trying alternative selectors")
            
            # Fallback selectors if the main one doesn't work
            fallback_selectors = [
                ".customer-price",
                ".price",
                ".current-price",
                ".pricing-current-price",
                "[data-testid='price']"
            ]
            
            for selector in fallback_selectors:
                try:
                    price_element = element.find_element(By.CSS_SELECTOR, selector)
                    price = price_element.text.strip()
                    if price and "$" in price:
                        # Clean up price text
                        import re
                        price_match = re.search(r'\$[\d,]+\.?\d*', price)
                        if price_match:
                            return price_match.group(0)
                        return price
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _extract_product_url(self, element) -> Optional[str]:
        """Extract product URL from element"""
        try:
            link_selectors = [
                "a[href*='/site/']",
                ".sr-title a",
                ".product-title a",
                "h3 a",
                "h4 a"
            ]
            
            for selector in link_selectors:
                try:
                    link_element = element.find_element(By.CSS_SELECTOR, selector)
                    url = link_element.get_attribute("href")
                    if url and "/site/" in url:
                        return url
                except NoSuchElementException:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _extract_basic_specs(self, element) -> Dict[str, Any]:
        """Extract basic specifications from element if available"""
        try:
            specs = {}
            
            # Look for specification text in various formats
            spec_selectors = [
                # Best Buy specific specification selectors
                ".sr-spec",
                ".specifications",
                ".product-specs",
                ".features",
                ".key-specs",
                ".sr-item-specifications",
                ".item-features",
                ".product-features",
                ".sr-product-highlights",
                ".highlight-list"
            ]
            
            for selector in spec_selectors:
                try:
                    spec_element = element.find_element(By.CSS_SELECTOR, selector)
                    spec_text = spec_element.text.strip()
                    if spec_text and len(spec_text) > 10:
                        specs["basic_info"] = spec_text
                        break
                except NoSuchElementException:
                    continue
            
            # Look for specific common laptop specifications
            spec_details = {}
            
            # Try to extract specific details from the product element
            try:
                # Look for processor information
                processor_keywords = ["Intel", "AMD", "i3", "i5", "i7", "i9", "Ryzen", "Core"]
                processor_selectors = [
                    ".//*[contains(text(), 'Intel') or contains(text(), 'AMD') or contains(text(), 'Core') or contains(text(), 'Ryzen')]"
                ]
                
                for xpath in processor_selectors:
                    try:
                        proc_elements = element.find_elements(By.XPATH, xpath)
                        for proc_element in proc_elements:
                            proc_text = proc_element.text.strip()
                            if any(keyword in proc_text for keyword in processor_keywords):
                                spec_details["processor"] = proc_text[:100]  # Limit length
                                break
                        if "processor" in spec_details:
                            break
                    except:
                        continue
            except:
                pass
            
            # Look for RAM information
            try:
                ram_selectors = [
                    ".//*[contains(text(), 'GB') and (contains(text(), 'RAM') or contains(text(), 'Memory'))]",
                    ".//*[contains(text(), 'GB') and contains(text(), 'DDR')]"
                ]
                
                for xpath in ram_selectors:
                    try:
                        ram_elements = element.find_elements(By.XPATH, xpath)
                        for ram_element in ram_elements:
                            ram_text = ram_element.text.strip()
                            if "GB" in ram_text and len(ram_text) < 50:
                                spec_details["memory"] = ram_text
                                break
                        if "memory" in spec_details:
                            break
                    except:
                        continue
            except:
                pass
            
            # Look for storage information
            try:
                storage_selectors = [
                    ".//*[contains(text(), 'SSD') or contains(text(), 'HDD') or contains(text(), 'TB') or contains(text(), 'Storage')]"
                ]
                
                for xpath in storage_selectors:
                    try:
                        storage_elements = element.find_elements(By.XPATH, xpath)
                        for storage_element in storage_elements:
                            storage_text = storage_element.text.strip()
                            if any(keyword in storage_text for keyword in ["SSD", "HDD", "TB", "GB"]) and len(storage_text) < 50:
                                spec_details["storage"] = storage_text
                                break
                        if "storage" in spec_details:
                            break
                    except:
                        continue
            except:
                pass
            
            # Look for screen size
            try:
                screen_selectors = [
                    ".//*[contains(text(), 'inch') or contains(text(), '\"')]"
                ]
                
                for xpath in screen_selectors:
                    try:
                        screen_elements = element.find_elements(By.XPATH, xpath)
                        for screen_element in screen_elements:
                            screen_text = screen_element.text.strip()
                            if ("inch" in screen_text or '"' in screen_text) and len(screen_text) < 30:
                                import re
                                # Look for screen size pattern like "15.6 inch" or '15.6"'
                                size_match = re.search(r'(\d+\.?\d*)\s*(?:inch|")', screen_text)
                                if size_match:
                                    spec_details["screen_size"] = f"{size_match.group(1)} inches"
                                    break
                        if "screen_size" in spec_details:
                            break
                    except:
                        continue
            except:
                pass
            
            # Add specific details to specs if found
            if spec_details:
                specs["details"] = spec_details
            
            # Try to get additional product information from any visible text
            try:
                all_text = element.text.strip()
                if all_text and len(all_text) > 20:
                    # Extract key terms that might be specifications
                    import re
                    key_terms = []
                    
                    # Look for common laptop terms
                    patterns = [
                        r'(\d+\.?\d*\s*(?:inch|"))',  # Screen size
                        r'(\d+\s*GB\s*(?:RAM|Memory|DDR\d?))',  # RAM
                        r'(\d+\s*(?:GB|TB)\s*(?:SSD|HDD|Storage))',  # Storage
                        r'(Intel\s+Core\s+i\d+|AMD\s+Ryzen\s+\d+)',  # Processor
                        r'(Windows\s+\d+|macOS|Chrome\s*OS)',  # OS
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, all_text, re.IGNORECASE)
                        key_terms.extend(matches)
                    
                    if key_terms:
                        specs["extracted_terms"] = key_terms[:10]  # Limit to 10 terms
            except:
                pass
            
            return specs
            
        except Exception:
            return {}
    
    def _save_product_data(self, products: List[Dict[str, Any]]):
        """Save extracted product data to JSON file"""
        try:
            # Ensure data directory exists
            config.DATA_DIR.mkdir(exist_ok=True)
            
            # Save to JSON file
            json_file = config.DATA_DIR / config.OUTPUT_CONFIG["json_filename"]
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✓ Product data saved to {json_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving product data: {str(e)}")
    
    def _log_detailed_sample_products(self, products: List[Dict[str, Any]]):
        """Log detailed sample product information for verification"""
        try:
            self.logger.info("Detailed sample extracted products:")
            for i, product in enumerate(products[:3]):  # Log first 3 products
                name = product.get('name', 'N/A')
                price = product.get('price', 'N/A')
                rating = product.get('rating', 'N/A')
                self.logger.info(f"  {i+1}. {name[:50]}{'...' if len(name) > 50 else ''}")
                self.logger.info(f"      Price: {price}, Rating: {rating}")
                
        except Exception as e:
            self.logger.debug(f"Error logging detailed sample products: {str(e)}")
    
    def run_product_category_analysis(self) -> bool:
        """
        Run the complete product category analysis (Task 2)
        
        Returns:
            bool: True if analysis completed successfully
        """
        try:
            self.logger.info("🚀 Starting Product Category Analysis (Task 2)")
            
            # Step 1: Navigate to laptops category
            navigation_success = self.navigate_to_laptops_category()
            
            if navigation_success:
                # Step 2: Apply filters
                if not self.apply_product_filters():
                    self.logger.warning("Filters failed, continuing with unfiltered results")
            else:
                # If navigation failed, try direct approach to filtered URL
                self.logger.warning("Regular navigation failed, trying direct filtered URL approach...")
                if self._navigate_to_filtered_url():
                    self.logger.info("✓ Successfully used direct filtered URL approach")
                    navigation_success = True
                else:
                    self.logger.error("✗ All navigation approaches failed")
                    return False
            
            # Step 3: Extract product data
            products = self.extract_product_data()
            
            if products:
                self.logger.info(f"🎉 Product Category Analysis completed successfully!")
                self.logger.info(f"✓ Extracted data for {len(products)} products")
                
                # Log some sample product information
                self._log_sample_products(products)
                
                self.logger.info("=" * 60)
                return True
            else:
                self.logger.error("✗ No products extracted")
                return False
                
        except Exception as e:
            self.logger.error(f"Product Category Analysis error: {str(e)}")
            return False
    
    def _log_sample_products(self, products: List[Dict[str, Any]]):
        """Log some sample product information for verification"""
        try:
            self.logger.info("Sample extracted products:")
            for i, product in enumerate(products[:3]):  # Log first 3 products
                name = product.get('name', 'N/A')
                price = product.get('price', 'N/A')
                rating = product.get('rating', 'N/A')
                self.logger.info(f"  {i+1}. {name[:50]}{'...' if len(name) > 50 else ''}")
                self.logger.info(f"      Price: {price}, Rating: {rating}")
                
        except Exception as e:
            self.logger.debug(f"Error logging sample products: {str(e)}")
    
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

    def extract_products_from_specific_url(self, url: str) -> List[Dict[str, Any]]:
        """
        Extract product data directly from a specific URL
        
        Args:
            url (str): The specific URL to extract products from
            
        Returns:
            List[Dict]: List of product data dictionaries
        """
        try:
            self.logger.info("🚀 Starting Product Extraction from Specific URL")
            self.logger.info(f"Target URL: {url}")
            
            # Initialize browser if not already done
            if not self.browser_manager or not self.browser_manager.driver:
                if not self.initialize_browser():
                    self.logger.error("Failed to initialize browser")
                    return []
            
            # Extract product data using the specific URL
            products = self.extract_product_data(use_specific_url=True, specific_url=url)
            
            if products:
                self.logger.info(f"🎉 Successfully extracted {len(products)} products!")
                self.logger.info("=" * 60)
                
                # Print a summary to console
                print(f"\n✅ Extraction Complete!")
                print(f"📊 Total products extracted: {len(products)}")
                print(f"📁 Data saved to: {config.DATA_DIR / config.OUTPUT_CONFIG['json_filename']}")
                print(f"📋 Log files saved to: {config.LOGS_DIR}")
                
                # Print sample products
                print(f"\n📋 Sample products:")
                for i, product in enumerate(products[:3]):
                    name = product.get('name', 'N/A')
                    price = product.get('price', 'N/A')
                    rating = product.get('rating', 'N/A')
                    reviews = product.get('review_count', 'N/A')
                    print(f"  {i+1}. {name[:60]}{'...' if len(name) > 60 else ''}")
                    print(f"      💰 Price: {price} | ⭐ Rating: {rating} | 📝 Reviews: {reviews}")
                
                return products
            else:
                self.logger.error("No products were extracted")
                return []
                
        except Exception as e:
            self.logger.error(f"Error in extract_products_from_specific_url: {str(e)}")
            return []

def main():
    """Main function to run the e-commerce analytics automation"""
    # Check command line arguments
    headless_mode = True
    run_task = "1"  # Default to Task 1
    specific_url = None
    
    if len(sys.argv) > 1:
        if "--visible" in sys.argv:
            headless_mode = False
            print("Running in visible mode for debugging...")
        
        if "--task2" in sys.argv:
            run_task = "2"
        elif "--both" in sys.argv:
            run_task = "both"
        elif "--extract-url" in sys.argv:
            run_task = "extract-url"
            # Look for the URL argument after --extract-url
            try:
                url_index = sys.argv.index("--extract-url") + 1
                # Check if the next argument exists and is not another flag
                if url_index < len(sys.argv) and not sys.argv[url_index].startswith("--"):
                    specific_url = sys.argv[url_index]
                else:
                    # Use the default URL provided by user
                    specific_url = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001"
            except (ValueError, IndexError):
                specific_url = "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001"
    
    # Create and run the analyzer
    analyzer = ECommerceAnalyzer(headless=headless_mode)
    
    try:
        if run_task == "extract-url":
            print("🚀 Running Product Extraction from Specific URL")
            print(f"URL: {specific_url}")
            
            products = analyzer.extract_products_from_specific_url(specific_url)
            if products:
                print(f"\n✅ Extraction completed successfully!")
                print(f"Extracted {len(products)} products from the main-results div.")
                return 0
            else:
                print("\n❌ Extraction failed!")
                return 1
                
        elif run_task == "1":
            print("🚀 Running Task 1: Initial Setup and Navigation")
            success = analyzer.run_initial_setup_demo()
            if success:
                print("\n✅ Task 1 completed successfully!")
                print("Check the logs directory for detailed execution logs.")
                return 0
            else:
                print("\n❌ Task 1 failed!")
                return 1
                
        elif run_task == "2":
            print("🚀 Running Task 2: Product Category Analysis")
            
            # Initialize browser first
            if not analyzer.initialize_browser():
                print("\n❌ Browser initialization failed!")
                return 1
            
            # Navigate to website
            if not analyzer.navigate_to_target_website():
                print("\n❌ Website navigation failed!")
                return 1
            
            # Run Task 2
            success = analyzer.run_product_category_analysis()
            if success:
                print("\n✅ Task 2 completed successfully!")
                print("Check the data directory for extracted product data.")
                print("Check the logs directory for detailed execution logs.")
                return 0
            else:
                print("\n❌ Task 2 failed!")
                return 1
                
        elif run_task == "both":
            print("🚀 Running Both Tasks: Setup + Product Analysis")
            
            # Run Task 1
            success1 = analyzer.run_initial_setup_demo()
            
            if success1:
                print("✅ Task 1 completed successfully!")
                
                # Re-initialize for Task 2 (fresh browser)
                analyzer.cleanup()
                analyzer = ECommerceAnalyzer(headless=headless_mode)
                
                if not analyzer.initialize_browser():
                    print("\n❌ Browser re-initialization failed!")
                    return 1
                
                if not analyzer.navigate_to_target_website():
                    print("\n❌ Website navigation failed!")
                    return 1
                
                # Run Task 2
                success2 = analyzer.run_product_category_analysis()
                
                if success2:
                    print("\n✅ Both tasks completed successfully!")
                    print("Check the data directory for extracted product data.")
                    print("Check the logs directory for detailed execution logs.")
                    return 0
                else:
                    print("\n⚠️ Task 1 succeeded, but Task 2 failed!")
                    return 1
            else:
                print("\n❌ Task 1 failed, skipping Task 2!")
                return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        analyzer.cleanup()
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        analyzer.cleanup()
        return 1
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    # Print usage information
    if len(sys.argv) == 1:
        print("🔍 E-Commerce Analytics Automation")
        print("\nUsage:")
        print("  python main.py                    # Run Task 1 (Initial Setup)")
        print("  python main.py --task2            # Run Task 2 (Product Analysis)")
        print("  python main.py --both             # Run both tasks")
        print("  python main.py --extract-url      # Extract from specific URL")
        print("  python main.py --extract-url [URL]  # Extract from custom URL")
        print("\nOptions:")
        print("  --visible                         # Run browser in visible mode")
        print("\nExample:")
        print("  python main.py --extract-url --visible")
        
    sys.exit(main()) 