"""
Static HTML page generator for daily Scranton news
"""
import os
import json
from datetime import datetime
from typing import Dict, List
from pathlib import Path

class StaticNewsGenerator:
    def __init__(self, template_dir: str = "templates", output_dir: str = "static"):
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_daily_page(self, news_data: Dict, date_str: str = None) -> str:
        """
        Generate static HTML page from news data
        
        Args:
            news_data: Dictionary containing articles and metadata
            date_str: Date string for the page (defaults to today)
            
        Returns:
            Path to generated HTML file
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Generate HTML content
        html_content = self._generate_html(news_data, date_str)
        
        # Save to file
        filename = f"scranton_news_{date_str}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Also generate index.html with latest news
        index_path = os.path.join(self.output_dir, "index.html")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated daily news page: {filepath}")
        return filepath
    
    def _generate_html(self, news_data: Dict, date_str: str) -> str:
        """Generate HTML content from news data"""
        articles = news_data.get('articles', [])
        total_count = news_data.get('total_results', 0)
        fetched_at = news_data.get('fetched_at', '')
        
        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            display_date = date_obj.strftime("%B %d, %Y")
        except:
            display_date = date_str
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrantenna - Greater Scranton News - {display_date}</title>
    <style>
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            background: #1a365f;
            color: white;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 8px;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: normal;
        }}
        
        .subtitle {{
            font-size: 1.2em;
            margin-top: 10px;
            opacity: 0.9;
        }}
        
        .meta-info {{
            background: white;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 8px;
            border-left: 4px solid #1a365f;
        }}
        
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .article-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }}
        
        .article-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .article-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1a365f;
        }}
        
        .article-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .article-title a:hover {{
            text-decoration: underline;
        }}
        
        .article-meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .article-description {{
            color: #333;
            margin-bottom: 15px;
        }}
        
        .article-source {{
            font-size: 0.85em;
            color: #888;
            font-style: italic;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        .no-articles {{
            text-align: center;
            padding: 50px;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>Scrantenna</h1>
        <div class="subtitle">Greater Scranton Area News</div>
    </header>
    
    <div class="meta-info">
        <strong>Daily Briefing for {display_date}</strong><br>
        {total_count} articles found • Last updated: {self._format_timestamp(fetched_at)}
    </div>
"""
        
        if articles:
            html += '<div class="articles-grid">'
            
            for article in articles:
                # Clean and format article data
                title = self._clean_text(article.get('title', 'No title'))
                description = self._clean_text(article.get('description', ''))
                url = article.get('url', '#')
                source = article.get('source', {}).get('name', 'Unknown Source')
                published_at = self._format_article_date(article.get('publishedAt', ''))
                author = article.get('author', '')
                
                html += f"""
        <article class="article-card">
            <h2 class="article-title">
                <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
            </h2>
            <div class="article-meta">
                {published_at}{' • ' + author if author else ''}
            </div>
            <div class="article-description">
                {description}
            </div>
            <div class="article-source">
                Source: {source}
            </div>
        </article>
"""
            
            html += '</div>'
        else:
            html += '<div class="no-articles">No articles found for today.</div>'
        
        html += f"""
    <footer class="footer">
        <p>Scrantenna • Knowledge graphs for community understanding</p>
        <p>Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
    </footer>
</body>
</html>"""
        
        return html
    
    def _clean_text(self, text: str) -> str:
        """Clean text for HTML display"""
        if not text:
            return ""
        return text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
    
    def _format_timestamp(self, timestamp_str: str) -> str:
        """Format ISO timestamp for display"""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%I:%M %p")
        except:
            return timestamp_str
    
    def _format_article_date(self, date_str: str) -> str:
        """Format article publication date"""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            return date_str

def main():
    """
    Example usage
    """
    # Load latest news data
    data_dir = "data/daily"
    today = datetime.now().strftime("%Y-%m-%d")
    news_file = f"{data_dir}/scranton_news_{today}.json"
    
    if os.path.exists(news_file):
        with open(news_file, 'r') as f:
            news_data = json.load(f)
        
        generator = StaticNewsGenerator()
        html_file = generator.generate_daily_page(news_data, today)
        print(f"Generated: {html_file}")
    else:
        print(f"No news data found at {news_file}")
        print("Run news_fetcher.py first to fetch today's news")

if __name__ == "__main__":
    main()