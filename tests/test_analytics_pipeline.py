"""
Unit tests for AnalyticsPipeline class

Tests for the main pipeline orchestrator including:
- Initialization and setup
- Directory creation
- Logging configuration
- Pipeline execution methods
- Error handling and fallback mechanisms
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import logging

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analytics_pipeline import AnalyticsPipeline
import config


class TestAnalyticsPipeline(unittest.TestCase):
    """Test cases for AnalyticsPipeline class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        
        # Mock config paths to use test directory
        self.config_patcher = patch.multiple(
            config,
            DATA_DIR=Path(self.test_dir) / "data",
            LOGS_DIR=Path(self.test_dir) / "logs", 
            REPORTS_DIR=Path(self.test_dir) / "reports"
        )
        self.config_patcher.start()
        
        # Change to test directory
        Path(self.test_dir).mkdir(exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        self.config_patcher.stop()
        
        # Clean up temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    @patch('analytics_pipeline.DataProcessor')
    @patch('analytics_pipeline.ReportGenerator') 
    @patch('analytics_pipeline.DashboardGenerator')
    def test_pipeline_initialization(self, mock_dashboard, mock_report, mock_data):
        """Test pipeline initialization with mocked components."""
        # Arrange
        mock_data.return_value = Mock()
        mock_report.return_value = Mock()
        mock_dashboard.return_value = Mock()
        
        # Act
        pipeline = AnalyticsPipeline()
        
        # Assert
        self.assertIsNotNone(pipeline.config)
        self.assertIsNotNone(pipeline.logger)
        self.assertIsNotNone(pipeline.data_processor)
        self.assertIsNotNone(pipeline.report_generator)
        self.assertIsNotNone(pipeline.dashboard_generator)
        self.assertIsNone(pipeline.extractor)
    
    def test_setup_directories(self):
        """Test that required directories are created."""
        # Arrange & Act
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Assert
        expected_dirs = ["data", "logs", "reports", "tests"]
        for directory in expected_dirs:
            dir_path = Path(directory)
            self.assertTrue(dir_path.exists(), f"Directory {directory} should exist")
    
    def test_setup_logging(self):
        """Test logging configuration."""
        # Arrange & Act
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Assert
        self.assertIsInstance(pipeline.logger, logging.Logger)
        self.assertEqual(pipeline.logger.level, logging.INFO)
        self.assertGreater(len(pipeline.logger.handlers), 0)
    
    @patch('analytics_pipeline.ECommerceAnalyzer')
    def test_initialize_extractor_success(self, mock_analyzer):
        """Test successful extractor initialization."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor.initialize_browser.return_value = True
        mock_analyzer.return_value = mock_extractor
        
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Act
        result = pipeline._initialize_extractor(headless=True)
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(pipeline.extractor, mock_extractor)
        mock_extractor.initialize_browser.assert_called_once()
    
    @patch('analytics_pipeline.ECommerceAnalyzer')
    def test_initialize_extractor_browser_failure(self, mock_analyzer):
        """Test extractor initialization with browser failure."""
        # Arrange
        mock_extractor = Mock()
        mock_extractor.initialize_browser.return_value = False
        mock_analyzer.return_value = mock_extractor
        
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Act
        result = pipeline._initialize_extractor(headless=True)
        
        # Assert
        self.assertFalse(result)
    
    @patch('analytics_pipeline.ECommerceAnalyzer')
    def test_initialize_extractor_exception(self, mock_analyzer):
        """Test extractor initialization with exception."""
        # Arrange
        mock_analyzer.side_effect = Exception("Test exception")
        
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Act
        result = pipeline._initialize_extractor(headless=True)
        
        # Assert
        self.assertFalse(result)
    
    @patch.object(AnalyticsPipeline, '_initialize_extractor')
    def test_extract_products_with_fallback_existing_data(self, mock_init):
        """Test extract_products_with_fallback with existing recent data."""
        # Arrange
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        # Create mock data file
        data_file = config.DATA_DIR / config.OUTPUT_CONFIG["json_filename"]
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.touch()
        
        # Mock recent file (less than 24 hours old)
        with patch('time.time', return_value=1000), \
             patch.object(data_file, 'stat') as mock_stat:
            mock_stat.return_value.st_mtime = 999  # 1 second ago
            
            # Act
            result = pipeline.extract_products_with_fallback()
            
            # Assert
            self.assertTrue(result)
            mock_init.assert_not_called()
    
    @patch.object(AnalyticsPipeline, '_initialize_extractor')
    @patch.object(AnalyticsPipeline, 'run_complete_analysis')
    def test_run_complete_analysis_with_extraction_success(self, mock_run_analysis, mock_init):
        """Test successful complete analysis with extraction."""
        # Arrange
        mock_init.return_value = True
        mock_run_analysis.return_value = True
        
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        with patch.object(pipeline, 'extract_products_with_fallback', return_value=True):
            # Act
            result = pipeline.run_complete_analysis_with_extraction()
            
            # Assert
            self.assertTrue(result)
            mock_run_analysis.assert_called_once()
    
    @patch.object(AnalyticsPipeline, '_initialize_extractor')
    def test_run_complete_analysis_with_extraction_failure(self, mock_init):
        """Test complete analysis with extraction failure."""
        # Arrange
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            pipeline = AnalyticsPipeline()
        
        with patch.object(pipeline, 'extract_products_with_fallback', return_value=False):
            # Act
            result = pipeline.run_complete_analysis_with_extraction()
            
            # Assert
            self.assertFalse(result)
    
    def test_run_complete_analysis_success(self):
        """Test successful complete analysis."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.load_product_data.return_value = [{"test": "data"}]
        mock_data_processor.create_product_summary.return_value = (Mock(), Mock())
        mock_data_processor.create_specs_comparison.return_value = Mock()
        mock_data_processor.analyze_reviews.return_value = (Mock(), Mock())
        mock_data_processor.create_visualizations.return_value = None
        mock_data_processor.save_excel_report.return_value = "test_report.xlsx"
        
        mock_report_generator = Mock()
        mock_report_generator.generate_pdf_report.return_value = "test_report.pdf"
        
        mock_dashboard_generator = Mock()
        mock_dashboard_generator.generate_dashboard.return_value = "test_dashboard.html"
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator', return_value=mock_report_generator), \
             patch('analytics_pipeline.DashboardGenerator', return_value=mock_dashboard_generator):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_complete_analysis()
            
            # Assert
            self.assertTrue(result)
            mock_data_processor.load_product_data.assert_called_once()
            mock_data_processor.create_product_summary.assert_called_once()
            mock_report_generator.generate_pdf_report.assert_called_once()
            mock_dashboard_generator.generate_dashboard.assert_called_once()
    
    def test_run_complete_analysis_no_data(self):
        """Test complete analysis with no data available."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.load_product_data.return_value = None
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_complete_analysis()
            
            # Assert
            self.assertFalse(result)
    
    def test_run_extraction_only_success(self):
        """Test extraction only mode success."""
        # Arrange
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            with patch.object(pipeline, 'extract_products_with_fallback', return_value=True):
                # Act
                result = pipeline.run_extraction_only()
                
                # Assert
                self.assertTrue(result)
    
    def test_run_extraction_only_failure(self):
        """Test extraction only mode failure."""
        # Arrange
        with patch('analytics_pipeline.DataProcessor'), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            with patch.object(pipeline, 'extract_products_with_fallback', return_value=False):
                # Act
                result = pipeline.run_extraction_only()
                
                # Assert
                self.assertFalse(result)
    
    def test_run_data_processing_only_success(self):
        """Test data processing only mode success."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.process_all_data.return_value = True
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_data_processing_only()
            
            # Assert
            self.assertTrue(result)
            mock_data_processor.process_all_data.assert_called_once_with(None)
    
    def test_run_data_processing_only_exception(self):
        """Test data processing only mode with exception."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.process_all_data.side_effect = Exception("Test exception")
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_data_processing_only()
            
            # Assert
            self.assertFalse(result)
    
    def test_run_report_generation_only_success(self):
        """Test report generation only mode success."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.load_product_data.return_value = [{"test": "data"}]
        mock_data_processor.create_product_summary.return_value = (Mock(), Mock())
        mock_data_processor.analyze_reviews.return_value = (Mock(), Mock())
        
        mock_report_generator = Mock()
        mock_report_generator.generate_pdf_report.return_value = "test_report.pdf"
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator', return_value=mock_report_generator), \
             patch('analytics_pipeline.DashboardGenerator'):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_report_generation_only()
            
            # Assert
            self.assertTrue(result)
            mock_report_generator.generate_pdf_report.assert_called_once()
    
    def test_run_dashboard_generation_only_success(self):
        """Test dashboard generation only mode success."""
        # Arrange
        mock_data_processor = Mock()
        mock_data_processor.load_product_data.return_value = [{"test": "data"}]
        mock_data_processor.create_product_summary.return_value = (Mock(), Mock())
        mock_data_processor.analyze_reviews.return_value = (Mock(), Mock())
        
        mock_dashboard_generator = Mock()
        mock_dashboard_generator.generate_dashboard.return_value = "test_dashboard.html"
        
        with patch('analytics_pipeline.DataProcessor', return_value=mock_data_processor), \
             patch('analytics_pipeline.ReportGenerator'), \
             patch('analytics_pipeline.DashboardGenerator', return_value=mock_dashboard_generator):
            
            pipeline = AnalyticsPipeline()
            
            # Act
            result = pipeline.run_dashboard_generation_only()
            
            # Assert
            self.assertTrue(result)
            mock_dashboard_generator.generate_dashboard.assert_called_once()


if __name__ == '__main__':
    unittest.main() 