# E-Commerce Analytics Automation

## 🎯 Overview

This project provides a comprehensive automated system to analyze product data and customer reviews from e-commerce platforms. It includes web scraping, data processing, sentiment analysis, report generation, and interactive dashboard creation.

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
├── analytics_pipeline.py          # 🚀 Main pipeline orchestrator
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

### 2. Run Complete Analytics Pipeline

```bash
# Run all components (data processing, PDF report, dashboard)
python analytics_pipeline.py --mode all

# Run specific components
python analytics_pipeline.py --mode data      # Data processing only
python analytics_pipeline.py --mode report    # PDF report only
python analytics_pipeline.py --mode dashboard # Dashboard only
```

### 3. Run Individual Modules

```bash
# Data processing and analysis
python data_processor.py

# PDF report generation
python report_generator.py

# Interactive dashboard creation
python dashboard_generator.py

# Web scraping (original functionality)
python main.py
```

## 📊 Components Overview

### 1. Data Processing (`data_processor.py`)

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

### 2. Report Generation (`report_generator.py`)

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

### 3. Dashboard Generator (`dashboard_generator.py`)

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

### 4. Analytics Pipeline (`analytics_pipeline.py`)

**Features:**
- Orchestrates the complete analytics workflow
- Modular execution (run individual components or complete pipeline)
- Comprehensive logging with timestamps
- Error handling and graceful degradation
- Command-line interface with argument parsing

**Usage:**
```bash
python analytics_pipeline.py [OPTIONS]

Options:
  --mode {all,data,report,dashboard}  Which component to run (default: all)
  --data-file FILE                   Specific data file to process
  --config FILE                      Configuration file path
```

## 📈 Generated Reports

### 1. Excel Report (`Product_Analysis.xlsx`)
- **Sheet 1**: Product summary with conditional formatting and data validation
- **Sheet 2**: Specifications comparison with unique feature highlighting
- **Sheet 3**: Review analysis with sentiment scores and aggregations

### 2. PDF Report (`E-Commerce_Analysis_Report.pdf`)
- Executive summary with key insights
- Price trend analysis charts
- Sentiment analysis visualizations
- Brand competitive analysis
- Top product recommendations table

### 3. Interactive Dashboard (`analytics_dashboard.html`)
- Modern, responsive web interface
- Interactive Plotly charts with hover details
- Summary statistics cards
- Professional styling with gradients and shadows

### 4. Visualization Charts (PNG files)
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

## 🧪 Testing

```bash
# Run individual module tests
python data_processor.py      # Test data processing
python report_generator.py    # Test PDF report generation
python dashboard_generator.py # Test dashboard creation

# Run the test suite (if available)
python -m pytest tests/
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

### Custom Data Processing

```python
from data_processor import DataProcessor

# Initialize processor
processor = DataProcessor()

# Process custom data file
processor.process_all_data("custom_data.json")

# Individual operations
data = processor.load_product_data("custom_data.json")
df_products, pivot_brand = processor.create_product_summary(data)
df_reviews, agg = processor.analyze_reviews(data)
```

### Custom Report Generation

```python
from report_generator import ReportGenerator
from data_processor import DataProcessor

# Load data
processor = DataProcessor()
data = processor.load_product_data()
df_products, pivot_brand = processor.create_product_summary(data)
df_reviews, agg = processor.analyze_reviews(data)

# Generate custom report
generator = ReportGenerator()
pdf_path = generator.generate_pdf_report(df_products, pivot_brand, df_reviews, agg)
```

### Custom Dashboard Creation

```python
from dashboard_generator import DashboardGenerator
from data_processor import DataProcessor

# Load data
processor = DataProcessor()
data = processor.load_product_data()
df_products, pivot_brand = processor.create_product_summary(data)
df_reviews, agg = processor.analyze_reviews(data)

# Generate dashboard
generator = DashboardGenerator()
dashboard_path = generator.generate_dashboard(df_products, pivot_brand, df_reviews, agg)
```

## 📋 Assessment Requirements Completion

### ✅ Section 4: Data Processing and Analysis
- **Complete**: Excel workbook with multiple sheets, conditional formatting, pivot tables, sentiment analysis, visualizations

### ✅ Section 5: Automated Report Generation  
- **Complete**: PDF report with executive summary, price trends, sentiment analysis, competitive analysis, recommendations

### ✅ Section 6: Data Visualization Dashboard
- **Complete**: Interactive HTML dashboard with Plotly charts, modern UI, responsive design

### 🔄 Integration Features
- **Modular Architecture**: Clean separation of concerns
- **Error Handling**: Comprehensive error handling and logging
- **Synthetic Data**: Fallback data for testing when real data unavailable
- **Configuration Management**: Centralized configuration system
- **Command-line Interface**: Easy execution with different modes

## 🚨 Troubleshooting

### Common Issues

1. **NLTK Data Missing**: Run `python -c "import nltk; nltk.download('vader_lexicon')"`
2. **Empty Data File**: The system will automatically use synthetic data for demonstration
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **Permission Errors**: Ensure write permissions for `reports/` and `logs/` directories

### Log Files

Check the `logs/` directory for detailed execution logs:
- `analytics_pipeline_YYYYMMDD_HHMMSS.log`: Main pipeline logs
- Individual module logs are also available

## 👥 Contributing

1. Follow the existing code structure and naming conventions
2. Add comprehensive error handling and logging
3. Update this README when adding new features
4. Add unit tests for new functionality

## 📄 License

This project is part of the E-Commerce Analytics Assessment and follows the requirements specified in `assessment.md`.

---

**Generated Reports Location**: `reports/` directory  
**Logs Location**: `logs/` directory  
**Configuration**: `config.py`  
**Main Entry Point**: `analytics_pipeline.py`