"""
E-Commerce Analytics Pipeline

This module orchestrates the complete analytics workflow, integrating
data processing, report generation, and dashboard creation.

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
    parser.add_argument('--mode', choices=['all', 'data', 'report', 'dashboard'], 
                       default='all', help='Which component to run')
    parser.add_argument('--data-file', help='Specific data file to process')
    parser.add_argument('--config', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Create pipeline
    pipeline = AnalyticsPipeline(args.config)
    
    # Run based on mode
    if args.mode == 'all':
        success = pipeline.run_complete_analysis(args.data_file)
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