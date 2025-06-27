"""
Integration tests for the complete news processing pipeline.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime


class TestNewsProcessingPipeline:
    """Integration tests for end-to-end news processing flow."""
    
    @pytest.fixture
    def pipeline_workspace(self):
        """Create a temporary workspace for pipeline testing."""
        workspace = Path(tempfile.mkdtemp())
        
        # Create directory structure
        (workspace / "data" / "daily").mkdir(parents=True)
        (workspace / "data" / "sentiment").mkdir(parents=True)
        (workspace / "data" / "graph").mkdir(parents=True)
        (workspace / "shorts").mkdir(parents=True)
        
        yield workspace
        
        # Cleanup
        shutil.rmtree(workspace)
    
    @pytest.fixture
    def mock_newsapi_response(self):
        """Mock NewsAPI response for integration testing."""
        return {
            "status": "ok",
            "totalResults": 5,
            "articles": [
                {
                    "title": "Mayor Cognetti Announces Infrastructure Improvements",
                    "description": "Scranton Mayor Paige Cognetti announced a $2 million infrastructure project for Providence Road improvements.",
                    "content": "Mayor Paige Cognetti held a press conference today to announce...",
                    "url": "https://example.com/news/infrastructure",
                    "urlToImage": "https://example.com/images/infrastructure.jpg",
                    "publishedAt": "2025-06-26T14:30:00Z",
                    "source": {
                        "id": "scranton-times",
                        "name": "Scranton Times"
                    }
                },
                {
                    "title": "Local Business Wins State Award",
                    "description": "Downtown Scranton business receives recognition for community service and innovation.",
                    "content": "A local business in downtown Scranton has been honored...",
                    "url": "https://example.com/news/business-award",
                    "urlToImage": "https://example.com/images/business.jpg",
                    "publishedAt": "2025-06-26T12:15:00Z",
                    "source": {
                        "id": "business-journal",
                        "name": "Scranton Business Journal"
                    }
                },
                {
                    "title": "City Council Meeting Scheduled",
                    "description": "Important municipal decisions will be discussed at next week's city council meeting.",
                    "content": "The Scranton City Council will convene next Tuesday...",
                    "url": "https://example.com/news/council-meeting",
                    "urlToImage": "https://example.com/images/council.jpg",
                    "publishedAt": "2025-06-25T16:45:00Z",
                    "source": {
                        "id": "city-newsletter",
                        "name": "City Newsletter"
                    }
                }
            ]
        }
    
    @patch('requests.get')
    def test_complete_pipeline_flow(self, mock_requests, pipeline_workspace, mock_newsapi_response):
        """Test the complete pipeline from news fetching to shorts generation."""
        # Mock NewsAPI response
        mock_response = Mock()
        mock_response.json.return_value = mock_newsapi_response
        mock_response.status_code = 200
        mock_requests.return_value = mock_response
        
        # Step 1: News Ingestion
        with patch('os.getcwd', return_value=str(pipeline_workspace)):
            from src.news_fetcher import fetch_scranton_news
            
            # Mock the API key
            with patch.dict('os.environ', {'NEWSAPI_KEY': 'test_api_key'}):
                news_data = fetch_scranton_news()
        
        assert news_data is not None
        assert "articles" in news_data
        assert len(news_data["articles"]) == 3
        
        # Verify news data structure
        for article in news_data["articles"]:
            assert "title" in article
            assert "description" in article
            assert "publishedAt" in article
            assert "source" in article
        
        # Step 2: Save news data to workspace
        daily_file = pipeline_workspace / "data" / "daily" / "scranton_news_2025-06-26.json"
        with open(daily_file, 'w') as f:
            json.dump(news_data, f, indent=2)
        
        assert daily_file.exists()
        
        # Step 3: Process news for distillation
        with patch('sys.path', [str(pipeline_workspace / "shorts")] + sys.path):
            # Mock LLM distillation
            with patch('shorts.generate_shorts.create_distilled_version') as mock_distill:
                mock_distill.side_effect = lambda text: f"Distilled: {text[:30]}..."
                
                # Mock entity extraction
                with patch('shorts.generate_shorts.generate_article_graph') as mock_graph:
                    mock_graph.return_value = {
                        "entities": [
                            {"name": "Paige Cognetti", "type": "PERSON"},
                            {"name": "Scranton", "type": "LOCATION"}
                        ],
                        "relationships": [
                            {"from": "Paige Cognetti", "to": "Scranton", "type": "MAYOR_OF"}
                        ],
                        "svg": "<svg><circle cx='50' cy='50' r='20' fill='#FF6B6B'/></svg>"
                    }
                    
                    from shorts.generate_shorts import generate_shorts_from_news
                    
                    # Generate shorts
                    shorts_data = generate_shorts_from_news(daily_file)
        
        # Verify shorts generation
        assert shorts_data is not None
        assert "shorts" in shorts_data
        assert shorts_data["total_shorts"] == 3
        assert len(shorts_data["shorts"]) == 3
        
        # Verify each short has required fields
        for short in shorts_data["shorts"]:
            assert "id" in short
            assert "title" in short
            assert "title_distilled" in short
            assert "content" in short
            assert "content_distilled" in short
            assert "graph" in short
            assert "background_gradient" in short
            assert "duration" in short
            
            # Verify graph structure
            graph = short["graph"]
            assert "entities" in graph
            assert "relationships" in graph
            assert "svg" in graph
            assert len(graph["entities"]) >= 0
        
        # Step 4: Save shorts data
        shorts_file = pipeline_workspace / "shorts" / "shorts_data.json"
        with open(shorts_file, 'w') as f:
            json.dump(shorts_data, f, indent=2)
        
        assert shorts_file.exists()
        
        # Verify file content integrity
        with open(shorts_file, 'r') as f:
            saved_shorts = json.load(f)
        
        assert saved_shorts["total_shorts"] == shorts_data["total_shorts"]
        assert len(saved_shorts["shorts"]) == len(shorts_data["shorts"])
    
    def test_pipeline_with_api_failure(self, pipeline_workspace):
        """Test pipeline behavior when API fails."""
        from src.news_fetcher import fetch_scranton_news
        
        # Mock API failure
        with patch('requests.get') as mock_requests:
            mock_requests.side_effect = Exception("API connection failed")
            
            with patch.dict('os.environ', {'NEWSAPI_KEY': 'test_api_key'}):
                with pytest.raises(Exception):
                    fetch_scranton_news()
    
    def test_pipeline_with_invalid_api_response(self, pipeline_workspace):
        """Test pipeline behavior with invalid API response."""
        from src.news_fetcher import fetch_scranton_news
        
        # Mock invalid API response
        with patch('requests.get') as mock_requests:
            mock_response = Mock()
            mock_response.json.return_value = {"status": "error", "message": "API key invalid"}
            mock_response.status_code = 401
            mock_requests.return_value = mock_response
            
            with patch.dict('os.environ', {'NEWSAPI_KEY': 'invalid_key'}):
                result = fetch_scranton_news()
                # Should handle error gracefully
                assert result is None or "error" in result
    
    def test_pipeline_data_persistence(self, pipeline_workspace, mock_newsapi_response):
        """Test that data persists correctly across pipeline stages."""
        # Create sample news data
        news_data = mock_newsapi_response
        daily_file = pipeline_workspace / "data" / "daily" / "scranton_news_2025-06-26.json"
        
        with open(daily_file, 'w') as f:
            json.dump(news_data, f, indent=2)
        
        # Process through shorts generation
        with patch('shorts.generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {
                "entities": [{"name": "Test", "type": "PERSON"}],
                "relationships": [],
                "svg": "<svg>test</svg>"
            }
            
            from shorts.generate_shorts import generate_shorts_from_news
            shorts_data = generate_shorts_from_news(daily_file)
        
        # Verify data integrity
        assert shorts_data["source_file"] == str(daily_file)
        assert shorts_data["total_shorts"] == len(news_data["articles"])
        
        # Verify that original article data is preserved
        for i, short in enumerate(shorts_data["shorts"]):
            original_article = news_data["articles"][i]
            assert short["title"] == original_article["title"]
            assert short["url"] == original_article["url"]
            assert short["publishedAt"] == original_article["publishedAt"]
    
    def test_pipeline_error_recovery(self, pipeline_workspace):
        """Test pipeline error recovery and partial processing."""
        # Create mixed valid/invalid news data
        mixed_news_data = {
            "articles": [
                {  # Valid article
                    "title": "Valid News Article",
                    "description": "This is a valid article with proper content.",
                    "publishedAt": "2025-06-26T14:30:00Z",
                    "source": {"name": "Valid Source"},
                    "url": "https://example.com/valid"
                },
                {  # Invalid article - missing title
                    "description": "Article without title",
                    "publishedAt": "2025-06-26T13:30:00Z",
                    "source": {"name": "Invalid Source"},
                    "url": "https://example.com/invalid1"
                },
                {  # Invalid article - missing description
                    "title": "Article Without Description",
                    "publishedAt": "2025-06-26T12:30:00Z",
                    "source": {"name": "Invalid Source"},
                    "url": "https://example.com/invalid2"
                },
                {  # Valid article
                    "title": "Another Valid Article",
                    "description": "This is another valid article with content.",
                    "publishedAt": "2025-06-26T11:30:00Z",
                    "source": {"name": "Valid Source"},
                    "url": "https://example.com/valid2"
                }
            ]
        }
        
        daily_file = pipeline_workspace / "data" / "daily" / "mixed_news.json"
        with open(daily_file, 'w') as f:
            json.dump(mixed_news_data, f, indent=2)
        
        # Process through shorts generation
        with patch('shorts.generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {
                "entities": [],
                "relationships": [],
                "svg": "<svg>empty</svg>"
            }
            
            from shorts.generate_shorts import generate_shorts_from_news
            shorts_data = generate_shorts_from_news(daily_file)
        
        # Should only process valid articles
        assert shorts_data["total_shorts"] == 2  # Only 2 valid articles
        assert len(shorts_data["shorts"]) == 2
        
        # Verify valid articles were processed
        processed_titles = [short["title"] for short in shorts_data["shorts"]]
        assert "Valid News Article" in processed_titles
        assert "Another Valid Article" in processed_titles
    
    def test_pipeline_performance_large_dataset(self, pipeline_workspace):
        """Test pipeline performance with larger dataset."""
        import time
        
        # Generate larger dataset
        large_news_data = {
            "articles": [
                {
                    "title": f"News Article {i}",
                    "description": f"Description for news article number {i} with relevant content.",
                    "content": f"Full content for article {i}...",
                    "publishedAt": f"2025-06-{26-i//10:02d}T{10+i%14:02d}:00:00Z",
                    "source": {"name": f"Source {i%5}"},
                    "url": f"https://example.com/news/{i}"
                }
                for i in range(50)  # 50 articles
            ]
        }
        
        daily_file = pipeline_workspace / "data" / "daily" / "large_news.json"
        with open(daily_file, 'w') as f:
            json.dump(large_news_data, f, indent=2)
        
        # Mock fast graph generation
        with patch('shorts.generate_shorts.generate_article_graph') as mock_graph:
            mock_graph.return_value = {
                "entities": [{"name": f"Entity", "type": "PERSON"}],
                "relationships": [],
                "svg": "<svg>fast</svg>"
            }
            
            start_time = time.time()
            
            from shorts.generate_shorts import generate_shorts_from_news
            shorts_data = generate_shorts_from_news(daily_file, max_shorts=25)
            
            end_time = time.time()
            processing_time = end_time - start_time
        
        # Performance assertions
        assert processing_time < 30  # Should complete in under 30 seconds
        assert shorts_data["total_shorts"] == 25  # Respects max_shorts limit
        assert len(shorts_data["shorts"]) == 25
    
    def test_pipeline_concurrent_safety(self, pipeline_workspace):
        """Test pipeline safety with concurrent access patterns."""
        import threading
        import queue
        
        # Create shared news data
        news_data = {
            "articles": [
                {
                    "title": f"Concurrent Article {i}",
                    "description": f"Article {i} for concurrency testing.",
                    "publishedAt": "2025-06-26T14:30:00Z",
                    "source": {"name": "Test Source"},
                    "url": f"https://example.com/concurrent/{i}"
                }
                for i in range(10)
            ]
        }
        
        daily_file = pipeline_workspace / "data" / "daily" / "concurrent_news.json"
        with open(daily_file, 'w') as f:
            json.dump(news_data, f, indent=2)
        
        results_queue = queue.Queue()
        
        def process_shorts(thread_id):
            """Process shorts in separate thread."""
            try:
                with patch('shorts.generate_shorts.generate_article_graph') as mock_graph:
                    mock_graph.return_value = {
                        "entities": [{"name": f"Entity{thread_id}", "type": "PERSON"}],
                        "relationships": [],
                        "svg": f"<svg>thread{thread_id}</svg>"
                    }
                    
                    from shorts.generate_shorts import generate_shorts_from_news
                    shorts_data = generate_shorts_from_news(daily_file)
                    results_queue.put((thread_id, shorts_data))
            except Exception as e:
                results_queue.put((thread_id, f"Error: {e}"))
        
        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=process_shorts, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)
        
        # Collect results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        
        # Verify all threads completed successfully
        assert len(results) == 3
        for thread_id, result in results:
            assert not isinstance(result, str) or not result.startswith("Error")
            if isinstance(result, dict):
                assert "shorts" in result
                assert len(result["shorts"]) > 0