"""
Data Visualization Dashboard Module

This module creates an interactive HTML dashboard using plotly/dash containing
interactive charts for price comparison, sentiment trends, and brand performance.

Author: Assessment Solution
Date: 2024
"""

import logging
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots


class DashboardGenerator:
    """Handles creation of interactive HTML dashboard with plotly."""
    
    def __init__(self, config=None):
        """Initialize the dashboard generator."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Ensure required directories exist
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
    
    def create_price_comparison_chart(self, df_products):
        """Create interactive price comparison charts."""
        try:
            # Interactive Price Comparison Boxplot
            price_box = go.Figure()
            for brand in df_products['Brand'].unique():
                filtered = df_products[df_products['Brand'] == brand]
                price_box.add_trace(go.Box(
                    y=filtered['Price'],
                    name=brand,
                    boxmean='sd',
                    boxpoints='all',
                    jitter=0.5
                ))
            price_box.update_layout(
                title="Laptop Price Distribution by Brand", 
                yaxis_title="Price (USD)",
                height=500
            )
            
            self.logger.info("Created price comparison chart")
            return price_box
            
        except Exception as e:
            self.logger.error(f"Error creating price comparison chart: {e}")
            return go.Figure()
    
    def create_sentiment_trends_chart(self, df_reviews):
        """Create review sentiment trends visualization."""
        try:
            if df_reviews.empty:
                self.logger.warning("No review data for sentiment trends")
                sentiment_scatter = go.Figure()
                sentiment_scatter.update_layout(title="No review data available")
                return sentiment_scatter
            
            # Review Sentiment Trends per Product
            sentiment_trend = df_reviews.groupby('Product Name')['Sentiment'].mean().reset_index()
            sentiment_trend = pd.merge(
                sentiment_trend, 
                df_reviews[['Product Name', 'Brand']].drop_duplicates(), 
                on='Product Name'
            )
            
            sentiment_scatter = go.Figure()
            for brand in sentiment_trend['Brand'].unique():
                brand_df = sentiment_trend[sentiment_trend['Brand'] == brand]
                sentiment_scatter.add_trace(go.Scatter(
                    x=brand_df['Product Name'],
                    y=brand_df['Sentiment'],
                    mode='markers+lines',
                    name=brand,
                    hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
                ))
            sentiment_scatter.update_layout(
                title="Average Review Sentiment by Product",
                yaxis_title="Average Sentiment",
                xaxis_title="Product",
                showlegend=True,
                height=500,
                xaxis={'tickangle': 45}
            )
            
            self.logger.info("Created sentiment trends chart")
            return sentiment_scatter
            
        except Exception as e:
            self.logger.error(f"Error creating sentiment trends chart: {e}")
            return go.Figure()
    
    def create_brand_performance_chart(self, df_products, df_reviews):
        """Create brand performance metrics visualization."""
        try:
            # Brand Performance Metrics
            brand_perf = df_products.groupby('Brand').agg(
                Avg_Price=('Price', 'mean'),
                Product_Count=('Product Name', 'count')
            ).reset_index()
            
            if not df_reviews.empty:
                brand_sent = df_reviews.groupby('Brand')['Sentiment'].mean().reset_index()
                brand_perf = pd.merge(brand_perf, brand_sent, on='Brand', how='left').rename(
                    columns={'Sentiment': 'Avg_Sentiment'}
                )
            else:
                brand_perf['Avg_Sentiment'] = None

            # Create grouped bar chart
            brand_bar = go.Figure()
            
            # Normalize data for comparison (scale to 0-100)
            max_price = brand_perf['Avg_Price'].max()
            max_count = brand_perf['Product_Count'].max()
            
            brand_bar.add_trace(go.Bar(
                name='Avg Price (scaled)', 
                x=brand_perf['Brand'], 
                y=(brand_perf['Avg_Price'] / max_price) * 100,
                hovertemplate='Brand: %{x}<br>Avg Price: $%{customdata:.0f}<extra></extra>',
                customdata=brand_perf['Avg_Price']
            ))
            
            brand_bar.add_trace(go.Bar(
                name='Product Count (scaled)', 
                x=brand_perf['Brand'], 
                y=(brand_perf['Product_Count'] / max_count) * 100,
                hovertemplate='Brand: %{x}<br>Product Count: %{customdata}<extra></extra>',
                customdata=brand_perf['Product_Count']
            ))
            
            if not brand_perf['Avg_Sentiment'].isnull().all():
                # Scale sentiment from [-1,1] to [0,100]
                sentiment_scaled = ((brand_perf['Avg_Sentiment'] + 1) / 2) * 100
                brand_bar.add_trace(go.Bar(
                    name='Avg Sentiment (scaled)', 
                    x=brand_perf['Brand'], 
                    y=sentiment_scaled,
                    hovertemplate='Brand: %{x}<br>Avg Sentiment: %{customdata:.2f}<extra></extra>',
                    customdata=brand_perf['Avg_Sentiment']
                ))
            
            brand_bar.update_layout(
                barmode='group',
                title="Brand Performance Metrics (Scaled 0-100 for Comparison)",
                yaxis_title="Scaled Value (0-100)",
                height=500
            )
            
            self.logger.info("Created brand performance chart")
            return brand_bar
            
        except Exception as e:
            self.logger.error(f"Error creating brand performance chart: {e}")
            return go.Figure()
    
    def create_sentiment_distribution_chart(self, df_reviews):
        """Create sentiment distribution pie chart."""
        try:
            if df_reviews.empty:
                sentiment_pie = go.Figure()
                sentiment_pie.update_layout(title="No review data available")
                return sentiment_pie
            
            # Add sentiment category
            df_reviews['Sentiment Category'] = df_reviews['Sentiment'].apply(
                lambda x: 'Positive' if x > 0.2 else ('Negative' if x < -0.2 else 'Neutral')
            )
            
            # Review Sentiment Distribution (Pie)
            sentiment_dist = df_reviews['Sentiment Category'].value_counts().reset_index()
            sentiment_dist.columns = ['Sentiment', 'Count']
            
            sentiment_pie = go.Figure(data=[go.Pie(
                labels=sentiment_dist['Sentiment'], 
                values=sentiment_dist['Count'],
                hole=0.3,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            sentiment_pie.update_layout(
                title='Overall Review Sentiment Distribution',
                height=500
            )
            
            self.logger.info("Created sentiment distribution chart")
            return sentiment_pie
            
        except Exception as e:
            self.logger.error(f"Error creating sentiment distribution chart: {e}")
            return go.Figure()
    
    def create_comprehensive_dashboard(self, df_products, pivot_brand, df_reviews, agg):
        """Create comprehensive interactive dashboard."""
        try:
            # Create individual charts
            price_box = self.create_price_comparison_chart(df_products)
            sentiment_scatter = self.create_sentiment_trends_chart(df_reviews)
            brand_bar = self.create_brand_performance_chart(df_products, df_reviews)
            sentiment_pie = self.create_sentiment_distribution_chart(df_reviews)
            
            # Create comprehensive HTML dashboard
            dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Laptop Analytics Dashboard</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 40px; 
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        h1 {{ 
            color: white; 
            margin: 0;
            font-size: 2.5em;
        }}
        h2 {{ 
            color: #333; 
            border-left: 4px solid #667eea;
            padding-left: 15px;
            margin-top: 40px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #ddd;
            margin-top: 50px;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }}
        .stat-item {{
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 E-Commerce Laptop Analytics Dashboard</h1>
        <p>Comprehensive analysis of laptop products and customer reviews</p>
    </div>
    
    <div class="stats">
        <div class="stat-item">
            <div class="stat-number">{total_products}</div>
            <div class="stat-label">Products Analyzed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_reviews}</div>
            <div class="stat-label">Customer Reviews</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{total_brands}</div>
            <div class="stat-label">Brands</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">${avg_price:.0f}</div>
            <div class="stat-label">Average Price</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h2>💰 Price Comparison Analysis</h2>
        {price_box}
    </div>
    
    <div class="chart-container">
        <h2>😊 Review Sentiment Trends</h2>
        {sentiment_scatter}
    </div>
    
    <div class="chart-container">
        <h2>🏆 Brand Performance Metrics</h2>
        {brand_bar}
    </div>
    
    <div class="chart-container">
        <h2>📈 Overall Sentiment Distribution</h2>
        {sentiment_pie}
    </div>
    
    <div class="footer">
        <p>🤖 Generated by E-Commerce Analytics Pipeline | Data processed on {timestamp}</p>
        <p>Dashboard created using Python, Pandas, and Plotly</p>
    </div>
</body>
</html>
            """
            
            # Calculate statistics
            total_products = len(df_products)
            total_reviews = len(df_reviews) if not df_reviews.empty else 0
            total_brands = df_products['Brand'].nunique() if not df_products.empty else 0
            avg_price = df_products['Price'].mean() if not df_products.empty else 0
            
            # Get current timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Format the HTML with charts and statistics
            dashboard_html = dashboard_html.format(
                total_products=total_products,
                total_reviews=total_reviews,
                total_brands=total_brands,
                avg_price=avg_price,
                timestamp=timestamp,
                price_box=pio.to_html(price_box, full_html=False, include_plotlyjs='cdn'),
                sentiment_scatter=pio.to_html(sentiment_scatter, full_html=False, include_plotlyjs=False),
                brand_bar=pio.to_html(brand_bar, full_html=False, include_plotlyjs=False),
                sentiment_pie=pio.to_html(sentiment_pie, full_html=False, include_plotlyjs=False)
            )
            
            # Save dashboard
            output_path = self.reports_dir / 'analytics_dashboard.html'
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(dashboard_html)
            
            self.logger.info(f"Dashboard saved to {output_path}")
            print(f"🖥️  Interactive dashboard created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating comprehensive dashboard: {e}")
            return None
    
    def generate_dashboard(self, df_products, pivot_brand, df_reviews, agg):
        """Main method to generate the complete dashboard."""
        try:
            self.logger.info("Starting dashboard generation")
            
            # Create comprehensive dashboard
            dashboard_path = self.create_comprehensive_dashboard(df_products, pivot_brand, df_reviews, agg)
            
            if dashboard_path:
                self.logger.info("Dashboard generation completed successfully")
                return dashboard_path
            else:
                self.logger.error("Failed to generate dashboard")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in dashboard generation: {e}")
            return None


def main():
    """Main function for testing the dashboard generator."""
    # Test with sample data
    import sys
    sys.path.append('.')
    from data_processor import DataProcessor
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create processor and generator
    processor = DataProcessor()
    generator = DashboardGenerator()
    
    # Load data
    data = processor.load_product_data()
    df_products, pivot_brand = processor.create_product_summary(data)
    df_reviews, agg = processor.analyze_reviews(data)
    
    # Generate dashboard
    success = generator.generate_dashboard(df_products, pivot_brand, df_reviews, agg)
    
    if success:
        print("✅ Dashboard generation test completed successfully!")
        print(f"🌐 Open the dashboard file in your browser to view the interactive charts.")
    else:
        print("❌ Dashboard generation test failed.")


if __name__ == "__main__":
    main() 