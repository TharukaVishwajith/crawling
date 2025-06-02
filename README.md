# E-Commerce Analytics Automation

## 🎯 Overview

This project provides a comprehensive automated system to analyze product data and customer reviews from e-commerce platforms. It includes **web scraping with extraction**, data processing, sentiment analysis, report generation, and interactive dashboard creation with robust fallback mechanisms.

## 📁 Project Structure

```
/project
├── data/                           # Data storage directory
│   └── raw_product_data.json      # Collected product data
├── logs/                          # Application logs
├── reports/                       # Generated reports and visualizations
│   ├── Product_Analysis.xlsx      # Excel report with multiple sheets
│   ├── E-Commerce_Analysis_Report.pdf  # Comprehensive PDF report
│   ├── analytics_dashboard.html   # Interactive HTML dashboard
│   └── *.png                     # Visualization charts
├── tests/                         # Unit tests
├── main.py                        # Main scraping application
├── browser_utils.py               # Browser automation utilities
├── data_processor.py              # 📊 Data processing and analysis module
├── report_generator.py            # 📋 PDF report generation module
├── dashboard_generator.py         # 📈 Interactive dashboard creation module
├── analytics_pipeline.py          # 🚀 Main pipeline orchestrator with extraction
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone/navigate to the project directory
cd /path/to/your/project

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Complete Pipeline with Product Extraction

```bash
# 🔥 NEW: Run complete pipeline including product extraction
python analytics_pipeline.py --mode full

# Run with specific extraction URL
python analytics_pipeline.py --mode full --extraction-url "https://www.bestbuy.com/site/searchpage.jsp..."

# Run in visible browser mode for debugging
python analytics_pipeline.py --mode full --visible

# Extract products only (no analytics)
python analytics_pipeline.py --mode extract

# Run analytics only (skip extraction, use existing data)
python analytics_pipeline.py --mode all
```

## 🚀 Usage Examples

### Run Complete Assessment Pipeline
```bash
# Execute all sections (4, 5, 6) in sequence
python analytics_pipeline.py --mode all
```

### Run Individual Sections
```bash
# Section 4: Data Processing and Analysis
python analytics_pipeline.py --mode data
python data_processor.py  # Direct execution

# Section 5: Automated Report Generation
python analytics_pipeline.py --mode report
python report_generator.py  # Direct execution

# Section 6: Data Visualization Dashboard
python analytics_pipeline.py --mode dashboard
python dashboard_generator.py  # Direct execution
```

### Custom Data Processing
```bash
# Process specific data file
python analytics_pipeline.py --mode all --data-file custom_data.json
```

## 🛒 **NEW: Integrated Product Extraction with Fallback**

### Enhanced Pipeline Features

The analytics pipeline now includes **comprehensive product extraction** with multiple fallback strategies:

#### 🎯 **Multi-Strategy Extraction Process**

1. **Strategy 1: Specific URL Extraction**
   - Extracts from user-provided URL
   - Handles country selection automatically
   - Implements lazy-loading scroll techniques

2. **Strategy 2: Full Category Analysis**
   - Navigates to laptop category
   - Applies price/brand/rating filters
   - Performs complete product analysis

3. **Strategy 3: Fallback URL Attempts**
   - Tries multiple Best Buy laptop URLs
   - Automatic URL rotation on failure
   - Progressive degradation approach

#### 🛡️ **Robust Fallback Mechanism**

- **Data Age Check**: Uses existing data if recent (< 24 hours)
- **Graceful Degradation**: Falls back to older data if extraction fails
- **Pipeline Stoppage**: Stops execution only if no data available
- **Error Recovery**: Comprehensive error handling with detailed logging

#### 🔧 **Smart Data Management**

```bash
# Extraction saves data to: data/raw_product_data.json
# Pipeline checks data age and freshness
# Automatic fallback to existing data when needed
```

### Usage Examples

```bash
# Complete pipeline with fresh extraction
python analytics_pipeline.py --mode full

# Extract from specific URL with visible browser
python analytics_pipeline.py --mode full --extraction-url "YOUR_URL" --visible

# Skip extraction, use existing data
python analytics_pipeline.py --mode all --data-file raw_product_data.json

# Extract products only (debugging)
python analytics_pipeline.py --mode extract --visible
```

## 📊 Components Overview

### 1. **Product Extraction** (`main.py` integration)

**Features:**
- **Multi-strategy extraction** with comprehensive fallback
- **Lazy-loading support** with automatic scrolling
- **Country selection handling** for Best Buy
- **Rate limiting** and respectful crawling
- **Robust element detection** with multiple selector fallbacks

**Key Integration Methods:**
- `extract_products_with_fallback()`: Main extraction orchestrator
- `_initialize_extractor()`: Browser setup with error handling
- `run_complete_analysis_with_extraction()`: Full pipeline entry point

### 2. Data Processing (`data_processor.py`)

**Features:**
- Loads product and review data from JSON files
- Performs sentiment analysis on customer reviews using NLTK VADER
- Creates Excel reports with multiple sheets:
  - **Product Summary**: Product details with conditional formatting
  - **Specifications Comparison**: Side-by-side product comparison
  - **Review Analysis**: Sentiment analysis results and aggregations
- Generates visualization charts (PNG format)
- Handles synthetic data for testing when real data is unavailable

**Key Methods:**
- `load_product_data()`: Load and validate product data
- `create_product_summary()`: Generate product DataFrames and brand analysis
- `analyze_reviews()`: Perform sentiment analysis on reviews
- `create_visualizations()`: Generate PNG charts
- `save_excel_report()`: Create comprehensive Excel workbook

### 3. Report Generation (`report_generator.py`)

**Features:**
- Creates comprehensive PDF reports using matplotlib
- Includes multiple analysis sections:
  - **Executive Summary**: Key findings and dataset overview
  - **Price Trend Analysis**: Price distribution and trends by brand
  - **Sentiment Analysis**: Review sentiment visualizations
  - **Competitive Analysis**: Brand comparison metrics
  - **Product Recommendations**: Top-rated products table

**Key Methods:**
- `generate_pdf_report()`: Main report generation method
- `create_price_trend_analysis()`: Price-focused charts
- `create_sentiment_analysis_section()`: Sentiment visualizations
- `create_competitive_analysis()`: Brand comparison charts
- `create_recommendations()`: Product recommendation table

### 4. Dashboard Generator (`dashboard_generator.py`)

**Features:**
- Creates interactive HTML dashboards using Plotly
- Responsive design with modern CSS styling
- Interactive charts include:
  - **Price Comparison**: Box plots with hover details
  - **Sentiment Trends**: Scatter plots by product and brand
  - **Brand Performance**: Grouped bar charts with multiple metrics
  - **Sentiment Distribution**: Interactive pie charts
- Summary statistics dashboard header

**Key Methods:**
- `create_price_comparison_chart()`: Interactive price box plots
- `create_sentiment_trends_chart()`: Sentiment scatter plots
- `create_brand_performance_chart()`: Multi-metric brand analysis
- `create_comprehensive_dashboard()`: Complete HTML dashboard

### 5. **Enhanced Analytics Pipeline** (`analytics_pipeline.py`)

**Features:**
- **Integrated extraction pipeline** with fallback strategies
- **Modular execution** (run individual components or complete pipeline)
- **Comprehensive logging** with timestamps and detailed error tracking
- **Error handling** and graceful degradation
- **Smart data management** with age checking and fallback
- **Command-line interface** with extensive options

**Usage Options:**
```bash
python analytics_pipeline.py [OPTIONS]

Options:
  --mode {full,all,extract,data,report,dashboard}  Component to run (default: full)
  --data-file FILE                                 Specific data file to process
  --extraction-url URL                             URL to extract products from
  --visible                                        Run browser in visible mode
  --config FILE                                    Configuration file path
```

## 📈 Generated Reports

### 1. **Product Data** (`data/raw_product_data.json`)
- **Fresh extraction results** with comprehensive product information
- **Structured JSON format** with name, price, rating, specs, reviews
- **Automatic saving** after successful extraction

### 2. Excel Report (`Product_Analysis.xlsx`)
- **Sheet 1**: Product summary with conditional formatting and data validation
- **Sheet 2**: Specifications comparison with unique feature highlighting
- **Sheet 3**: Review analysis with sentiment scores and aggregations

### 3. PDF Report (`E-Commerce_Analysis_Report.pdf`)
- Executive summary with key insights
- Price trend analysis charts
- Sentiment analysis visualizations
- Brand competitive analysis
- Top product recommendations table

### 4. Interactive Dashboard (`analytics_dashboard.html`)
- Modern, responsive web interface
- Interactive Plotly charts with hover details
- Summary statistics cards
- Professional styling with gradients and shadows

### 5. Visualization Charts (PNG files)
- `sentiment_distribution.png`: Pie chart of sentiment categories
- `sentiment_by_brand.png`: Bar chart of average sentiment by brand
- `sentiment_vs_reviews.png`: Scatter plot of review count vs sentiment

## 🛠️ Configuration

The `config.py` file contains all configuration settings:

- **Browser settings**: Headless mode, window size, Chrome options
- **Wait configurations**: Timeouts and delays
- **Rate limiting**: Request delays and page load timing
- **Website configuration**: URLs and CSS selectors
- **Filter settings**: Price ranges, brands, ratings
- **Output settings**: File names and paths

## 🛡️ **Fallback & Error Handling**

### **Extraction Fallback Chain**
1. ✅ **Fresh Data Check**: Use recent data (< 24 hours) if available
2. 🎯 **Strategy 1**: Extract from specific URL (if provided)
3. 🎯 **Strategy 2**: Full product category analysis
4. 🎯 **Strategy 3**: Try multiple fallback URLs
5. 📁 **Data Fallback**: Use existing data file (any age)
6. ❌ **Pipeline Stop**: Stop if no data available

### **Error Recovery**
- **Comprehensive logging** with detailed error tracking
- **Graceful degradation** - continue with available data
- **Resource cleanup** - proper browser closure
- **User guidance** - helpful error messages and suggestions

## 🧪 Testing

```bash
# Test individual components
python analytics_pipeline.py --mode extract --visible    # Test extraction
python analytics_pipeline.py --mode data                 # Test data processing
python analytics_pipeline.py --mode report               # Test PDF report
python analytics_pipeline.py --mode dashboard            # Test dashboard

# Test complete pipeline
python analytics_pipeline.py --mode full --visible       # Full pipeline test
```

## 📦 Dependencies

Key Python packages:
- **selenium**: Web scraping and browser automation
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Static visualizations and PDF generation
- **seaborn**: Statistical visualizations
- **plotly**: Interactive visualizations and dashboards
- **nltk**: Natural language processing for sentiment analysis
- **openpyxl/xlsxwriter**: Excel file generation
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests

## 🔧 Advanced Usage

### **Custom Extraction with Analytics**

```python
from analytics_pipeline import AnalyticsPipeline

# Initialize pipeline
pipeline = AnalyticsPipeline()

# Run extraction with custom URL
success = pipeline.run_complete_analysis_with_extraction(
    extraction_url="https://www.bestbuy.com/site/searchpage.jsp?...",
    headless=False  # Visible mode for debugging
)
```

### **Analytics Without Extraction**

```python
# Run analytics on existing data
pipeline = AnalyticsPipeline()
success = pipeline.run_complete_analysis(data_filename="custom_data.json")
```

### **Extraction Only Mode**

```python
# Extract products without running analytics
pipeline = AnalyticsPipeline()
success = pipeline.extract_products_with_fallback(
    extraction_url="https://www.bestbuy.com/site/...",
    headless=True
)
```

## 🚨 Troubleshooting

### Common Issues

1. **NLTK Data Missing**: Run `python -c "import nltk; nltk.download('vader_lexicon')"`
2. **Extraction Failures**: Use `--visible` flag to debug browser issues
3. **No Products Found**: Check URL and page structure, try fallback mode
4. **Permission Errors**: Ensure write permissions for `data/`, `reports/`, and `logs/` directories
5. **Browser Issues**: Update Chrome browser and ChromeDriver

### **Extraction Troubleshooting**

```bash
# Debug extraction with visible browser
python analytics_pipeline.py --mode extract --visible

# Test specific URL extraction
python analytics_pipeline.py --mode extract --extraction-url "YOUR_URL" --visible

# Check logs for detailed error information
cat logs/analytics_pipeline_*.log
```

### Log Files

Check the `logs/` directory for detailed execution logs:
- `analytics_pipeline_YYYYMMDD_HHMMSS.log`: Main pipeline logs with extraction details
- Individual module logs are also available

## 👥 Contributing

1. Follow the existing code structure and naming conventions
2. Add comprehensive error handling and logging
3. Update this README when adding new features
4. Add unit tests for new functionality
5. Test extraction fallback mechanisms

## 📄 License

This project is part of the E-Commerce Analytics Assessment and follows the requirements specified in `assessment.md`.

---

**NEW FEATURES:**  
🛒 **Integrated Product Extraction** | 🛡️ **Robust Fallback System** | 🔧 **Smart Data Management**  

**Generated Reports Location**: `reports/` directory  
**Extracted Data Location**: `data/` directory  
**Logs Location**: `logs/` directory  
**Configuration**: `config.py`  
**Main Entry Point**: `analytics_pipeline.py --mode full`