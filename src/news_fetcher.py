"""
NewsAPI integration for fetching Greater Scranton area news
"""
import os
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
from rss_fetcher import RSSNewsFetcher

class NewsFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.rss_fetcher = RSSNewsFetcher()
        
    def fetch_scranton_news(self, query_terms: List[str] = None) -> Dict:
        """
        Fetch news articles related to Greater Scranton area (Lackawanna County)
        
        Args:
            query_terms: Additional search terms beyond default Scranton queries
            
        Returns:
            Dict containing articles and metadata
        """
        if query_terms is None:
            # Focus on specific municipalities in Lackawanna County
            # Note: NewsAPI free tier may not include local papers like Times-Tribune
            query_terms = [
                '"Scranton Pennsylvania"',  # Quoted for exact phrase
                '"Lackawanna County"',
                '"Dunmore PA"',
                '"Clarks Summit Pennsylvania"',
                '"Old Forge Pennsylvania"',
                '"Taylor Pennsylvania"',
                '"Dickson City Pennsylvania"',
                '"Throop Pennsylvania"',
                '"Archbald Pennsylvania"',
                '"Jessup Pennsylvania"',
                '"Olyphant Pennsylvania"',
                '"Blakely Pennsylvania"',
                '"Carbondale Pennsylvania"',
                '"Jermyn Pennsylvania"',
                # Try some regional terms that might catch local coverage
                'NEPA Pennsylvania',
                'Northeastern Pennsylvania',
                'Scranton mayor',
                'Lackawanna County commissioners'
            ]
        
        all_articles = []
        
        # Fetch from NewsAPI
        for query in query_terms:
            articles = self._fetch_by_query(query)
            if articles:
                all_articles.extend(articles)
        
        # Fetch from local RSS feeds
        print("Fetching from local RSS feeds...")
        rss_articles = self.rss_fetcher.fetch_local_rss_news(hours_back=24)
        all_articles.extend(rss_articles)
                
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Filter articles to ensure they're actually about Greater Scranton area
        filtered_articles = self._filter_local_content(unique_articles)
                
        return {
            'articles': filtered_articles,
            'total_results': len(filtered_articles),
            'fetched_at': datetime.now().isoformat(),
            'queries': query_terms
        }
    
    def _fetch_by_query(self, query: str, page_size: int = 50) -> Optional[List[Dict]]:
        """
        Fetch articles for a specific query
        """
        params = {
            'q': query,
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': page_size
        }
        
        try:
            response = requests.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('articles', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for query '{query}': {e}")
            return None
    
    def _filter_local_content(self, articles: List[Dict]) -> List[Dict]:
        """
        Filter articles to ensure they're actually about Greater Scranton area
        """
        local_keywords = [
            # Primary cities/boroughs
            'scranton', 'dunmore', 'clarks summit', 'old forge', 'taylor',
            'dickson city', 'throop', 'archbald', 'jessup', 'olyphant',
            'blakely', 'carbondale', 'jermyn',
            # County and region
            'lackawanna county', 'nepa', 'northeastern pennsylvania',
            # Local institutions
            'university of scranton', 'marywood university', 'lackawanna college',
            'scranton school district', 'dunmore school district',
            # Local government
            'scranton mayor', 'lackawanna county commissioners',
            # Local landmarks/areas
            'steamtown', 'electric city', 'downtown scranton', 'nay aug park'
        ]
        
        # Terms that often indicate non-local content
        exclude_keywords = [
            'scranton university california',  # Different Scranton
            'scranton iowa', 'scranton north dakota', 'scranton south carolina',
            'scranton kansas', 'scranton arkansas',  # Other Scrantons
            'the office tv show', 'dunder mifflin',  # Unless it's local filming/events
        ]
        
        filtered_articles = []
        
        for article in articles:
            # Combine title, description, and content for analysis
            content_text = ' '.join([
                article.get('title', ''),
                article.get('description', ''),
                article.get('content', '')
            ]).lower()
            
            # Check for exclude keywords first
            if any(exclude_term in content_text for exclude_term in exclude_keywords):
                # Special case: allow if it mentions local Scranton context
                if not any(local_term in content_text for local_term in ['pennsylvania', 'pa', 'lackawanna']):
                    continue
            
            # Must contain at least one local keyword
            if any(local_term in content_text for local_term in local_keywords):
                filtered_articles.append(article)
        
        print(f"Filtered {len(articles)} articles down to {len(filtered_articles)} local articles")
        return filtered_articles
    
    def save_daily_news(self, output_dir: str = "data/daily") -> str:
        """
        Fetch and save today's news to a JSON file
        
        Returns:
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        news_data = self.fetch_scranton_news()
        
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"scranton_news_{today}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(news_data, f, indent=2)
            
        print(f"Saved {news_data['total_results']} articles to {filepath}")
        return filepath

def main():
    """
    Example usage - can be called directly or imported
    """
    # Use environment variable or fallback to hardcoded key
    api_key = os.getenv('NEWSAPI_KEY', 'be93936988fd4df185bd56e8a11125a0')
    
    fetcher = NewsFetcher(api_key)
    saved_file = fetcher.save_daily_news()
    print(f"Daily news saved to: {saved_file}")

if __name__ == "__main__":
    main()