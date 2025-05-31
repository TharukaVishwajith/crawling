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
    "headless": True,
    "window_size": (1920, 1080),
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "chrome_options": [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-popup-blocking",
        "--disable-notifications",
        "--disable-web-security",
        "--allow-running-insecure-content",
        "--disable-blink-features=AutomationControlled"
    ]
}

# Wait configuration
WAIT_CONFIG = {
    "implicit_wait": 10,
    "explicit_wait": 20,
    "page_load_timeout": 30,
    "script_timeout": 30
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    "min_delay": 1,
    "max_delay": 3,
    "request_delay": 2,
    "page_load_delay": 3
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