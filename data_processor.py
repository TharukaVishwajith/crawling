"""
Data Processing and Analysis Module

This module handles the processing of collected product and review data,
creating Excel reports with multiple sheets and generating visualizations.

Author: Assessment Solution
Date: 2024
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging
import os
from pathlib import Path


class DataProcessor:
    """Handles data processing, analysis, and Excel report generation."""
    
    def __init__(self, config=None):
        """Initialize the data processor."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Ensure required directories exist
        self.data_dir = Path("data")
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Initialize sentiment analyzer
        try:
            # Try to handle SSL issues for NLTK download
            import ssl
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
            
            # Download VADER lexicon if needed
            try:
                nltk.download('vader_lexicon', quiet=True)
            except:
                # If download fails, try to use existing data
                pass
            
            self.sia = SentimentIntensityAnalyzer()
            # Test the analyzer
            test_result = self.sia.polarity_scores("test")
            self.logger.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize sentiment analyzer: {e}")
            self.sia = None
    
    def load_product_data(self, filename="raw_product_data.json"):
        """Load product data from JSON file."""
        try:
            filepath = self.data_dir / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Data file {filename} not found in {self.data_dir}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate that data is not empty
            if not data or len(data) == 0:
                raise ValueError(f"Data file {filename} is empty")
            
            self.logger.info(f"Loaded {len(data)} products from {filename}")
            return data
            
        except FileNotFoundError as e:
            self.logger.error(f"Data file {filename} not found in {self.data_dir}")
            raise e
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON file {filename}: {e}")
            raise e
        except ValueError as e:
            self.logger.error(f"Invalid data in file {filename}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Unexpected error loading data: {e}")
            raise e
    
    def create_product_summary(self, data):
        """Create product summary DataFrame with brand analysis."""
        try:
            products = []
            for item in data:
                specs = item.get("product_specs", {})
                prod = {
                    "Product Name": item.get("product_name", "N/A"),
                    "Brand": specs.get("brand", "Unknown"),
                    "Model": specs.get("model", "N/A"),
                    "Screen Size": specs.get("screen_size", "N/A"),
                    "Screen Resolution": specs.get("screen_resolution", "N/A"),
                    "Processor": specs.get("processor", "N/A"),
                    "Price": float(item.get("product_price", "0").replace("$", "").replace(",", "")),
                    "URL": item.get("product_url", "N/A")
                }
                products.append(prod)
            
            df_products = pd.DataFrame(products)
            
            # Create brand pivot table
            pivot_brand = df_products.pivot_table(
                index='Brand',
                values='Price',
                aggfunc=['mean', 'count']
            )
            pivot_brand.columns = ['Average Price', 'Product Count']
            pivot_brand.reset_index(inplace=True)
            
            self.logger.info(f"Created product summary with {len(df_products)} products")
            return df_products, pivot_brand
            
        except Exception as e:
            self.logger.error(f"Error creating product summary: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def create_specs_comparison(self, df_products):
        """Create specifications comparison DataFrame."""
        try:
            spec_cols = ["Product Name", "Brand", "Model", "Screen Size", 
                        "Screen Resolution", "Processor", "Price"]
            df_specs = df_products[spec_cols].copy()
            
            self.logger.info("Created specifications comparison")
            return df_specs
            
        except Exception as e:
            self.logger.error(f"Error creating specs comparison: {e}")
            return pd.DataFrame()
    
    def analyze_reviews(self, data):
        """Perform sentiment analysis on reviews."""
        if not self.sia:
            self.logger.error("Sentiment analyzer not available")
            return pd.DataFrame(), pd.DataFrame()
        
        try:
            rows = []
            for prod in data:
                pname = prod.get("product_name", "N/A")
                brand = prod.get("product_specs", {}).get("brand", "Unknown")
                price = float(prod.get("product_price", "0").replace("$", "").replace(",", ""))
                
                for rev in prod.get("reviews", []):
                    text = rev.get("description", "")
                    title = rev.get("title", "")
                    if text:
                        score = self.sia.polarity_scores(text)['compound']
                        rows.append({
                            "Product Name": pname,
                            "Brand": brand,
                            "Price": price,
                            "Review Title": title,
                            "Review Text": text,
                            "Sentiment": score
                        })
            
            df_reviews = pd.DataFrame(rows)
            
            if not df_reviews.empty:
                # Create aggregated sentiment data
                agg = df_reviews.groupby('Product Name').agg(
                    Review_Count=('Sentiment', 'count'),
                    Avg_Sentiment=('Sentiment', 'mean'),
                    Pos_Reviews=('Sentiment', lambda x: (x > 0.2).sum()),
                    Neg_Reviews=('Sentiment', lambda x: (x < -0.2).sum()),
                    Neu_Reviews=('Sentiment', lambda x: ((x >= -0.2) & (x <= 0.2)).sum())
                ).reset_index()
                
                self.logger.info(f"Analyzed {len(df_reviews)} reviews")
                return df_reviews, agg
            else:
                self.logger.warning("No reviews found for sentiment analysis")
                return pd.DataFrame(), pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"Error analyzing reviews: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def create_visualizations(self, df_reviews):
        """Create and save visualization charts."""
        if df_reviews.empty:
            self.logger.warning("No review data available for visualizations")
            return
        
        try:
            # Ensure reports directory exists
            self.reports_dir.mkdir(exist_ok=True)
            
            # Sentiment distribution pie chart
            sentiment_class = df_reviews['Sentiment'].apply(
                lambda x: 'Positive' if x > 0.2 else ('Negative' if x < -0.2 else 'Neutral')
            )
            sent_counts = sentiment_class.value_counts()
            
            plt.figure(figsize=(8, 6))
            colors = ['#28a745', '#dc3545', '#ffc107']  # Green, Red, Yellow
            plt.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            plt.title('Overall Review Sentiment Distribution', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(self.reports_dir / "sentiment_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            # Average sentiment by brand
            if 'Brand' in df_reviews.columns:
                plt.figure(figsize=(10, 6))
                brand_sentiment = df_reviews.groupby('Brand')['Sentiment'].mean().sort_values(ascending=False)
                sns.barplot(x=brand_sentiment.index, y=brand_sentiment.values, palette='viridis')
                plt.ylabel('Average Sentiment Score', fontsize=12)
                plt.xlabel('Brand', fontsize=12)
                plt.title('Average Sentiment by Brand', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(self.reports_dir / "sentiment_by_brand.png", dpi=300, bbox_inches='tight')
                plt.close()
            
            # Reviews per product vs. sentiment scatter plot
            agg = df_reviews.groupby('Product Name').agg(
                Review_Count=('Sentiment', 'count'),
                Avg_Sentiment=('Sentiment', 'mean')
            ).reset_index()
            
            plt.figure(figsize=(12, 8))
            plt.scatter(agg['Review_Count'], agg['Avg_Sentiment'], 
                       alpha=0.7, s=100, color='steelblue')
            plt.xlabel('Number of Reviews', fontsize=12)
            plt.ylabel('Average Sentiment Score', fontsize=12)
            plt.title('Review Count vs. Average Sentiment', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(self.reports_dir / "sentiment_vs_reviews.png", dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info("Created and saved visualization charts")
            
        except Exception as e:
            self.logger.error(f"Error creating visualizations: {e}")
    
    def save_excel_report(self, df_products, pivot_brand, df_specs, df_reviews, agg):
        """Save comprehensive Excel report with multiple sheets."""
        try:
            output_path = self.reports_dir / 'Product_Analysis.xlsx'
            
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # SHEET 1: Product Summary + Brand Analysis
                df_products.to_excel(writer, sheet_name='Product Summary', index=False, startrow=0)
                startrow = len(df_products) + 3
                pivot_brand.to_excel(writer, sheet_name='Product Summary', index=False, startrow=startrow)
                
                worksheet = writer.sheets['Product Summary']
                
                # Conditional formatting for price column
                if 'Price' in df_products.columns:
                    price_col = df_products.columns.get_loc("Price")
                    worksheet.conditional_format(1, price_col, len(df_products), price_col, {
                        'type': '3_color_scale',
                        'min_color': "#63be7b",
                        'mid_color': "#ffeb84",
                        'max_color': "#f8696b"
                    })
                
                # Data validation for brand and screen size
                if 'Brand' in df_products.columns:
                    brands = df_products['Brand'].unique().tolist()
                    brand_col = df_products.columns.get_loc("Brand")
                    worksheet.data_validation(1, brand_col, len(df_products), brand_col, {
                        'validate': 'list',
                        'source': brands
                    })
                
                if 'Screen Size' in df_products.columns:
                    screen_sizes = df_products['Screen Size'].unique().tolist()
                    size_col = df_products.columns.get_loc("Screen Size")
                    worksheet.data_validation(1, size_col, len(df_products), size_col, {
                        'validate': 'list',
                        'source': screen_sizes
                    })
                
                # SHEET 2: Specifications Comparison
                if not df_specs.empty:
                    df_specs.to_excel(writer, sheet_name='Specifications Comparison', index=False)
                    ws_specs = writer.sheets['Specifications Comparison']
                    
                    # Highlight unique differentiators
                    spec_cols = df_specs.columns.tolist()
                    yellow_format = workbook.add_format({'bg_color': '#FFD966'})
                    
                    for i, col in enumerate(spec_cols):
                        if col not in ["Product Name", "Price"]:
                            freq = df_specs[col].value_counts()
                            for row_num, val in enumerate(df_specs[col], start=2):
                                if pd.notna(val) and freq.get(val, 0) == 1:
                                    ws_specs.write(row_num - 1, i, val, yellow_format)
                        elif col == "Price":
                            ws_specs.conditional_format(1, i, len(df_specs), i, {
                                'type': '3_color_scale',
                                'min_color': "#63be7b",
                                'mid_color': "#ffeb84",
                                'max_color': "#f8696b"
                            })
                
                # SHEET 3: Review Analysis
                if not df_reviews.empty:
                    df_reviews.to_excel(writer, sheet_name='Review Analysis', index=False, startrow=0)
                    if not agg.empty:
                        agg.to_excel(writer, sheet_name='Review Analysis', index=False, 
                                   startrow=len(df_reviews)+3)
            
            self.logger.info(f"Excel report saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving Excel report: {e}")
            return None
    
    def process_all_data(self, data_filename=None):
        """Complete data processing pipeline."""
        try:
            self.logger.info("Starting complete data processing pipeline")
            
            # Load data
            try:
                data = self.load_product_data(data_filename) if data_filename else self.load_product_data()
            except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
                self.logger.error(f"Failed to load data: {e}")
                print(f"❌ Error loading data: {e}")
                return False
            
            # Create product summary and brand analysis
            df_products, pivot_brand = self.create_product_summary(data)
            
            # Create specifications comparison
            df_specs = self.create_specs_comparison(df_products)
            
            # Analyze reviews and sentiment
            df_reviews, agg = self.analyze_reviews(data)
            
            # Create visualizations
            self.create_visualizations(df_reviews)
            
            # Save Excel report
            excel_path = self.save_excel_report(df_products, pivot_brand, df_specs, df_reviews, agg)
            
            if excel_path:
                self.logger.info("Data processing pipeline completed successfully")
                print(f"✅ Data processing complete!")
                print(f"📊 Excel report saved: {excel_path}")
                print(f"📈 Charts saved in: {self.reports_dir}")
                return True
            else:
                self.logger.error("Failed to complete data processing pipeline")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in data processing pipeline: {e}")
            print(f"❌ Error in data processing pipeline: {e}")
            return False


def main():
    """Main function for testing the data processor."""
    import logging
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run data processor
    processor = DataProcessor()
    success = processor.process_all_data()
    
    if success:
        print("\n🎉 Data processing completed successfully!")
        print("Check the 'reports' directory for Excel file and visualization charts.")
    else:
        print("\n❌ Data processing failed. Check logs for details.")


if __name__ == "__main__":
    main() 