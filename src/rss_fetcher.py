"""
RSS feed integration for local Scranton news sources
This supplements NewsAPI with local newspaper feeds
"""
import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import time

class RSSNewsFetcher:
    def __init__(self):
        # Local news RSS feeds for Greater Scranton area
        self.rss_feeds = {
            'times_tribune': 'https://www.thetimes-tribune.com/feed/',
            'wnep': 'https://www.wnep.com/feeds/syndication/rss/news/local/',
            'wbre': 'https://www.pahomepage.com/feed/',
            'wyou': 'https://www.pahomepage.com/feed/',  # Same as WBRE
            'electric_city': 'https://electriccitypa.com/feed/',
            # Add more local sources as available
        }
    
    def fetch_local_rss_news(self, hours_back: int = 24) -> List[Dict]:
        """
        Fetch recent news from local RSS feeds
        
        Args:
            hours_back: How many hours back to fetch articles
            
        Returns:
            List of articles in NewsAPI-compatible format
        """
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        all_articles = []
        
        for source_name, feed_url in self.rss_feeds.items():
            try:
                print(f"Fetching RSS from {source_name}: {feed_url}")
                articles = self._fetch_rss_feed(feed_url, source_name, cutoff_time)
                all_articles.extend(articles)
                time.sleep(1)  # Be respectful with requests
            except Exception as e:
                print(f"Error fetching {source_name}: {e}")
                continue
        
        print(f"Fetched {len(all_articles)} articles from RSS feeds")
        return all_articles
    
    def _fetch_rss_feed(self, feed_url: str, source_name: str, cutoff_time: datetime) -> List[Dict]:
        """
        Fetch and parse a single RSS feed
        """
        articles = []
        
        # Parse RSS feed
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print(f"Warning: RSS feed {source_name} may have issues")
        
        for entry in feed.entries:
            # Convert RSS entry to NewsAPI-compatible format
            try:
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                
                # Skip old articles
                if pub_date and pub_date < cutoff_time:
                    continue
                
                # Format article
                article = {
                    'source': {'name': source_name.replace('_', ' ').title()},
                    'title': entry.get('title', 'No title'),
                    'description': entry.get('summary', ''),
                    'url': entry.get('link', ''),
                    'publishedAt': pub_date.isoformat() if pub_date else datetime.now().isoformat(),
                    'content': entry.get('description', entry.get('summary', '')),
                    'author': entry.get('author', ''),
                    'urlToImage': self._extract_image_url(entry)
                }
                
                articles.append(article)
                
            except Exception as e:
                print(f"Error processing entry from {source_name}: {e}")
                continue
        
        return articles
    
    def _extract_image_url(self, entry) -> str:
        """
        Extract image URL from RSS entry
        """
        # Try various common image fields
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url', '')
        
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('type', '').startswith('image'):
                    return media.get('url', '')
        
        # Look in content for images
        if hasattr(entry, 'content'):
            for content in entry.content:
                if 'img src=' in content.value:
                    # Basic regex-like extraction (would need proper parsing in production)
                    pass
        
        return ''

def main():
    """
    Test RSS fetching
    """
    fetcher = RSSNewsFetcher()
    articles = fetcher.fetch_local_rss_news(hours_back=48)
    
    print(f"\nFound {len(articles)} articles:")
    for article in articles[:5]:
        print(f"- {article['title']}")
        print(f"  Source: {article['source']['name']}")
        print(f"  Published: {article['publishedAt']}")
        print()

if __name__ == "__main__":
    main()