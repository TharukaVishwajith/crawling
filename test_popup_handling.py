#!/usr/bin/env python3
"""
Test script for popup handling functionality
"""
from browser_utils import BrowserManager
import config
import time

def test_popup_handling():
    """Test the popup handling functionality"""
    print('Testing popup handling functionality...')
    
    try:
        browser = BrowserManager()
        driver = browser.setup_browser()
        print('✅ Browser setup successful')
        
        # Test navigation with popup handling
        print('Testing navigation to BestBuy product page with popup handling...')
        
        # Navigate to a product page that might trigger login popup
        product_url = "https://www.bestbuy.com/site/laptops/abcat0502000.c?id=abcat0502000"
        success = browser.safe_navigate_with_popup_handling(product_url)
        
        if success:
            print('✅ Successfully navigated with popup handling')
            
            # Simulate some page interactions that might trigger popups
            print('Simulating page interactions that might trigger popups...')
            
            # Scroll around to trigger any delayed popups
            browser._simulate_human_scrolling()
            
            # Monitor for popups for 10 seconds
            print('Monitoring for popups for 10 seconds...')
            browser.monitor_and_dismiss_popups(duration=10)
            
            # Try to manually trigger popup check
            print('Manual popup check...')
            popup_found = browser.handle_login_popup()
            if popup_found:
                print('✅ Popup detected and handled')
            else:
                print('ℹ️  No popup detected')
            
            # Test JavaScript alert handling
            print('Testing JavaScript alert handling...')
            try:
                # Create a test alert (this might not work on all sites due to security)
                driver.execute_script("setTimeout(function() { alert('Test alert'); }, 1000);")
                time.sleep(2)
                alert_handled = browser._handle_javascript_alert()
                if alert_handled:
                    print('✅ JavaScript alert handled')
                else:
                    print('ℹ️  No JavaScript alert to handle')
            except Exception as e:
                print(f'ℹ️  JavaScript alert test skipped: {e}')
            
        else:
            print('❌ Navigation with popup handling failed')
        
        print('Taking screenshot for verification...')
        browser.take_screenshot('popup_test_result')
        
        browser.close()
        return True
        
    except Exception as e:
        print(f'❌ Error testing popup handling: {e}')
        return False

def test_specific_popup_selectors():
    """Test specific popup selector patterns"""
    print('\nTesting specific popup selector patterns...')
    
    try:
        browser = BrowserManager()
        driver = browser.setup_browser()
        
        # Navigate to BestBuy
        browser.navigate_to_website("https://www.bestbuy.com")
        
        # Test various popup detection methods
        print('Testing modal popup detection...')
        
        # Check for common modal indicators
        modal_indicators = [
            '[role="dialog"]',
            '[aria-modal="true"]',
            '.modal',
            '.popup',
            '.overlay'
        ]
        
        for indicator in modal_indicators:
            try:
                from selenium.webdriver.common.by import By
                elements = driver.find_elements(By.CSS_SELECTOR, indicator)
                if elements:
                    print(f'Found {len(elements)} elements with selector: {indicator}')
                    for element in elements:
                        if element.is_displayed():
                            print(f'  - Visible element: {element.tag_name}')
            except Exception as e:
                print(f'Error checking {indicator}: {e}')
        
        browser.close()
        return True
        
    except Exception as e:
        print(f'❌ Error testing popup selectors: {e}')
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("POPUP HANDLING TEST SUITE")
    print("=" * 60)
    
    # Test main popup handling
    test_popup_handling()
    
    # Test specific selectors
    test_specific_popup_selectors()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60) 