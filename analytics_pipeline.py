"""
E-Commerce Analytics Pipeline

This module orchestrates the complete analytics workflow, integrating
data extraction, processing, report generation, and dashboard creation.

Author: Assessment Solution
Date: 2024
"""

import logging
from pathlib import Path
import sys
from datetime import datetime

# Import custom modules
from data_processor import DataProcessor
from report_generator import ReportGenerator
from dashboard_generator import DashboardGenerator
import config


class AnalyticsPipeline:
    """Main pipeline orchestrator for e-commerce analytics."""
    
    def __init__(self, config_file=None):
        """Initialize the analytics pipeline."""
        self.config = config  # Use the imported config module
        self.logger = self._setup_logging()
        
        # Initialize components
        self.data_processor = DataProcessor(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.dashboard_generator = DashboardGenerator(self.config)
        
        # Initialize extraction component (will be imported when needed)
        self.extractor = None
        
        # Ensure directories exist
        self._setup_directories()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        # Create logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Setup logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        log_file = logs_dir / f"analytics_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_directories(self):
        """Ensure all required directories exist."""
        directories = ["data", "logs", "reports", "tests"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def _initialize_extractor(self, headless=True):
        """Initialize the product extractor with fallback handling."""
        try:
            # Import here to avoid circular imports
            from main import ECommerceAnalyzer
            
            self.logger.info("🔧 Initializing product extractor...")
            self.extractor = ECommerceAnalyzer(headless=headless)
            
            # Initialize browser
            if self.extractor.initialize_browser():
                self.logger.info("✅ Product extractor initialized successfully")
                return True
            else:
                self.logger.error("❌ Failed to initialize browser for product extraction")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize product extractor: {e}")
            return False
    
    def extract_products_with_fallback(self, extraction_url=None, headless=True):
        """
        Extract product data with comprehensive fallback mechanism.
        
        Args:
            extraction_url: Specific URL to extract from (optional)
            headless: Whether to run browser in headless mode
            
        Returns:
            bool: True if extraction successful, False if complete failure
        """
        try:
            self.logger.info("🛒 Step 0: Product Data Extraction")
            self.logger.info("=" * 60)
            
            # Check if we already have recent data
            data_file = config.DATA_DIR / config.OUTPUT_CONFIG["json_filename"]
            if data_file.exists():
                self.logger.info(f"📁 Found existing data file: {data_file}")
                
                # Check if data is recent (e.g., less than 24 hours old)
                import time
                file_age_hours = (time.time() - data_file.stat().st_mtime) / 3600
                
                if file_age_hours < 24:
                    self.logger.info(f"✅ Using existing data (age: {file_age_hours:.1f} hours)")
                    return True
                else:
                    self.logger.info(f"⚠️ Data is old (age: {file_age_hours:.1f} hours), attempting fresh extraction...")
            
            # Initialize extractor
            if not self._initialize_extractor(headless=headless):
                self.logger.error("❌ Extractor initialization failed - STOPPING PIPELINE")
                return False
            
            # Attempt extraction with multiple fallback strategies
            extraction_success = False
            
            # Strategy 1: Extract from specific URL if provided
            if extraction_url:
                self.logger.info(f"🎯 Strategy 1: Extracting from specific URL")
                try:
                    products = self.extractor.extract_products_from_specific_url(extraction_url)
                    if products and len(products) > 0:
                        self.logger.info(f"✅ Strategy 1 SUCCESS: Extracted {len(products)} products")
                        extraction_success = True
                    else:
                        self.logger.warning("⚠️ Strategy 1 FAILED: No products extracted from specific URL")
                except Exception as e:
                    self.logger.warning(f"⚠️ Strategy 1 ERROR: {e}")
            
            # Strategy 2: Run full product category analysis if Strategy 1 failed
            if not extraction_success:
                self.logger.info("🎯 Strategy 2: Running full product category analysis")
                try:
                    # Navigate to website first
                    if self.extractor.navigate_to_target_website():
                        if self.extractor.run_product_category_analysis():
                            self.logger.info("✅ Strategy 2 SUCCESS: Full product analysis completed")
                            extraction_success = True
                        else:
                            self.logger.warning("⚠️ Strategy 2 FAILED: Product analysis failed")
                    else:
                        self.logger.warning("⚠️ Strategy 2 FAILED: Website navigation failed")
                except Exception as e:
                    self.logger.warning(f"⚠️ Strategy 2 ERROR: {e}")
            
            # Strategy 3: Try direct URL approach with different URLs
            if not extraction_success:
                self.logger.info("🎯 Strategy 3: Trying direct URL approaches")
                fallback_urls = [
                    "https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001",
                    "https://www.bestbuy.com/site/computers-pcs/laptop-computers/abcat0502000.c?id=abcat0502000",
                    "https://www.bestbuy.com/site/searchpage.jsp?st=laptops"
                ]
                
                for i, url in enumerate(fallback_urls):
                    try:
                        self.logger.info(f"   Trying fallback URL {i+1}/{len(fallback_urls)}")
                        products = self.extractor.extract_product_data(use_specific_url=True, specific_url=url)
                        if products and len(products) > 0:
                            self.logger.info(f"✅ Strategy 3 SUCCESS: Extracted {len(products)} products from URL {i+1}")
                            extraction_success = True
                            break
                        else:
                            self.logger.warning(f"⚠️ URL {i+1} failed - no products extracted")
                    except Exception as e:
                        self.logger.warning(f"⚠️ URL {i+1} error: {e}")
            
            # Clean up extractor
            try:
                if self.extractor:
                    self.extractor.cleanup()
            except Exception as e:
                self.logger.warning(f"⚠️ Cleanup warning: {e}")
            
            if extraction_success:
                self.logger.info("🎉 Product extraction completed successfully!")
                return True
            else:
                self.logger.error("❌ ALL EXTRACTION STRATEGIES FAILED")
                
                # Check if we have any data file at all (even old one)
                if data_file.exists():
                    self.logger.info("📁 Falling back to existing data file for analytics")
                    return True
                else:
                    self.logger.error("❌ No data available - STOPPING PIPELINE")
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Critical error in product extraction: {e}")
            
            # Final fallback - check for existing data
            data_file = config.DATA_DIR / config.OUTPUT_CONFIG["json_filename"]
            if data_file.exists():
                self.logger.info("📁 Critical fallback: Using existing data file")
                return True
            else:
                self.logger.error("❌ No fallback data available - STOPPING PIPELINE")
                return False
    
    def run_complete_analysis_with_extraction(self, extraction_url=None, headless=True, data_filename=None):
        """
        Run the complete analytics pipeline including product extraction.
        
        Args:
            extraction_url: Specific URL to extract from (optional)
            headless: Whether to run browser in headless mode
            data_filename: Specific data file to use (skips extraction if provided)
            
        Returns:
            bool: True if pipeline completed successfully
        """
        try:
            self.logger.info("🚀 Starting Complete E-Commerce Analytics Pipeline with Extraction")
            self.logger.info("=" * 80)
            
            # Step 0: Product Data Extraction (only if no specific data file provided)
            if not data_filename:
                extraction_success = self.extract_products_with_fallback(
                    extraction_url=extraction_url, 
                    headless=headless
                )
                
                if not extraction_success:
                    self.logger.error("❌ Product extraction failed - PIPELINE STOPPED")
                    self.logger.info("💡 To run analytics on existing data, use: --data-file [filename]")
                    return False
                
                self.logger.info("✅ Product extraction phase completed successfully")
                self.logger.info("=" * 60)
            else:
                self.logger.info(f"📁 Using provided data file: {data_filename}")
                self.logger.info("=" * 60)
            
            # Continue with existing analytics pipeline
            return self.run_complete_analysis(data_filename)
            
        except Exception as e:
            self.logger.error(f"❌ Complete pipeline failed with error: {e}")
            return False
    
    def run_complete_analysis(self, data_filename=None):
        """Run the complete analytics pipeline."""
        try:
            self.logger.info("🚀 Starting E-Commerce Analytics Pipeline")
            self.logger.info("=" * 60)
            
            # Step 1: Data Processing and Analysis
            self.logger.info("📊 Step 1: Data Processing and Analysis")
            data = self.data_processor.load_product_data(data_filename) if data_filename else self.data_processor.load_product_data()
            
            if not data:
                self.logger.error("❌ No data available for processing")
                return False
            
            # Create product summary and brand analysis
            df_products, pivot_brand = self.data_processor.create_product_summary(data)
            if df_products.empty:
                self.logger.error("❌ Failed to create product summary")
                return False
            
            # Create specifications comparison
            df_specs = self.data_processor.create_specs_comparison(df_products)
            
            # Analyze reviews and sentiment
            df_reviews, agg = self.data_processor.analyze_reviews(data)
            
            # Create visualizations
            self.data_processor.create_visualizations(df_reviews)
            
            # Save Excel report
            excel_path = self.data_processor.save_excel_report(df_products, pivot_brand, df_specs, df_reviews, agg)
            
            if not excel_path:
                self.logger.error("❌ Failed to create Excel report")
                return False
            
            self.logger.info("✅ Data processing completed successfully")
            
            # Step 2: Automated Report Generation
            self.logger.info("📋 Step 2: Automated Report Generation")
            try:
                pdf_path = self.report_generator.generate_pdf_report(df_products, pivot_brand, df_reviews, agg)
                if pdf_path:
                    self.logger.info("✅ PDF report generated successfully")
                else:
                    self.logger.warning("⚠️ PDF report generation failed or not implemented")
            except Exception as e:
                self.logger.warning(f"⚠️ PDF report generation failed: {e}")
            
            # Step 3: Data Visualization Dashboard
            self.logger.info("📈 Step 3: Data Visualization Dashboard")
            try:
                dashboard_path = self.dashboard_generator.generate_dashboard(df_products, pivot_brand, df_reviews, agg)
                if dashboard_path:
                    self.logger.info("✅ Interactive dashboard created successfully")
                else:
                    self.logger.warning("⚠️ Dashboard generation failed or not implemented")
            except Exception as e:
                self.logger.warning(f"⚠️ Dashboard generation failed: {e}")
            
            # Summary
            self.logger.info("=" * 60)
            self.logger.info("🎉 Analytics Pipeline Completed Successfully!")
            self.logger.info("📁 Generated Files:")
            self.logger.info(f"   📊 Excel Report: {excel_path}")
            self.logger.info(f"   📈 Charts: reports/sentiment_*.png")
            if 'pdf_path' in locals() and pdf_path:
                self.logger.info(f"   📋 PDF Report: {pdf_path}")
            if 'dashboard_path' in locals() and dashboard_path:
                self.logger.info(f"   🖥️  Dashboard: {dashboard_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Pipeline failed with error: {e}")
            return False
    
    def run_extraction_only(self, extraction_url=None, headless=True):
        """Run only the product extraction component."""
        try:
            self.logger.info("🛒 Running Product Extraction Only")
            success = self.extract_products_with_fallback(extraction_url=extraction_url, headless=headless)
            return success
        except Exception as e:
            self.logger.error(f"Product extraction failed: {e}")
            return False
    
    def run_data_processing_only(self, data_filename=None):
        """Run only the data processing component."""
        try:
            self.logger.info("📊 Running Data Processing Only")
            success = self.data_processor.process_all_data(data_filename)
            return success
        except Exception as e:
            self.logger.error(f"Data processing failed: {e}")
            return False
    
    def run_report_generation_only(self, data_filename=None):
        """Run only the report generation component."""
        try:
            self.logger.info("📋 Running Report Generation Only")
            # Load data first
            data = self.data_processor.load_product_data(data_filename) if data_filename else self.data_processor.load_product_data()
            df_products, pivot_brand = self.data_processor.create_product_summary(data)
            df_reviews, agg = self.data_processor.analyze_reviews(data)
            
            # Generate report
            pdf_path = self.report_generator.generate_pdf_report(df_products, pivot_brand, df_reviews, agg)
            return pdf_path is not None
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return False
    
    def run_dashboard_generation_only(self, data_filename=None):
        """Run only the dashboard generation component."""
        try:
            self.logger.info("📈 Running Dashboard Generation Only")
            # Load data first
            data = self.data_processor.load_product_data(data_filename) if data_filename else self.data_processor.load_product_data()
            df_products, pivot_brand = self.data_processor.create_product_summary(data)
            df_reviews, agg = self.data_processor.analyze_reviews(data)
            
            # Generate dashboard
            dashboard_path = self.dashboard_generator.generate_dashboard(df_products, pivot_brand, df_reviews, agg)
            return dashboard_path is not None
        except Exception as e:
            self.logger.error(f"Dashboard generation failed: {e}")
            return False


def main():
    """Main function for running the analytics pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description='E-Commerce Analytics Pipeline')
    parser.add_argument('--mode', choices=['all', 'extract', 'data', 'report', 'dashboard', 'full'], 
                       default='full', help='Which component to run (default: full - includes extraction)')
    parser.add_argument('--data-file', help='Specific data file to process')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--extraction-url', help='Specific URL to extract products from')
    parser.add_argument('--visible', action='store_true', help='Run browser in visible mode (non-headless)')
    
    args = parser.parse_args()
    
    # Create pipeline
    pipeline = AnalyticsPipeline(args.config)
    
    # Determine headless mode
    headless = not args.visible
    
    # Run based on mode
    if args.mode == 'full':
        # Full pipeline including extraction
        success = pipeline.run_complete_analysis_with_extraction(
            extraction_url=args.extraction_url,
            headless=headless,
            data_filename=args.data_file
        )
    elif args.mode == 'all':
        # Analytics only (no extraction)
        success = pipeline.run_complete_analysis(args.data_file)
    elif args.mode == 'extract':
        # Extraction only
        success = pipeline.run_extraction_only(args.extraction_url, headless)
    elif args.mode == 'data':
        success = pipeline.run_data_processing_only(args.data_file)
    elif args.mode == 'report':
        success = pipeline.run_report_generation_only(args.data_file)
    elif args.mode == 'dashboard':
        success = pipeline.run_dashboard_generation_only(args.data_file)
    
    if success:
        print("\n✨ Pipeline execution completed successfully!")
    else:
        print("\n❌ Pipeline execution failed. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 