"""
Pytest configuration and shared fixtures for Scrantenna testing.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime, timedelta


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_news_article():
    """Sample news article for testing."""
    return {
        "title": "Mayor Cognetti Announces New Infrastructure Project in Scranton",
        "description": "Scranton Mayor Paige Cognetti announced a $2 million infrastructure improvement project targeting Providence Road. The project will improve drainage and road conditions for residents.",
        "content": "Scranton Mayor Paige Cognetti announced a $2 million infrastructure improvement project targeting Providence Road...",
        "url": "https://example.com/news/infrastructure-project",
        "urlToImage": "https://example.com/images/project.jpg",
        "publishedAt": "2025-06-26T10:00:00Z",
        "source": {
            "id": "local-news",
            "name": "Local News Source"
        }
    }


@pytest.fixture
def sample_news_response():
    """Sample NewsAPI response for testing."""
    return {
        "status": "ok",
        "totalResults": 3,
        "articles": [
            {
                "title": "Mayor Cognetti Announces New Infrastructure Project",
                "description": "Scranton Mayor announces infrastructure improvements.",
                "content": "Full article content here...",
                "url": "https://example.com/news/1",
                "urlToImage": "https://example.com/images/1.jpg",
                "publishedAt": "2025-06-26T10:00:00Z",
                "source": {"id": "source1", "name": "Local News"}
            },
            {
                "title": "City Council Meeting Scheduled for Next Week",
                "description": "Important municipal matters to be discussed.",
                "content": "The city council will meet...",
                "url": "https://example.com/news/2",
                "urlToImage": "https://example.com/images/2.jpg",
                "publishedAt": "2025-06-25T15:30:00Z",
                "source": {"id": "source2", "name": "City Newsletter"}
            },
            {
                "title": "Local Business Receives State Recognition",
                "description": "Downtown business honored for community service.",
                "content": "A local business has been recognized...",
                "url": "https://example.com/news/3",
                "urlToImage": "https://example.com/images/3.jpg",
                "publishedAt": "2025-06-24T09:15:00Z",
                "source": {"id": "source3", "name": "Business Journal"}
            }
        ]
    }


@pytest.fixture
def sample_entities():
    """Sample extracted entities for testing."""
    return [
        {"name": "Paige Cognetti", "type": "PERSON", "confidence": 0.95},
        {"name": "Scranton", "type": "LOCATION", "confidence": 0.98},
        {"name": "Providence Road", "type": "LOCATION", "confidence": 0.85},
        {"name": "City Hall", "type": "ORGANIZATION", "confidence": 0.90},
        {"name": "Infrastructure Project", "type": "EVENT", "confidence": 0.80}
    ]


@pytest.fixture
def sample_relationships():
    """Sample extracted relationships for testing."""
    return [
        {"from": "Paige Cognetti", "to": "Scranton", "type": "MAYOR_OF"},
        {"from": "Infrastructure Project", "to": "Providence Road", "type": "LOCATED_AT"},
        {"from": "Paige Cognetti", "to": "Infrastructure Project", "type": "ANNOUNCED"}
    ]


@pytest.fixture
def sample_shorts_data():
    """Sample shorts data for testing."""
    return {
        "generated_at": "2025-06-26T16:38:59.186034",
        "source_file": "../data/daily/scranton_news_2025-06-25.json",
        "total_shorts": 3,
        "total_duration": 30,
        "has_svo": True,
        "shorts": [
            {
                "id": "short_0",
                "title": "Mayor Announces Infrastructure Project",
                "title_distilled": "Mayor announces road improvements.",
                "description": "Scranton Mayor Paige Cognetti announced improvements.",
                "description_distilled": "Mayor announces project.",
                "content": "Full content here...",
                "content_distilled": "Mayor announces road project.",
                "graph": {
                    "entities": [
                        {"name": "Paige Cognetti", "type": "PERSON"},
                        {"name": "Scranton", "type": "LOCATION"}
                    ],
                    "relationships": [
                        {"from": "Paige Cognetti", "to": "Scranton", "type": "MAYOR_OF"}
                    ],
                    "svg": "<svg>...</svg>"
                },
                "source": "Local News",
                "publishedAt": "2025-06-26T10:00:00Z",
                "url": "https://example.com/news/1",
                "duration": 10000,
                "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
            }
        ]
    }


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Mayor announces road improvements."
    return mock_response


@pytest.fixture
def mock_ollama_response():
    """Mock Ollama API response for testing."""
    return {
        'response': '[{"name": "Paige Cognetti", "type": "PERSON"}, {"name": "Scranton", "type": "LOCATION"}]'
    }


@pytest.fixture
def mock_newsapi_client():
    """Mock NewsAPI client for testing."""
    with patch('newsapi.NewsApiClient') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_file_system(temp_dir):
    """Set up mock file system structure for testing."""
    # Create directory structure
    data_dir = temp_dir / "data" / "daily"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    shorts_dir = temp_dir / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample data files
    sample_news_file = data_dir / "scranton_news_2025-06-25.json"
    with open(sample_news_file, 'w') as f:
        json.dump({
            "articles": [
                {
                    "title": "Test Article",
                    "description": "Test description",
                    "publishedAt": "2025-06-25T10:00:00Z",
                    "source": {"name": "Test Source"}
                }
            ]
        }, f)
    
    return {
        "temp_dir": temp_dir,
        "data_dir": data_dir,
        "shorts_dir": shorts_dir,
        "sample_news_file": sample_news_file
    }


@pytest.fixture
def mock_dates():
    """Provide consistent dates for testing."""
    return {
        "today": datetime(2025, 6, 26, 12, 0, 0),
        "yesterday": datetime(2025, 6, 25, 12, 0, 0),
        "week_ago": datetime(2025, 6, 19, 12, 0, 0)
    }


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    import os
    # Store original environment
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def capture_logs(caplog):
    """Capture logs with appropriate level."""
    import logging
    caplog.set_level(logging.INFO)
    return caplog


# Markers for test categorization
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )


# Test data generators
def generate_large_dataset(size=100):
    """Generate large dataset for performance testing."""
    articles = []
    for i in range(size):
        articles.append({
            "title": f"Test Article {i}",
            "description": f"Test description for article {i}",
            "content": f"Full content for test article {i}",
            "url": f"https://example.com/news/{i}",
            "publishedAt": (datetime.now() - timedelta(days=i)).isoformat() + "Z",
            "source": {"name": f"Source {i % 5}"}
        })
    return {"articles": articles}


# Custom assertions
def assert_valid_json_structure(data, expected_keys):
    """Assert that data has valid JSON structure with expected keys."""
    assert isinstance(data, dict), "Data should be a dictionary"
    for key in expected_keys:
        assert key in data, f"Missing required key: {key}"


def assert_valid_entity(entity):
    """Assert that entity has valid structure."""
    required_keys = ["name", "type"]
    assert_valid_json_structure(entity, required_keys)
    assert len(entity["name"]) > 0, "Entity name should not be empty"
    assert entity["type"] in ["PERSON", "ORGANIZATION", "LOCATION", "EVENT", "OTHER"], \
        f"Invalid entity type: {entity['type']}"


def assert_valid_relationship(relationship):
    """Assert that relationship has valid structure."""
    required_keys = ["from", "to", "type"]
    assert_valid_json_structure(relationship, required_keys)
    assert len(relationship["from"]) > 0, "Relationship 'from' should not be empty"
    assert len(relationship["to"]) > 0, "Relationship 'to' should not be empty"


def assert_valid_svg(svg_content):
    """Assert that SVG content is valid."""
    assert svg_content.startswith('<svg'), "SVG should start with <svg tag"
    assert svg_content.endswith('</svg>'), "SVG should end with </svg> tag"
    assert 'viewBox' in svg_content, "SVG should have viewBox attribute"