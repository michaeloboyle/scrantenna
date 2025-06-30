"""News loading module."""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class NewsLoader:
    """Handles loading news articles from various sources."""
    
    def __init__(self, data_dir: str = "../data/daily"):
        self.data_dir = Path(data_dir)
        
    def load_latest(self) -> List[Dict[str, Any]]:
        """Load the latest news file."""
        # Find the most recent news file
        news_files = list(self.data_dir.glob("scranton_news_*.json"))
        
        if not news_files:
            raise FileNotFoundError(f"No news files found in {self.data_dir}")
        
        # Sort by filename (contains date)
        latest_file = sorted(news_files)[-1]
        return self.load_from_file(latest_file)
    
    def load_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load articles from a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different file formats
            if isinstance(data, dict):
                articles = data.get('articles', [])
            elif isinstance(data, list):
                articles = data
            else:
                raise ValueError(f"Unexpected data format in {file_path}")
            
            print(f"Loaded {len(articles)} articles from {file_path.name}")
            return articles
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []
    
    def load_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Load articles from a date range (YYYY-MM-DD format)."""
        articles = []
        
        for news_file in self.data_dir.glob("scranton_news_*.json"):
            # Extract date from filename
            try:
                date_str = news_file.stem.split('_')[-1]  # scranton_news_2025-06-25.json
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                
                if start <= file_date <= end:
                    file_articles = self.load_from_file(news_file)
                    articles.extend(file_articles)
                    
            except (ValueError, IndexError) as e:
                print(f"Skipping file with invalid date format: {news_file.name}")
                continue
        
        print(f"Loaded {len(articles)} articles from date range {start_date} to {end_date}")
        return articles
    
    def validate_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean article data."""
        valid_articles = []
        required_fields = ['title']
        
        for article in articles:
            # Check required fields
            if not all(field in article and article[field] for field in required_fields):
                continue
            
            # Clean and normalize fields
            cleaned_article = {
                'title': self._clean_text(article.get('title', '')),
                'description': self._clean_text(article.get('description', '')),
                'content': self._clean_text(article.get('content', '')),
                'url': article.get('url', ''),
                'publishedAt': article.get('publishedAt', ''),
                'source': article.get('source', {}),
                'urlToImage': article.get('urlToImage', ''),
            }
            
            # Ensure we have some content
            if (cleaned_article['title'] or 
                cleaned_article['description'] or 
                cleaned_article['content']):
                valid_articles.append(cleaned_article)
        
        print(f"Validated {len(valid_articles)} articles")
        return valid_articles
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common suffixes from scraped content
        suffixes_to_remove = [
            '... [+]',
            '[Read more]',
            '[Continue reading]',
            '...',
        ]
        
        for suffix in suffixes_to_remove:
            if text.endswith(suffix):
                text = text[:-len(suffix)].strip()
        
        return text
    
    def get_available_dates(self) -> List[str]:
        """Get list of available dates with news data."""
        dates = []
        
        for news_file in self.data_dir.glob("scranton_news_*.json"):
            try:
                date_str = news_file.stem.split('_')[-1]
                # Validate date format
                datetime.strptime(date_str, '%Y-%m-%d')
                dates.append(date_str)
            except (ValueError, IndexError):
                continue
        
        return sorted(dates)