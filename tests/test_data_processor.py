"""
Unit tests for DataProcessor class

Tests for data processing and analysis functionality including:
- Data loading from JSON files
- Product summary creation and brand analysis
- Specifications comparison
- Review sentiment analysis
- Visualization generation
- Excel report creation
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import pandas as pd
import numpy as np

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_processor import DataProcessor
import config


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Mock config paths to use test directory
        self.config_patcher = patch.multiple(
            config,
            DATA_DIR=Path(self.test_dir) / "data",
            REPORTS_DIR=Path(self.test_dir) / "reports"
        )
        self.config_patcher.start()
        
        # Create test directories
        (Path(self.test_dir) / "data").mkdir(parents=True, exist_ok=True)
        (Path(self.test_dir) / "reports").mkdir(parents=True, exist_ok=True)
        
        # Sample test data
        self.sample_data = [
            {
                "product_name": "Dell XPS 13",
                "product_price": "$999.00",
                "product_url": "https://example.com/dell-xps-13",
                "product_specs": {
                    "brand": "Dell",
                    "model": "XPS 13",
                    "screen_size": "13.3 inches",
                    "screen_resolution": "1920x1080",
                    "processor": "Intel i5"
                },
                "reviews": [
                    {
                        "title": "Great laptop!",
                        "description": "This laptop is amazing for work and daily tasks."
                    },
                    {
                        "title": "Good performance",
                        "description": "Fast processor and good build quality."
                    }
                ]
            },
            {
                "product_name": "HP Pavilion 15",
                "product_price": "$599.99",
                "product_url": "https://example.com/hp-pavilion-15", 
                "product_specs": {
                    "brand": "HP",
                    "model": "Pavilion 15",
                    "screen_size": "15.6 inches",
                    "screen_resolution": "1366x768",
                    "processor": "AMD Ryzen 5"
                },
                "reviews": [
                    {
                        "title": "Decent laptop",
                        "description": "Average performance but good value for money."
                    }
                ]
            }
        ]
        
    def tearDown(self):
        """Clean up test environment."""
        self.config_patcher.stop()
        
        # Clean up temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_data_processor_initialization(self, mock_nltk, mock_sia):
        """Test DataProcessor initialization."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        # Act
        processor = DataProcessor()
        
        # Assert
        self.assertIsNotNone(processor.logger)
        self.assertIsNotNone(processor.config)
        self.assertTrue(processor.data_dir.exists())
        self.assertTrue(processor.reports_dir.exists())
        self.assertIsNotNone(processor.sia)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_data_processor_initialization_ssl_failure(self, mock_nltk, mock_sia):
        """Test DataProcessor initialization with SSL/NLTK failure."""
        # Arrange
        mock_nltk.download.side_effect = Exception("Download failed")
        mock_sia.side_effect = Exception("Analyzer failed")
        
        # Act
        processor = DataProcessor()
        
        # Assert
        self.assertIsNone(processor.sia)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_load_product_data_success(self, mock_nltk, mock_sia):
        """Test successful product data loading."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Create test JSON file
        test_file = processor.data_dir / "test_data.json"
        with open(test_file, 'w') as f:
            json.dump(self.sample_data, f)
        
        # Act
        result = processor.load_product_data("test_data.json")
        
        # Assert
        self.assertEqual(result, self.sample_data)
        self.assertEqual(len(result), 2)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_load_product_data_file_not_found(self, mock_nltk, mock_sia):
        """Test product data loading with missing file."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            processor.load_product_data("nonexistent.json")
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_load_product_data_invalid_json(self, mock_nltk, mock_sia):
        """Test product data loading with invalid JSON."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Create invalid JSON file
        test_file = processor.data_dir / "invalid.json"
        with open(test_file, 'w') as f:
            f.write("invalid json content")
        
        # Act & Assert
        with self.assertRaises(json.JSONDecodeError):
            processor.load_product_data("invalid.json")
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_load_product_data_empty_file(self, mock_nltk, mock_sia):
        """Test product data loading with empty file."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Create empty JSON file
        test_file = processor.data_dir / "empty.json"
        with open(test_file, 'w') as f:
            json.dump([], f)
        
        # Act & Assert
        with self.assertRaises(ValueError):
            processor.load_product_data("empty.json")
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_create_product_summary_success(self, mock_nltk, mock_sia):
        """Test successful product summary creation."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Act
        df_products, pivot_brand = processor.create_product_summary(self.sample_data)
        
        # Assert
        self.assertFalse(df_products.empty)
        self.assertEqual(len(df_products), 2)
        self.assertIn("Product Name", df_products.columns)
        self.assertIn("Brand", df_products.columns)
        self.assertIn("Price", df_products.columns)
        
        # Check price conversion
        self.assertEqual(df_products.iloc[0]["Price"], 999.0)
        self.assertEqual(df_products.iloc[1]["Price"], 599.99)
        
        # Check pivot table
        self.assertFalse(pivot_brand.empty)
        self.assertIn("Average Price", pivot_brand.columns)
        self.assertIn("Product Count", pivot_brand.columns)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_create_product_summary_empty_data(self, mock_nltk, mock_sia):
        """Test product summary creation with empty data."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Act
        df_products, pivot_brand = processor.create_product_summary([])
        
        # Assert
        self.assertTrue(df_products.empty)
        self.assertTrue(pivot_brand.empty)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_create_specs_comparison_success(self, mock_nltk, mock_sia):
        """Test successful specs comparison creation."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        df_products, _ = processor.create_product_summary(self.sample_data)
        
        # Act
        df_specs = processor.create_specs_comparison(df_products)
        
        # Assert
        self.assertFalse(df_specs.empty)
        expected_cols = ["Product Name", "Brand", "Model", "Screen Size", 
                        "Screen Resolution", "Processor", "Price"]
        for col in expected_cols:
            self.assertIn(col, df_specs.columns)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_analyze_reviews_success(self, mock_nltk, mock_sia):
        """Test successful review sentiment analysis."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.7}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Act
        df_reviews, agg = processor.analyze_reviews(self.sample_data)
        
        # Assert
        self.assertFalse(df_reviews.empty)
        self.assertEqual(len(df_reviews), 3)  # Total number of reviews
        self.assertIn("Product Name", df_reviews.columns)
        self.assertIn("Sentiment", df_reviews.columns)
        
        # Check aggregated data
        self.assertFalse(agg.empty)
        self.assertIn("Review_Count", agg.columns)
        self.assertIn("Avg_Sentiment", agg.columns)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_analyze_reviews_no_analyzer(self, mock_nltk, mock_sia):
        """Test review analysis without sentiment analyzer."""
        # Arrange
        mock_sia.side_effect = Exception("Failed to initialize")
        processor = DataProcessor()
        
        # Act
        df_reviews, agg = processor.analyze_reviews(self.sample_data)
        
        # Assert
        self.assertTrue(df_reviews.empty)
        self.assertTrue(agg.empty)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_analyze_reviews_no_reviews(self, mock_nltk, mock_sia):
        """Test review analysis with no reviews in data."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Create data without reviews
        data_no_reviews = [
            {
                "product_name": "Test Product",
                "product_price": "$500.00",
                "product_specs": {"brand": "Test"},
                "reviews": []
            }
        ]
        
        # Act
        df_reviews, agg = processor.analyze_reviews(data_no_reviews)
        
        # Assert
        self.assertTrue(df_reviews.empty)
        self.assertTrue(agg.empty)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.show')
    def test_create_visualizations_success(self, mock_show, mock_savefig, mock_nltk, mock_sia):
        """Test successful visualization creation."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        df_reviews, _ = processor.analyze_reviews(self.sample_data)
        
        # Act
        processor.create_visualizations(df_reviews)
        
        # Assert
        # Should call savefig for each chart
        self.assertGreater(mock_savefig.call_count, 0)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_create_visualizations_empty_data(self, mock_nltk, mock_sia):
        """Test visualization creation with empty data."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        empty_df = pd.DataFrame()
        
        # Act (should not raise exception)
        processor.create_visualizations(empty_df)
        
        # Assert - no exception should be raised
        self.assertTrue(True)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    @patch('pandas.ExcelWriter')
    def test_save_excel_report_success(self, mock_excel_writer, mock_nltk, mock_sia):
        """Test successful Excel report saving."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        df_products, pivot_brand = processor.create_product_summary(self.sample_data)
        df_specs = processor.create_specs_comparison(df_products)
        df_reviews, agg = processor.analyze_reviews(self.sample_data)
        
        # Mock the ExcelWriter context manager
        mock_writer = Mock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Act
        result = processor.save_excel_report(df_products, pivot_brand, df_specs, df_reviews, agg)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(str(result).endswith('.xlsx'))
        mock_excel_writer.assert_called_once()
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    @patch('pandas.ExcelWriter')
    def test_save_excel_report_exception(self, mock_excel_writer, mock_nltk, mock_sia):
        """Test Excel report saving with exception."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        df_products, pivot_brand = processor.create_product_summary(self.sample_data)
        df_specs = processor.create_specs_comparison(df_products)
        df_reviews, agg = processor.analyze_reviews(self.sample_data)
        
        # Mock ExcelWriter to raise exception
        mock_excel_writer.side_effect = Exception("Excel write failed")
        
        # Act
        result = processor.save_excel_report(df_products, pivot_brand, df_specs, df_reviews, agg)
        
        # Assert
        self.assertIsNone(result)
    
    @patch('data_processor.SentimentIntensityAnalyzer')
    @patch('data_processor.nltk')
    def test_process_all_data_success(self, mock_nltk, mock_sia):
        """Test successful complete data processing."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Create test JSON file
        test_file = processor.data_dir / "test_data.json"
        with open(test_file, 'w') as f:
            json.dump(self.sample_data, f)
        
        # Mock the save_excel_report method to avoid file operations
        with patch.object(processor, 'save_excel_report', return_value="test_report.xlsx"), \
             patch.object(processor, 'create_visualizations'):
            
            # Act
            result = processor.process_all_data("test_data.json")
            
            # Assert
            self.assertTrue(result)
    
    @patch('data_processor.SentimentIntensityAnalyzer') 
    @patch('data_processor.nltk')
    def test_process_all_data_no_file(self, mock_nltk, mock_sia):
        """Test complete data processing with missing file."""
        # Arrange
        mock_analyzer = Mock()
        mock_analyzer.polarity_scores.return_value = {"compound": 0.5}
        mock_sia.return_value = mock_analyzer
        
        processor = DataProcessor()
        
        # Act
        result = processor.process_all_data("nonexistent.json")
        
        # Assert
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main() 