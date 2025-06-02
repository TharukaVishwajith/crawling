"""
Configuration settings for E-Commerce Analytics Automation
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
TESTS_DIR = PROJECT_ROOT / "tests"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Browser configuration
BROWSER_CONFIG = {
    "headless": False,
    "window_size": (1366, 768),
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "chrome_options": [
        # --- Core stability flags ---
        "--no-sandbox",
        "--disable-dev-shm-usage",
        
        # --- Advanced stealth flags ---
        "--disable-blink-features=AutomationControlled",
        "--disable-automation",
        "--disable-infobars",
        "--disable-extensions-file-access-check",
        "--disable-extensions-http-throttling",
        "--disable-extensions-https-throttling",
        
        # --- Performance optimization flags ---
        "--aggressive-cache-discard",
        "--memory-pressure-off",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",
        "--disable-client-side-phishing-detection",
        "--disable-crash-reporter",
        "--disable-oopr-debug-crash-dump",
        "--no-crash-upload",
        "--disable-low-res-tiling",
        "--max_old_space_size=4096",
        
        # --- Network optimization ---
        "--aggressive-tab-discard",
        "--enable-tcp-fast-open",
        "--enable-experimental-web-platform-features",
        
        # --- Keep essential blocking for performance ---
        "--disable-background-networking",
        "--disable-notifications",
        "--disable-popup-blocking",
        "--disable-translate",
        "--disable-ipc-flooding-protection",
        
        # --- Additional stealth flags ---
        "--disable-features=VizDisplayCompositor",
        "--disable-features=TranslateUI",
        "--disable-component-extensions-with-background-pages",
        "--disable-default-apps",
        "--mute-audio",
        
        # --- Override automation detection ---
        "--disable-web-security",
        "--allow-running-insecure-content",
        
        # --- Browser fingerprint randomization ---
        "--enable-features=NetworkService,NetworkServiceLogging",
        "--disable-features=VizDisplayCompositor,VizServiceDisplay",
    ]
}

# Enhanced wait configuration for better stealth
WAIT_CONFIG = {
    "implicit_wait": 8,
    "explicit_wait": 25,
    "page_load_timeout": 45,
    "script_timeout": 30
}

# Enhanced rate limiting for more human-like behavior
RATE_LIMIT_CONFIG = {
    "min_delay": 2,
    "max_delay": 5,
    "request_delay": 3,
    "page_load_delay": 4,
    "human_typing_delay": (0.1, 0.3),
    "mouse_movement_delay": (0.5, 1.2),
}

# Target website configuration
WEBSITE_CONFIG = {
    "base_url": "https://www.bestbuy.com",
    "laptops_category_url": "https://www.bestbuy.com/site/computers-pcs/laptops/abcat0502000.c?id=abcat0502000",
    "search_selectors": {
        "search_box": 'input[data-testid="search-input"]',
        "search_button": 'button[data-testid="search-button"]',
        "product_cards": '.list-item',
        "product_title": '.sr-title',
        "product_price": '.sr-price',
        "product_rating": '.sr-rating',
        "next_page": '.page-next'
    }
}

# Filter configuration for product search
FILTER_CONFIG = {
    "price_range": {
        "min": 500,
        "max": 1500
    },
    "brands": ["Apple", "Dell", "HP", "Lenovo", "ASUS"],
    "min_rating": 4.0
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_name": "ecommerce_analytics.log"
}

# Output configuration
OUTPUT_CONFIG = {
    "excel_filename": "product_analysis.xlsx",
    "json_filename": "raw_product_data.json",
    "pdf_report_filename": "ecommerce_analytics_report.pdf",
    "dashboard_filename": "analytics_dashboard.html"
} 