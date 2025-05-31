# E-Commerce Analytics Automation

## Overview
This project implements an automated system to analyze product data and customer reviews from e-commerce platforms, starting with Best Buy. The current implementation focuses on **Task 1: Initial Setup and Navigation**.

## Features Implemented (Task 1)
- ✅ **Chrome Browser Setup**: Launches Chrome in headless mode with optimized settings
- ✅ **Website Navigation**: Navigates to bestbuy.com with robust error handling
- ✅ **Robust Wait Strategies**: Implements multiple wait strategies for dynamic elements:
  - Implicit waits for all element lookups
  - Explicit waits for specific conditions
  - Page load waits with document ready state checking
  - Dynamic content wait strategies

## Project Structure
```
/project
    /data/          # Data storage directory
    /logs/          # Application logs and screenshots
    /tests/         # Unit tests (to be implemented)
    /reports/       # Generated reports (to be implemented)
    main.py         # Main application entry point
    config.py       # Configuration settings
    browser_utils.py # Browser management utilities
    requirements.txt # Python dependencies
    README.md       # This file
    chromedriver    # Chrome WebDriver executable
```

## Prerequisites
- Python 3.11
- Google Chrome browser
- ChromeDriver (included in project)

## Setup Instructions

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd assesment

# Or extract from zip file
unzip project.zip
cd project
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify ChromeDriver
The project includes a ChromeDriver executable. Ensure it has execute permissions:
```bash
# On macOS/Linux:
chmod +x chromedriver
```

## Usage

### Run Initial Setup and Navigation Demo
```bash
# Run in headless mode (default)
python main.py

# Run in visible mode for debugging
python main.py --visible
```

### Expected Output
The application will:
1. Initialize Chrome browser in headless mode
2. Navigate to bestbuy.com
3. Verify successful page load
4. Demonstrate various wait strategies
5. Generate logs and screenshots in the `logs/` directory

### Logs and Screenshots
- **Log file**: `logs/ecommerce_analytics.log`
- **Screenshots**: `logs/successful_navigation.png` (on success)
- **Debug screenshots**: `logs/page_verification_failed.png` (if needed)

## Configuration

The project uses a centralized configuration system in `config.py`:

### Browser Settings
- Headless mode enabled by default
- Window size: 1920x1080
- Optimized Chrome options for automation
- Anti-detection measures

### Wait Configuration
- Implicit wait: 10 seconds
- Explicit wait: 20 seconds
- Page load timeout: 30 seconds
- Rate limiting delays: 1-3 seconds

### Website Configuration
- Target URL: https://www.bestbuy.com
- Predefined selectors for common elements
- Fallback verification strategies

## Error Handling

The application implements comprehensive error handling:
- **Network Issues**: Timeout handling and retry logic
- **Missing Elements**: Graceful fallbacks and alternative selectors
- **Rate Limiting**: Human-like delays and request spacing
- **Browser Issues**: Clean shutdown and resource management

## Logging

Detailed logging is implemented with:
- **File Logging**: All activities logged to `logs/ecommerce_analytics.log`
- **Console Output**: Real-time progress updates
- **Screenshot Capture**: Visual debugging for failed operations
- **Multiple Log Levels**: INFO, WARNING, ERROR, DEBUG

## Technical Implementation

### BrowserManager Class
- Robust Chrome browser setup with anti-detection
- Multiple wait strategy implementations
- Safe element interaction methods
- Screenshot and debugging capabilities
- Context manager support for resource cleanup

### ECommerceAnalyzer Class
- Main application orchestration
- Task-specific implementations
- Comprehensive testing and verification
- Modular design for future enhancements

## Next Steps (Future Tasks)

This implementation provides the foundation for:
- Task 2: Product Category Analysis
- Task 3: Advanced Data Collection
- Task 4: Data Processing and Analysis
- Task 5: Automated Report Generation
- Task 6: Data Visualization Dashboard
- Task 7: Error Handling and Logging (Enhanced)

## Troubleshooting

### Common Issues

1. **ChromeDriver Not Found**
   ```
   Error: ChromeDriver not found at ./chromedriver
   ```
   **Solution**: Ensure chromedriver file exists and has execute permissions

2. **Network Timeout**
   ```
   Error: Timeout while navigating to URL
   ```
   **Solution**: Check internet connection and website availability

3. **Element Not Found**
   ```
   Warning: Element not found within timeout
   ```
   **Solution**: Website structure may have changed; check logs for details

4. **Permission Denied**
   ```
   Error: Permission denied accessing chromedriver
   ```
   **Solution**: Run `chmod +x chromedriver` on macOS/Linux

### Debug Mode
Run with `--visible` flag to see browser actions:
```bash
python main.py --visible
```

## Code Quality Features

- **Type Hints**: Full type annotation for better code maintainability
- **Error Handling**: Comprehensive exception handling with logging
- **Documentation**: Detailed docstrings and inline comments
- **Modular Design**: Separated concerns with dedicated utility classes
- **Configuration Management**: Centralized configuration system
- **Resource Management**: Context managers for proper cleanup

## Dependencies

- `selenium==4.33.0` - Web automation framework
- `pandas==2.1.3` - Data manipulation (for future tasks)
- `numpy==1.25.2` - Numerical computing (for future tasks)
- `openpyxl==3.1.2` - Excel file handling (for future tasks)
- `matplotlib==3.8.2` - Plotting library (for future tasks)
- `plotly==5.17.0` - Interactive visualizations (for future tasks)
- Additional dependencies for future enhancements

## License

This project is for educational and assessment purposes.

## Support

For issues or questions:
1. Check the logs in `logs/ecommerce_analytics.log`
2. Run in visible mode (`--visible`) for debugging
3. Review the troubleshooting section above 