"""
Unit tests for DashboardGenerator class

Tests for interactive dashboard generation functionality including:
- Price comparison chart creation
- Sentiment trends visualization
- Brand performance metrics
- Sentiment distribution charts
- Complete dashboard generation
- HTML output creation
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

from dashboard_generator import DashboardGenerator
import config


class TestDashboardGenerator(unittest.TestCase):
    """Test cases for DashboardGenerator class."""
    
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
    
    def test_dashboard_generator_initialization(self):
        """Test DashboardGenerator initialization."""
        # Act
        generator = DashboardGenerator()
        
        # Assert
        self.assertIsNotNone(generator.logger)
        self.assertIsNotNone(generator.config)
        self.assertTrue(generator.reports_dir.exists())
    
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.graph_objects.Box')
    def test_create_price_comparison_chart_success(self, mock_box, mock_figure):
        """Test successful price comparison chart creation."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        
        # Act
        result = generator.create_price_comparison_chart(self.sample_products_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_figure.assert_called_once()
        mock_fig.add_trace.assert_called()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_price_comparison_chart_exception(self, mock_figure):
        """Test price comparison chart creation with exception."""
        # Arrange
        generator = DashboardGenerator()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act
        result = generator.create_price_comparison_chart(self.sample_products_df)
        
        # Assert
        # Should return empty figure on exception
        mock_figure.assert_called()
    
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.graph_objects.Scatter')
    @patch('pandas.merge')
    def test_create_sentiment_trends_chart_success(self, mock_merge, mock_scatter, mock_figure):
        """Test successful sentiment trends chart creation."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        
        # Mock merged dataframe
        sentiment_trend = pd.DataFrame([
            {"Product Name": "Dell XPS 13", "Sentiment": 0.7, "Brand": "Dell"},
            {"Product Name": "HP Pavilion 15", "Sentiment": 0.4, "Brand": "HP"}
        ])
        mock_merge.return_value = sentiment_trend
        
        # Act
        result = generator.create_sentiment_trends_chart(self.sample_reviews_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_figure.assert_called_once()
        mock_fig.add_trace.assert_called()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_sentiment_trends_chart_empty_data(self, mock_figure):
        """Test sentiment trends chart creation with empty data."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        empty_df = pd.DataFrame()
        
        # Act
        result = generator.create_sentiment_trends_chart(empty_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_sentiment_trends_chart_exception(self, mock_figure):
        """Test sentiment trends chart creation with exception."""
        # Arrange
        generator = DashboardGenerator()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act
        result = generator.create_sentiment_trends_chart(self.sample_reviews_df)
        
        # Assert
        # Should return empty figure on exception
        mock_figure.assert_called()
    
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.graph_objects.Bar')
    @patch('pandas.merge')
    def test_create_brand_performance_chart_success(self, mock_merge, mock_bar, mock_figure):
        """Test successful brand performance chart creation."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        
        # Mock merged dataframe
        brand_perf = pd.DataFrame([
            {"Brand": "Dell", "Avg_Price": 724.5, "Product_Count": 2, "Avg_Sentiment": 0.25},
            {"Brand": "HP", "Avg_Price": 599.99, "Product_Count": 1, "Avg_Sentiment": 0.4}
        ])
        mock_merge.return_value = brand_perf
        
        # Act
        result = generator.create_brand_performance_chart(
            self.sample_products_df, 
            self.sample_reviews_df
        )
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_figure.assert_called_once()
        mock_fig.add_trace.assert_called()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.graph_objects.Bar')
    def test_create_brand_performance_chart_no_reviews(self, mock_bar, mock_figure):
        """Test brand performance chart creation with no review data."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        empty_reviews = pd.DataFrame()
        
        # Act
        result = generator.create_brand_performance_chart(
            self.sample_products_df, 
            empty_reviews
        )
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_figure.assert_called_once()
        mock_fig.add_trace.assert_called()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_brand_performance_chart_exception(self, mock_figure):
        """Test brand performance chart creation with exception."""
        # Arrange
        generator = DashboardGenerator()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act
        result = generator.create_brand_performance_chart(
            self.sample_products_df,
            self.sample_reviews_df
        )
        
        # Assert
        # Should return empty figure on exception
        mock_figure.assert_called()
    
    @patch('plotly.graph_objects.Figure')
    @patch('plotly.graph_objects.Pie')
    def test_create_sentiment_distribution_chart_success(self, mock_pie, mock_figure):
        """Test successful sentiment distribution chart creation."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        
        # Act
        result = generator.create_sentiment_distribution_chart(self.sample_reviews_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_figure.assert_called_once()
        mock_pie.assert_called_once()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_sentiment_distribution_chart_empty_data(self, mock_figure):
        """Test sentiment distribution chart creation with empty data."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        empty_df = pd.DataFrame()
        
        # Act
        result = generator.create_sentiment_distribution_chart(empty_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_sentiment_distribution_chart_exception(self, mock_figure):
        """Test sentiment distribution chart creation with exception."""
        # Arrange
        generator = DashboardGenerator()
        mock_figure.side_effect = Exception("Chart creation failed")
        
        # Act
        result = generator.create_sentiment_distribution_chart(self.sample_reviews_df)
        
        # Assert
        # Should return empty figure on exception
        mock_figure.assert_called()
    
    @patch.object(DashboardGenerator, 'create_price_comparison_chart')
    @patch.object(DashboardGenerator, 'create_sentiment_trends_chart')
    @patch.object(DashboardGenerator, 'create_brand_performance_chart')
    @patch.object(DashboardGenerator, 'create_sentiment_distribution_chart')
    def test_create_comprehensive_dashboard_success(self, mock_sentiment_dist, 
                                                   mock_brand_perf, mock_sentiment_trends,
                                                   mock_price_comp):
        """Test successful comprehensive dashboard creation."""
        # Arrange
        generator = DashboardGenerator()
        
        # Mock chart returns
        mock_price_comp.return_value = Mock()
        mock_sentiment_trends.return_value = Mock()
        mock_brand_perf.return_value = Mock()
        mock_sentiment_dist.return_value = Mock()
        
        # Act
        result = generator.create_comprehensive_dashboard(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNotNone(result)
        mock_price_comp.assert_called_once()
        mock_sentiment_trends.assert_called_once()
        mock_brand_perf.assert_called_once()
        mock_sentiment_dist.assert_called_once()
    
    @patch.object(DashboardGenerator, 'create_comprehensive_dashboard')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_generate_dashboard_success(self, mock_open, mock_comprehensive):
        """Test successful dashboard generation and HTML file creation."""
        # Arrange
        generator = DashboardGenerator()
        mock_html_content = "<html><body>Test Dashboard</body></html>"
        mock_comprehensive.return_value = mock_html_content
        
        # Act
        result = generator.generate_dashboard(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(str(result).endswith('.html'))
        mock_comprehensive.assert_called_once()
        mock_open.assert_called_once()
    
    @patch.object(DashboardGenerator, 'create_comprehensive_dashboard')
    def test_generate_dashboard_exception(self, mock_comprehensive):
        """Test dashboard generation with exception."""
        # Arrange
        generator = DashboardGenerator()
        mock_comprehensive.side_effect = Exception("Dashboard creation failed")
        
        # Act
        result = generator.generate_dashboard(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNone(result)
    
    @patch('plotly.graph_objects.Figure')
    def test_create_price_comparison_chart_single_brand(self, mock_figure):
        """Test price comparison chart creation with single brand."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        single_brand_df = self.sample_products_df[self.sample_products_df['Brand'] == 'Dell']
        
        # Act
        result = generator.create_price_comparison_chart(single_brand_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_fig.add_trace.assert_called()
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_price_comparison_chart_empty_data(self, mock_figure):
        """Test price comparison chart creation with empty data."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        empty_df = pd.DataFrame()
        
        # Act
        result = generator.create_price_comparison_chart(empty_df)
        
        # Assert
        self.assertEqual(result, mock_fig)
        mock_fig.update_layout.assert_called_once()
    
    @patch('plotly.graph_objects.Figure')
    @patch('pandas.merge')
    def test_create_sentiment_trends_chart_merge_failure(self, mock_merge, mock_figure):
        """Test sentiment trends chart creation when merge fails."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        mock_merge.side_effect = Exception("Merge failed")
        
        # Act
        result = generator.create_sentiment_trends_chart(self.sample_reviews_df)
        
        # Assert
        # Should return empty figure on exception
        mock_figure.assert_called()
    
    @patch('plotly.graph_objects.Figure')
    def test_create_brand_performance_chart_empty_products(self, mock_figure):
        """Test brand performance chart creation with empty products data."""
        # Arrange
        generator = DashboardGenerator()
        mock_fig = Mock()
        mock_figure.return_value = mock_fig
        empty_products = pd.DataFrame()
        
        # Act
        result = generator.create_brand_performance_chart(
            empty_products,
            self.sample_reviews_df
        )
        
        # Assert
        # Should handle empty data gracefully
        mock_figure.assert_called()
    
    @patch.object(DashboardGenerator, 'create_price_comparison_chart')
    @patch.object(DashboardGenerator, 'create_sentiment_trends_chart')
    @patch.object(DashboardGenerator, 'create_brand_performance_chart')
    @patch.object(DashboardGenerator, 'create_sentiment_distribution_chart')
    def test_create_comprehensive_dashboard_chart_failure(self, mock_sentiment_dist, 
                                                         mock_brand_perf, mock_sentiment_trends,
                                                         mock_price_comp):
        """Test comprehensive dashboard creation when individual charts fail."""
        # Arrange
        generator = DashboardGenerator()
        
        # Mock some charts to fail
        mock_price_comp.side_effect = Exception("Price chart failed")
        mock_sentiment_trends.return_value = Mock()
        mock_brand_perf.return_value = Mock()
        mock_sentiment_dist.return_value = Mock()
        
        # Act
        result = generator.create_comprehensive_dashboard(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        # Should still return a dashboard even if some charts fail
        self.assertIsNotNone(result)
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_generate_dashboard_file_write_failure(self, mock_open):
        """Test dashboard generation when file writing fails."""
        # Arrange
        generator = DashboardGenerator()
        mock_open.side_effect = IOError("File write failed")
        
        # Act
        result = generator.generate_dashboard(
            self.sample_products_df,
            self.sample_pivot_brand,
            self.sample_reviews_df,
            self.sample_agg
        )
        
        # Assert
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main() 