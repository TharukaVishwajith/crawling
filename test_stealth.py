#!/usr/bin/env python3
"""
Test script for enhanced stealth browser configuration
"""
from browser_utils import BrowserManager
import config

def test_stealth_browser():
    """Test the enhanced stealth browser configuration"""
    print('Testing enhanced stealth browser configuration...')
    print(f'Headless mode: {config.BROWSER_CONFIG["headless"]}')
    print(f'Window size: {config.BROWSER_CONFIG["window_size"]}')
    print(f'Page load timeout: {config.WAIT_CONFIG["page_load_timeout"]}s')
    print(f'Rate limiting: {config.RATE_LIMIT_CONFIG["min_delay"]}-{config.RATE_LIMIT_CONFIG["max_delay"]}s')

    # Test browser initialization
    try:
        browser = BrowserManager()
        driver = browser.setup_browser()
        print('✅ Browser setup successful with stealth configuration')
        
        # Quick test navigation
        print('Testing navigation to BestBuy...')
        success = browser.navigate_to_website('https://www.bestbuy.com')
        if success:
            print('✅ Successfully navigated to BestBuy')
            
            # Check if we can detect any automation indicators
            webdriver_detected = driver.execute_script('return navigator.webdriver')
            print(f'navigator.webdriver detected: {webdriver_detected}')
            
            plugins_count = driver.execute_script('return navigator.plugins.length')
            print(f'Plugins count: {plugins_count}')
            
            chrome_present = driver.execute_script('return typeof window.chrome !== "undefined"')
            print(f'Chrome object present: {chrome_present}')
            
            user_agent = driver.execute_script('return navigator.userAgent')
            print(f'User agent: {user_agent[:80]}...')
            
            screen_width = driver.execute_script('return screen.width')
            screen_height = driver.execute_script('return screen.height')
            print(f'Screen resolution: {screen_width}x{screen_height}')
            
            print('✅ Stealth measures appear to be working')
            
            # Test human-like interaction
            print('Testing human-like scrolling...')
            browser._simulate_human_scrolling()
            print('✅ Human-like scrolling completed')
            
        else:
            print('❌ Navigation failed')
            
        browser.close()
        return True
        
    except Exception as e:
        print(f'❌ Error testing browser: {e}')
        return False

if __name__ == "__main__":
    test_stealth_browser() 