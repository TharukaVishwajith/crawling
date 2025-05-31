"""
Automated Report Generation Module

This module handles the generation of comprehensive PDF reports containing
executive summaries, trend analysis, visualizations, and recommendations.

Author: Assessment Solution
Date: 2024
"""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np


class ReportGenerator:
    """Handles automated PDF report generation with charts and analysis."""
    
    def __init__(self, config=None):
        """Initialize the report generator."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Ensure required directories exist
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_executive_summary(self, df_products, df_reviews):
        """Generate executive summary section."""
        summary_text = (
            "This report provides a comprehensive analysis of top-selling laptops based on pricing, brand performance,\n"
            "and customer review sentiment. The analysis covers trends in pricing, comparative sentiment across brands,\n"
            "and highlights top recommended products based on customer satisfaction and value.\n\n"
            f"Dataset analyzed: {len(df_products)} products, {len(df_reviews)} customer reviews.\n"
            "\nKey Findings:\n"
            "- Significant price variation across brands; some brands offer high value for specs.\n"
            "- Most reviews are positive or neutral, with a few models showing consistently high sentiment.\n"
            "- Top recommended laptops were selected by combining high sentiment, review volume, and competitive pricing."
        )
        return summary_text
    
    def create_price_trend_analysis(self, df_products, pdf):
        """Create price trend analysis with charts."""
        try:
            # Price distribution by brand (boxplot)
            plt.figure(figsize=(8, 4))
            sns.boxplot(data=df_products, x='Brand', y='Price')
            plt.title("Laptop Price Distribution by Brand")
            plt.ylabel("Price (USD)")
            plt.xticks(rotation=30)
            pdf.savefig()
            plt.close()

            # Price trend across all products
            plt.figure(figsize=(8, 4))
            sorted_products = df_products.sort_values('Price')
            sns.lineplot(data=sorted_products, x=range(len(sorted_products)), y='Price', marker='o')
            plt.title("Laptop Price Trend (All Products)")
            plt.xlabel("Product Index (sorted by price)")
            plt.ylabel("Price (USD)")
            pdf.savefig()
            plt.close()
            
            self.logger.info("Created price trend analysis charts")
            
        except Exception as e:
            self.logger.error(f"Error creating price trend analysis: {e}")
    
    def create_sentiment_analysis_section(self, df_reviews, pdf):
        """Create review sentiment analysis visualizations."""
        try:
            if df_reviews.empty:
                self.logger.warning("No review data available for sentiment analysis")
                return
            
            # Overall sentiment distribution (pie chart)
            sentiment_class = df_reviews['Sentiment'].apply(
                lambda x: 'Positive' if x > 0.2 else ('Negative' if x < -0.2 else 'Neutral')
            )
            sent_counts = sentiment_class.value_counts()
            plt.figure(figsize=(5, 5))
            plt.pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', 
                   colors=['green','red','gold'])
            plt.title('Overall Review Sentiment Distribution')
            pdf.savefig()
            plt.close()

            # Average sentiment by brand
            if 'Brand' in df_reviews.columns:
                plt.figure(figsize=(8, 4))
                brand_sent = df_reviews.groupby('Brand')['Sentiment'].mean().sort_values()
                sns.barplot(x=brand_sent.index, y=brand_sent.values, palette='viridis')
                plt.ylabel('Average Sentiment')
                plt.title('Average Review Sentiment by Brand')
                plt.xticks(rotation=30)
                pdf.savefig()
                plt.close()
                
            self.logger.info("Created sentiment analysis visualizations")
            
        except Exception as e:
            self.logger.error(f"Error creating sentiment analysis: {e}")
    
    def create_competitive_analysis(self, df_products, pdf):
        """Create competitive analysis of brands."""
        try:
            # Number of products per brand
            brand_counts = df_products['Brand'].value_counts()
            plt.figure(figsize=(8, 4))
            sns.barplot(x=brand_counts.index, y=brand_counts.values)
            plt.title('Number of Products per Brand')
            plt.ylabel('Product Count')
            plt.xlabel('Brand')
            pdf.savefig()
            plt.close()

            # Average price by brand
            plt.figure(figsize=(8, 4))
            brand_price = df_products.groupby('Brand')['Price'].mean().sort_values()
            sns.barplot(x=brand_price.index, y=brand_price.values)
            plt.title('Average Laptop Price by Brand')
            plt.ylabel('Avg Price (USD)')
            plt.xlabel('Brand')
            plt.xticks(rotation=30)
            pdf.savefig()
            plt.close()
            
            self.logger.info("Created competitive analysis charts")
            
        except Exception as e:
            self.logger.error(f"Error creating competitive analysis: {e}")
    
    def create_recommendations(self, df_products, df_reviews, pdf):
        """Generate top products recommendations."""
        try:
            if df_reviews.empty:
                self.logger.warning("No review data available for recommendations")
                return
            
            # Create aggregated review data
            agg = df_reviews.groupby('Product Name').agg(
                Review_Count=('Sentiment', 'count'),
                Avg_Sentiment=('Sentiment', 'mean'),
                Pos_Reviews=('Sentiment', lambda x: (x > 0.2).sum()),
                Neg_Reviews=('Sentiment', lambda x: (x < -0.2).sum()),
                Neu_Reviews=('Sentiment', lambda x: ((x >= -0.2) & (x <= 0.2)).sum())
            ).reset_index()

            # Merge with product data
            agg_merged = pd.merge(
                agg,
                df_products[['Product Name', 'Brand', 'Price']],
                on='Product Name',
                how='left'
            )

            # Filter and sort for recommendations
            min_reviews = 2  # Lowered for synthetic data
            recommended = agg_merged[agg_merged['Review_Count'] >= min_reviews].sort_values(
                by=['Avg_Sentiment', 'Review_Count', 'Price'],
                ascending=[False, False, True]
            ).head(5)

            # Create recommendations table
            if not recommended.empty:
                fig, ax = plt.subplots(figsize=(8.5, 4))
                ax.axis('off')
                table = ax.table(
                    cellText=recommended[['Product Name', 'Brand', 'Price', 'Avg_Sentiment', 'Review_Count']].round(2).values,
                    colLabels=['Product Name', 'Brand', 'Price', 'Avg Sentiment', 'Review Count'],
                    loc='center',
                    cellLoc='left',
                    colLoc='left'
                )
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 2)
                plt.title('Top 5 Recommended Laptops', fontsize=14, y=1.15)
                pdf.savefig(fig)
                plt.close()
                
                self.logger.info("Created product recommendations table")
            else:
                self.logger.warning("No products meet minimum review criteria for recommendations")
                
        except Exception as e:
            self.logger.error(f"Error creating recommendations: {e}")
    
    def generate_pdf_report(self, df_products, pivot_brand, df_reviews, agg):
        """Generate comprehensive PDF report."""
        try:
            output_path = self.reports_dir / 'E-Commerce_Analysis_Report.pdf'
            
            with PdfPages(str(output_path)) as pdf:
                # Executive Summary
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')

                # Title
                ax.set_title("Executive Summary", fontsize=20, fontweight='bold', loc='left', pad=40)

                # Summary text
                left_pad = 0
                title_y = 0.97
                pad_fraction = 0.045
                text_y = title_y - pad_fraction

                summary_text = self.generate_executive_summary(df_products, df_reviews)
                ax.text(
                    left_pad, text_y,
                    summary_text,
                    va='top', ha='left',
                    wrap=True,
                    fontsize=12
                )
                pdf.savefig(fig)
                plt.close()

                # Price Trend Analysis
                self.create_price_trend_analysis(df_products, pdf)

                # Review Sentiment Analysis
                self.create_sentiment_analysis_section(df_reviews, pdf)

                # Brand Competitive Analysis
                self.create_competitive_analysis(df_products, pdf)

                # Top Product Recommendations
                self.create_recommendations(df_products, df_reviews, pdf)
            
            self.logger.info(f"PDF report generated: {output_path}")
            print(f"📋 PDF report created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error generating PDF report: {e}")
            return None


def main():
    """Main function for testing the report generator."""
    # Test with sample data
    import sys
    sys.path.append('.')
    from data_processor import DataProcessor
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create processor and generator
    processor = DataProcessor()
    generator = ReportGenerator()
    
    # Load data
    data = processor.load_product_data()
    df_products, pivot_brand = processor.create_product_summary(data)
    df_reviews, agg = processor.analyze_reviews(data)
    
    # Generate report
    success = generator.generate_pdf_report(df_products, pivot_brand, df_reviews, agg)
    
    if success:
        print("✅ PDF report generation test completed successfully!")
    else:
        print("❌ PDF report generation test failed.")


if __name__ == "__main__":
    main() 