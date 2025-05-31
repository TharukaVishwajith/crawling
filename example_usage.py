#!/usr/bin/env python3
"""
Example Usage Script for Enhanced E-Commerce Analytics Pipeline

This script demonstrates how to use the enhanced analytics pipeline
with integrated product extraction and fallback mechanisms.

Author: Assessment Solution
Date: 2024
"""

import sys
from pathlib import Path
from analytics_pipeline import AnalyticsPipeline

def example_full_pipeline_with_extraction():
    """
    Example 1: Run complete pipeline with product extraction
    This includes extraction + analytics + reports + dashboard
    """
    print("🚀 Example 1: Complete Pipeline with Product Extraction")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = AnalyticsPipeline()
    
    # Run complete pipeline with extraction
    # This will:
    # 1. Check for recent data (< 24 hours)
    # 2. If no recent data, attempt extraction with fallback strategies
    # 3. Process the data (Excel report, sentiment analysis, visualizations)
    # 4. Generate PDF report
    # 5. Create interactive dashboard
    
    success = pipeline.run_complete_analysis_with_extraction(
        extraction_url="https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001",
        headless=True  # Set to False for debugging
    )
    
    if success:
        print("✅ Complete pipeline executed successfully!")
        print("📁 Check these directories for outputs:")
        print("   - data/raw_product_data.json (extracted products)")
        print("   - reports/Product_Analysis.xlsx (Excel report)")
        print("   - reports/E-Commerce_Analysis_Report.pdf (PDF report)")
        print("   - reports/analytics_dashboard.html (Interactive dashboard)")
        print("   - reports/sentiment_*.png (Visualization charts)")
    else:
        print("❌ Pipeline failed. Check logs for details.")
    
    return success

def example_extraction_only():
    """
    Example 2: Extract products only (no analytics)
    Useful for data collection phase
    """
    print("\n🛒 Example 2: Product Extraction Only")
    print("=" * 60)
    
    pipeline = AnalyticsPipeline()
    
    # Extract products with fallback strategies
    success = pipeline.extract_products_with_fallback(
        extraction_url="https://www.bestbuy.com/site/searchpage.jsp?browsedCategory=pcmcat138500050001&id=pcat17071&qp=currentprice_facet%3DPrice%7E500+to+1500%5Ebrand_facet%3DBrand%7EDell%5Ebrand_facet%3DBrand%7ELenovo%5Ebrand_facet%3DBrand%7EHP%5Ecustomerreviews_facet%3DCustomer+Rating%7E4+%26+Up&st=categoryid%24pcmcat138500050001",
        headless=True
    )
    
    if success:
        print("✅ Product extraction completed successfully!")
        print("📁 Data saved to: data/raw_product_data.json")
    else:
        print("❌ Product extraction failed. Check logs for details.")
    
    return success

def example_analytics_without_extraction():
    """
    Example 3: Run analytics on existing data (skip extraction)
    Useful when you already have data
    """
    print("\n📊 Example 3: Analytics Without Extraction")
    print("=" * 60)
    
    pipeline = AnalyticsPipeline()
    
    # Check if we have existing data
    data_file = Path("data/raw_product_data.json")
    if not data_file.exists():
        print("❌ No existing data found. Please run extraction first.")
        return False
    
    # Run analytics on existing data
    success = pipeline.run_complete_analysis()
    
    if success:
        print("✅ Analytics completed successfully!")
        print("📁 Generated reports in reports/ directory")
    else:
        print("❌ Analytics failed. Check logs for details.")
    
    return success

def example_individual_components():
    """
    Example 4: Run individual components separately
    Useful for development and testing
    """
    print("\n🔧 Example 4: Individual Components")
    print("=" * 60)
    
    pipeline = AnalyticsPipeline()
    
    # Check if we have data
    data_file = Path("data/raw_product_data.json")
    if not data_file.exists():
        print("❌ No existing data found. Running extraction first...")
        if not pipeline.extract_products_with_fallback():
            print("❌ Extraction failed. Cannot proceed with individual components.")
            return False
    
    # Run individual components
    print("📊 Running data processing...")
    data_success = pipeline.run_data_processing_only()
    
    print("📋 Running report generation...")
    report_success = pipeline.run_report_generation_only()
    
    print("📈 Running dashboard generation...")
    dashboard_success = pipeline.run_dashboard_generation_only()
    
    overall_success = data_success and report_success and dashboard_success
    
    if overall_success:
        print("✅ All individual components completed successfully!")
    else:
        print("⚠️ Some components failed. Check logs for details.")
    
    return overall_success

def example_fallback_demonstration():
    """
    Example 5: Demonstrate fallback mechanisms
    Shows how the system handles various failure scenarios
    """
    print("\n🛡️ Example 5: Fallback Mechanism Demonstration")
    print("=" * 60)
    
    pipeline = AnalyticsPipeline()
    
    # Test with invalid URL (will trigger fallback)
    print("Testing with invalid URL to demonstrate fallback...")
    success = pipeline.extract_products_with_fallback(
        extraction_url="https://invalid-url-for-testing.com",
        headless=True
    )
    
    if success:
        print("✅ Fallback mechanism worked! Used existing data or alternative strategies.")
    else:
        print("❌ All fallback strategies failed.")
    
    return success

def main():
    """
    Main function to run all examples
    """
    print("🎯 E-Commerce Analytics Pipeline - Enhanced Examples")
    print("=" * 80)
    
    examples = [
        ("Complete Pipeline with Extraction", example_full_pipeline_with_extraction),
        ("Extraction Only", example_extraction_only),
        ("Analytics Without Extraction", example_analytics_without_extraction),
        ("Individual Components", example_individual_components),
        ("Fallback Demonstration", example_fallback_demonstration)
    ]
    
    # Ask user which example to run
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  0. Run all examples")
    
    try:
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == "0":
            # Run all examples
            results = []
            for name, func in examples:
                print(f"\n{'='*80}")
                print(f"Running: {name}")
                print(f"{'='*80}")
                results.append(func())
            
            print(f"\n{'='*80}")
            print("FINAL RESULTS:")
            for i, (name, _) in enumerate(examples):
                status = "✅ SUCCESS" if results[i] else "❌ FAILED"
                print(f"  {name}: {status}")
            print(f"{'='*80}")
            
        elif choice in ["1", "2", "3", "4", "5"]:
            # Run specific example
            idx = int(choice) - 1
            name, func = examples[idx]
            print(f"\nRunning: {name}")
            print("=" * 80)
            success = func()
            
            print(f"\nFinal result: {'✅ SUCCESS' if success else '❌ FAILED'}")
            
        else:
            print("❌ Invalid choice. Please select 0-5.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Process interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1
    
    print("\n🎉 Example execution completed!")
    print("📁 Check the following directories for outputs:")
    print("  - data/ (extracted product data)")
    print("  - reports/ (Excel, PDF, HTML reports and charts)")
    print("  - logs/ (detailed execution logs)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 