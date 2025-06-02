"""
Unit tests for ReportGenerator class

Tests for PDF report generation functionality including:
- Executive summary generation
- Price trend analysis charts
- Sentiment analysis visualizations
- Competitive analysis charts
- Product recommendations
- Complete PDF report generation
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import pandas as pd
import numpy as np

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from report_generator import ReportGenerator
import config


class TestReportGenerator(unittest.TestCase):
    """Test cases for ReportGenerator class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Mock config paths to use test directory
        self.config_patcher = patch.multiple(
            config,
            REPORTS_DIR=Path(self.test_dir) / "reports"
        )
        self.config_patcher.start()
        
        # Create test directories
        (Path(self.test_dir) / "reports").mkdir(parents=True, exist_ok=True)
        
        # Sample test data
        self.sample_products_df = pd.DataFrame([
            {
                "Product Name": "Dell XPS 13",
                "Brand": "Dell",
                "Model": "XPS 13",
                "Price": 999.0,
                "Screen Size": "13.3 inches",
                "Processor": "Intel i5"
            },
            {
                "Product Name": "HP Pavilion 15",
                "Brand": "HP", 
                "Model": "Pavilion 15",
                "Price": 599.99,
                "Screen Size": "15.6 inches",
                "Processor": "AMD Ryzen 5"
            },
            {
                "Product Name": "Dell Inspiron 14",
                "Brand": "Dell",
                "Model": "Inspiron 14", 
                "Price": 449.99,
                "Screen Size": "14 inches",
                "Processor": "Intel i3"
            }
        ])
        
        self.sample_reviews_df = pd.DataFrame([
            {
                "Product Name": "Dell XPS 13",
                "Brand": "Dell",
                "Price": 999.0,
                "Sentiment": 0.8,
                "Review Title": "Great laptop!",
                "Review Text": "Amazing performance and build quality."
            },
            {
                "Product Name": "Dell XPS 13",
                "Brand": "Dell",
                "Price": 999.0,
                "Sentiment": 0.6,
                "Review Title": "Good choice",
                "Review Text": "Solid laptop for work."
            },
            {
                "Product Name": "HP Pavilion 15",
                "Brand": "HP",
                "Price": 599.99,
                "Sentiment": 0.4,
                "Review Title": "Decent laptop",
                "Review Text": "Average performance but good value."
            },
            {
                "Product Name": "Dell Inspiron 14",
                "Brand": "Dell",
                "Price": 449.99,
                "Sentiment": -0.2,
                "Review Title": "Could be better",
                "Review Text": "Some performance issues."
            }
        ])
        
        self.sample_pivot_brand = pd.DataFrame([
            {"Brand": "Dell", "Average Price": 724.495, "Product Count": 2},
            {"Brand": "HP", "Average Price": 599.99, "Product Count": 1}
        ])
        
        self.sample_agg = pd.DataFrame([
            {
                "Product Name": "Dell XPS 13",
                "Review_Count": 2,
                "Avg_Sentiment": 0.7,
                "Pos_Reviews": 2,
                "Neg_Reviews": 0,
                "Neu_Reviews": 0
            },
            {
                "Product Name": "HP Pavilion 15",
                "Review_Count": 1,
                "Avg_Sentiment": 0.4,
                "Pos_Reviews": 1,
                "Neg_Reviews": 0,
                "Neu_Reviews": 0
            },
            {
                "Product Name": "Dell Inspiron 14",
                "Review_Count": 1,
                "Avg_Sentiment": -0.2,
                "Pos_Reviews": 0,
                "Neg_Reviews": 1,
                "Neu_Reviews": 0
            }
        ])
        
    def tearDown(self):
        """Clean up test environment."""
        self.config_patcher.stop()
        
        # Clean up temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_report_generator_initialization(self):
        """Test ReportGenerator initialization."""
        # Act
        generator = ReportGenerator()
        
        # Assert
        self.assertIsNotNone(generator.logger)
        self.assertIsNotNone(generator.config)
        self.assertTrue(generator.reports_dir.exists())
    
    def test_generate_executive_summary(self):
        """Test executive summary generation."""
        # Arrange
        generator = ReportGenerator()
        
        # Act
        summary = generator.generate_executive_summary(
            self.sample_products_df, 
            self.sample_reviews_df
        )
        
        # Assert
        self.assertIsInstance(summary, str)
        self.assertIn("comprehensive analysis", summary)
        self.assertIn(str(len(self.sample_products_df)), summary)
        self.assertIn(str(len(self.sample_reviews_df)), summary)
        self.assertGreater(len(summary), 100)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    @patch('seaborn.boxplot')
    @patch('seaborn.lineplot')
    def test_create_price_trend_analysis_success(self, mock_lineplot, mock_boxplot, 
                                                mock_close, mock_figure):
        """Test successful price trend analysis creation."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        
        # Act
        generator.create_price_trend_analysis(self.sample_products_df, mock_pdf)
        
        # Assert
        self.assertEqual(mock_figure.call_count, 2)  # Two charts
        mock_boxplot.assert_called_once()
        mock_lineplot.assert_called_once()
        self.assertEqual(mock_pdf.savefig.call_count, 2)
        self.assertEqual(mock_close.call_count, 2)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    @patch('matplotlib.pyplot.pie')
    @patch('seaborn.barplot')
    def test_create_sentiment_analysis_section_success(self, mock_barplot, mock_pie,
                                                      mock_close, mock_figure):
        """Test successful sentiment analysis section creation."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        
        # Act
        generator.create_sentiment_analysis_section(self.sample_reviews_df, mock_pdf)
        
        # Assert
        self.assertEqual(mock_figure.call_count, 2)  # Two charts
        mock_pie.assert_called_once()
        mock_barplot.assert_called_once()
        self.assertEqual(mock_pdf.savefig.call_count, 2)
        self.assertEqual(mock_close.call_count, 2)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_sentiment_analysis_section_empty_data(self, mock_close, mock_figure):
        """Test sentiment analysis section with empty data."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        empty_df = pd.DataFrame()
        
        # Act (should not raise exception)
        generator.create_sentiment_analysis_section(empty_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    @patch('seaborn.barplot')
    def test_create_competitive_analysis_success(self, mock_barplot, mock_close, mock_figure):
        """Test successful competitive analysis creation."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        
        # Act
        generator.create_competitive_analysis(self.sample_products_df, mock_pdf)
        
        # Assert
        self.assertEqual(mock_figure.call_count, 2)  # Two charts
        self.assertEqual(mock_barplot.call_count, 2)
        self.assertEqual(mock_pdf.savefig.call_count, 2)
        self.assertEqual(mock_close.call_count, 2)
    
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.close')
    @patch('pandas.merge')
    def test_create_recommendations_success(self, mock_merge, mock_close, mock_subplots):
        """Test successful recommendations creation."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        
        # Mock matplotlib components
        mock_fig = Mock()
        mock_ax = Mock()
        mock_table = Mock()
        mock_ax.table.return_value = mock_table
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        # Mock merged dataframe
        merged_df = self.sample_agg.copy()
        merged_df['Brand'] = ['Dell', 'HP', 'Dell']
        merged_df['Price'] = [999.0, 599.99, 449.99]
        mock_merge.return_value = merged_df
        
        # Act
        generator.create_recommendations(
            self.sample_products_df, 
            self.sample_reviews_df, 
            mock_pdf
        )
        
        # Assert
        mock_merge.assert_called_once()
        mock_subplots.assert_called_once()
        mock_ax.table.assert_called_once()
        mock_pdf.savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.close')
    def test_create_recommendations_empty_data(self, mock_close, mock_subplots):
        """Test recommendations creation with empty review data."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        empty_df = pd.DataFrame()
        
        # Act (should not raise exception)
        generator.create_recommendations(self.sample_products_df, empty_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.close')
    @patch('pandas.merge')
    def test_create_recommendations_no_qualifying_products(self, mock_merge, mock_close, mock_subplots):
        """Test recommendations creation when no products meet minimum criteria."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        
        # Mock merged dataframe with low review counts
        merged_df = self.sample_agg.copy()
        merged_df['Brand'] = ['Dell', 'HP', 'Dell']
        merged_df['Price'] = [999.0, 599.99, 449.99]
        merged_df['Review_Count'] = [1, 1, 1]  # All below minimum threshold
        mock_merge.return_value = merged_df
        
        # Act (should not raise exception)
        generator.create_recommendations(
            self.sample_products_df,
            self.sample_reviews_df,
            mock_pdf
        )
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('report_generator.PdfPages')
    @patch.object(ReportGenerator, 'create_price_trend_analysis')
    @patch.object(ReportGenerator, 'create_sentiment_analysis_section') 
    @patch.object(ReportGenerator, 'create_competitive_analysis')
    @patch.object(ReportGenerator, 'create_recommendations')
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.close')
    def test_generate_pdf_report_success(self, mock_close, mock_subplots, 
                                       mock_recommendations, mock_competitive,
                                       mock_sentiment, mock_price, mock_pdf_pages):
        """Test successful PDF report generation."""
        # Arrange
        generator = ReportGenerator()
        
        # Mock PdfPages context manager
        mock_pdf = Mock()
        mock_pdf_pages.return_value.__enter__.return_value = mock_pdf
        
        # Mock matplotlib components
        mock_fig = Mock()
        mock_ax = Mock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        
        # Act
        result = generator.generate_pdf_report(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(str(result).endswith('.pdf'))
        mock_pdf_pages.assert_called_once()
        mock_price.assert_called_once()
        mock_sentiment.assert_called_once()
        mock_competitive.assert_called_once()
        mock_recommendations.assert_called_once()
    
    @patch('report_generator.PdfPages')
    def test_generate_pdf_report_exception(self, mock_pdf_pages):
        """Test PDF report generation with exception."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf_pages.side_effect = Exception("PDF generation failed")
        
        # Act
        result = generator.generate_pdf_report(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNone(result)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_price_trend_analysis_exception(self, mock_close, mock_figure):
        """Test price trend analysis with exception."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act (should not raise exception)
        generator.create_price_trend_analysis(self.sample_products_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_sentiment_analysis_section_exception(self, mock_close, mock_figure):
        """Test sentiment analysis section with exception."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act (should not raise exception)
        generator.create_sentiment_analysis_section(self.sample_reviews_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_competitive_analysis_exception(self, mock_close, mock_figure):
        """Test competitive analysis with exception."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act (should not raise exception)
        generator.create_competitive_analysis(self.sample_products_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.close')
    def test_create_recommendations_exception(self, mock_close, mock_subplots):
        """Test recommendations creation with exception."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        mock_subplots.side_effect = Exception("Chart creation failed")
        
        # Act (should not raise exception)
        generator.create_recommendations(
            self.sample_products_df,
            self.sample_reviews_df,
            mock_pdf
        )
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    def test_executive_summary_with_empty_dataframes(self):
        """Test executive summary generation with empty dataframes."""
        # Arrange
        generator = ReportGenerator()
        empty_products = pd.DataFrame()
        empty_reviews = pd.DataFrame()
        
        # Act
        summary = generator.generate_executive_summary(empty_products, empty_reviews)
        
        # Assert
        self.assertIsInstance(summary, str)
        self.assertIn("0 products", summary)
        self.assertIn("0 customer reviews", summary)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_price_trend_analysis_single_brand(self, mock_close, mock_figure):
        """Test price trend analysis with single brand data."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        single_brand_df = self.sample_products_df[self.sample_products_df['Brand'] == 'Dell']
        
        # Act (should not raise exception)
        generator.create_price_trend_analysis(single_brand_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.close')
    def test_create_sentiment_analysis_section_no_brand_column(self, mock_close, mock_figure):
        """Test sentiment analysis section when Brand column is missing."""
        # Arrange
        generator = ReportGenerator()
        mock_pdf = Mock()
        no_brand_df = self.sample_reviews_df.drop('Brand', axis=1)
        
        # Act (should not raise exception)
        generator.create_sentiment_analysis_section(no_brand_df, mock_pdf)
        
        # Assert - no exception should be raised
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main() 