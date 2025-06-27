"""
Unit tests for shorts generation functionality.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from datetime import datetime

# Import the module to test
import sys
sys.path.append('/Users/michaeloboyle/Documents/GitHub/scrantenna/shorts')
from generate_shorts import (
    clean_text,
    create_distilled_version_fallback,
    create_short_from_article,
    get_background_gradient,
    generate_shorts_from_news,
    check_if_shorts_current
)


class TestShortsGeneration:
    """Test suite for shorts generation functions."""
    
    def test_clean_text_basic(self):
        """Test basic text cleaning functionality."""
        # Test normal text
        clean = clean_text("This is a normal text.")
        assert clean == "This is a normal text."
        
        # Test text with extra whitespace
        messy_text = "This  has   extra    spaces\n\nand\tlines"
        clean = clean_text(messy_text)
        assert clean == "This has extra spaces and lines"
        
        # Test text with character count indicators
        text_with_chars = "This is text [+150 chars]"
        clean = clean_text(text_with_chars)
        assert clean == "This is text"
    
    def test_clean_text_truncation(self):
        """Test text truncation when enabled."""
        long_text = "This is a very long text that should be truncated when the truncate flag is set to True because it exceeds the 200 character limit that is defined in the function and we want to make sure this works properly."
        
        # Without truncation
        clean_no_truncate = clean_text(long_text, truncate=False)
        assert len(clean_no_truncate) > 200
        
        # With truncation
        clean_truncated = clean_text(long_text, truncate=True)
        assert len(clean_truncated) <= 200
        assert clean_truncated.endswith("...")
    
    def test_clean_text_empty_and_none(self):
        """Test handling of empty and None inputs."""
        assert clean_text("") == ""
        assert clean_text(None) == ""
        assert clean_text("   ") == ""
    
    def test_create_distilled_version_fallback(self):
        """Test fallback distillation function."""
        # Test normal article
        text = "The mayor announced a new project. This will benefit residents."
        distilled = create_distilled_version_fallback(text)
        
        assert len(distilled) > 0
        assert distilled.endswith(".")
        assert len(distilled) <= 61  # 60 chars + period
    
    def test_create_distilled_version_fallback_edge_cases(self):
        """Test fallback distillation with edge cases."""
        # Empty text
        assert create_distilled_version_fallback("") == ""
        
        # Text with parentheses
        text_with_parens = "The mayor (Paige Cognetti) announced a project."
        distilled = create_distilled_version_fallback(text_with_parens)
        assert "(" not in distilled and ")" not in distilled
        
        # Text starting with articles
        text_with_article = "The mayor announced something important."
        distilled = create_distilled_version_fallback(text_with_article)
        assert not distilled.startswith("The ")
    
    def test_get_background_gradient(self):
        """Test background gradient generation."""
        # Test that different indices give different gradients
        gradient_0 = get_background_gradient(0)
        gradient_1 = get_background_gradient(1)
        assert gradient_0 != gradient_1
        
        # Test that gradients cycle properly
        gradient_10 = get_background_gradient(10)  # Should be same as index 0
        assert gradient_10 == gradient_0
        
        # Test gradient format
        assert gradient_0.startswith("linear-gradient(")
        assert "%" in gradient_0
    
    def test_create_short_from_article(self, sample_news_article):
        """Test creation of short from article."""
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {
                "entities": [{"name": "Test", "type": "PERSON"}],
                "relationships": [],
                "svg": "<svg>test</svg>"
            }
            
            short = create_short_from_article(sample_news_article, 0)
            
            # Check required fields
            assert "id" in short
            assert short["id"] == "short_0"
            assert "title" in short
            assert "content" in short
            assert "graph" in short
            assert "duration" in short
            assert "background_gradient" in short
            
            # Check title and content are properly cleaned
            assert short["title"] == sample_news_article["title"]
            assert len(short["content"]) > 0
    
    @patch('generate_shorts.create_distilled_version')
    def test_create_short_distilled_versions(self, mock_distill, sample_news_article):
        """Test that distilled versions are created when missing."""
        mock_distill.return_value = "Distilled content"
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {"entities": [], "relationships": [], "svg": ""}
            
            # Article without distilled versions
            article_no_distilled = sample_news_article.copy()
            short = create_short_from_article(article_no_distilled, 0)
            
            # Should have called distillation function
            assert mock_distill.call_count >= 1
            assert "title_distilled" in short
            assert "content_distilled" in short
    
    def test_generate_shorts_from_news_structure(self, mock_file_system, sample_news_response):
        """Test shorts generation from news file structure."""
        # Create a temporary news file
        news_file = mock_file_system["data_dir"] / "test_news.json"
        with open(news_file, 'w') as f:
            json.dump(sample_news_response, f)
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {
                "entities": [],
                "relationships": [],
                "svg": "<svg>empty</svg>"
            }
            
            shorts_data = generate_shorts_from_news(news_file, max_shorts=3)
            
            # Check structure
            assert "generated_at" in shorts_data
            assert "source_file" in shorts_data
            assert "total_shorts" in shorts_data
            assert "shorts" in shorts_data
            
            # Check content
            assert shorts_data["total_shorts"] == 3
            assert len(shorts_data["shorts"]) == 3
            
            # Check each short has required fields
            for short in shorts_data["shorts"]:
                assert "id" in short
                assert "title" in short
                assert "content" in short
                assert "graph" in short
    
    def test_generate_shorts_filtering(self, mock_file_system):
        """Test that shorts generation filters out invalid articles."""
        # Create news with some invalid articles
        invalid_news = {
            "articles": [
                {  # Valid article
                    "title": "Valid Article Title",
                    "description": "Valid description with enough content",
                    "publishedAt": "2025-06-26T10:00:00Z"
                },
                {  # Invalid - no title
                    "description": "Description without title",
                    "publishedAt": "2025-06-26T10:00:00Z"
                },
                {  # Invalid - title too short
                    "title": "Short",
                    "description": "Description",
                    "publishedAt": "2025-06-26T10:00:00Z"
                },
                {  # Invalid - no description
                    "title": "Title without description",
                    "publishedAt": "2025-06-26T10:00:00Z"
                }
            ]
        }
        
        news_file = mock_file_system["data_dir"] / "invalid_news.json"
        with open(news_file, 'w') as f:
            json.dump(invalid_news, f)
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {"entities": [], "relationships": [], "svg": ""}
            
            shorts_data = generate_shorts_from_news(news_file)
            
            # Should only have 1 valid short
            assert shorts_data["total_shorts"] == 1
            assert shorts_data["shorts"][0]["title"] == "Valid Article Title"
    
    def test_check_if_shorts_current(self, mock_file_system):
        """Test checking if shorts are current."""
        news_file = mock_file_system["data_dir"] / "test_news.json"
        shorts_file = Path("shorts_data.json")
        
        # Test when shorts file doesn't exist
        assert check_if_shorts_current(news_file) is False
        
        # Test when shorts file exists and is current
        current_shorts_data = {
            "generated_at": datetime.now().isoformat(),
            "source_file": str(news_file)
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(current_shorts_data))):
            with patch('pathlib.Path.exists', return_value=True):
                # Mock datetime.now in the function's context
                with patch('generate_shorts.datetime') as mock_datetime:
                    mock_datetime.now.return_value = datetime.now()
                    mock_datetime.fromisoformat = datetime.fromisoformat
                    result = check_if_shorts_current(news_file)
                    assert result is True
    
    def test_check_if_shorts_current_old_data(self, mock_file_system):
        """Test that old shorts data is considered not current."""
        news_file = mock_file_system["data_dir"] / "test_news.json"
        
        # Create old shorts data (more than 1 hour ago)
        old_time = datetime.now().replace(hour=datetime.now().hour - 2)
        old_shorts_data = {
            "generated_at": old_time.isoformat(),
            "source_file": str(news_file)
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(old_shorts_data))):
            with patch('pathlib.Path.exists', return_value=True):
                with patch('generate_shorts.datetime') as mock_datetime:
                    mock_datetime.now.return_value = datetime.now()
                    mock_datetime.fromisoformat = datetime.fromisoformat
                    mock_datetime.timedelta = datetime.timedelta
                    result = check_if_shorts_current(news_file)
                    assert result is False
    
    def test_shorts_animation_delays(self, sample_news_response, mock_file_system):
        """Test that shorts have proper animation delays."""
        news_file = mock_file_system["data_dir"] / "test_news.json"
        with open(news_file, 'w') as f:
            json.dump(sample_news_response, f)
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {"entities": [], "relationships": [], "svg": ""}
            
            shorts_data = generate_shorts_from_news(news_file)
            
            # Check that animation delays are properly staggered
            for i, short in enumerate(shorts_data["shorts"]):
                expected_delay = min(i * 0.1, 1.0)
                assert short["animation_delay"] == expected_delay
    
    def test_shorts_duration_calculation(self, sample_news_response, mock_file_system):
        """Test shorts duration calculation."""
        news_file = mock_file_system["data_dir"] / "test_news.json"
        with open(news_file, 'w') as f:
            json.dump(sample_news_response, f)
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {"entities": [], "relationships": [], "svg": ""}
            
            shorts_data = generate_shorts_from_news(news_file)
            
            # Each short should have 10 second duration
            for short in shorts_data["shorts"]:
                assert short["duration"] == 10000  # 10 seconds in milliseconds
            
            # Total duration should be calculated correctly
            expected_total = len(shorts_data["shorts"]) * 8  # 8 seconds per short for total
            assert shorts_data["total_duration"] == expected_total
    
    @patch('generate_shorts.llm_available', False)
    def test_shorts_generation_without_llm(self, sample_news_response, mock_file_system):
        """Test shorts generation when LLM is not available."""
        news_file = mock_file_system["data_dir"] / "test_news.json"
        with open(news_file, 'w') as f:
            json.dump(sample_news_response, f)
        
        with patch('generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {"entities": [], "relationships": [], "svg": ""}
            
            shorts_data = generate_shorts_from_news(news_file)
            
            # Should still generate shorts successfully
            assert shorts_data["total_shorts"] > 0
            assert len(shorts_data["shorts"]) > 0
            
            # Should use fallback distillation
            for short in shorts_data["shorts"]:
                assert "title_distilled" in short
                assert "content_distilled" in short
    
    def test_error_handling_invalid_json(self, mock_file_system):
        """Test error handling for invalid JSON files."""
        # Create invalid JSON file
        invalid_file = mock_file_system["data_dir"] / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("This is not valid JSON")
        
        # Should handle the error gracefully
        with pytest.raises(json.JSONDecodeError):
            generate_shorts_from_news(invalid_file)
    
    def test_error_handling_missing_file(self):
        """Test error handling for missing files."""
        nonexistent_file = Path("/nonexistent/path/news.json")
        
        # Should handle missing file gracefully
        with pytest.raises(FileNotFoundError):
            generate_shorts_from_news(nonexistent_file)