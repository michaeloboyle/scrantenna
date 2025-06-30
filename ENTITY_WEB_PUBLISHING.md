# Entity Web Publishing & Article Linking Strategy

## Vision: Living Knowledge Web

Transform the Obsidian entity vault into a **public, searchable knowledge web** where:
- Entity pages are published as HTML with rich styling
- News articles automatically link to relevant entity pages
- Users can explore Scranton's knowledge graph through web navigation
- Entity pages become the authoritative source for local information

## Benefits Analysis

### 🌐 **Public Knowledge Access**
- **Discoverability**: Entity pages indexed by search engines
- **Accessibility**: No Obsidian required to explore knowledge
- **Shareability**: Direct links to entity information
- **SEO Value**: Rich entity pages boost search rankings

### 🔗 **Enhanced Article Experience**
- **Context Enrichment**: Click through from articles to learn about entities
- **Knowledge Discovery**: Find related articles through entity pages
- **Navigation**: Explore entity relationships and connections
- **Authority Building**: Scrantenna becomes definitive source for local knowledge

### 📊 **Analytics & Insights**
- **Popular Entities**: Track which entities get most page views
- **User Journeys**: Understand how people navigate the knowledge graph
- **Content Gaps**: Identify entities needing more information
- **Engagement**: Measure time spent exploring entity relationships

## Technical Architecture

### 📝 **Markdown → HTML Pipeline**

```
entities/*.md → entity-publisher.py → docs/entities/*.html
     ↓
- Parse YAML front matter
- Convert markdown body to HTML
- Apply entity page template
- Generate entity index pages
- Create search functionality
```

### 🔗 **Article Entity Linking**

```
articles/*.json → entity-linker.py → docs/articles/*.html
     ↓
- Extract entity mentions from article text
- Match against known entity database
- Replace entity mentions with HTML links
- Generate enhanced article pages
```

## Implementation Strategy

### Phase 1: Entity Page Publisher

```python
class EntityWebPublisher:
    def __init__(self, vault_path, output_path):
        self.vault_path = Path(vault_path)
        self.output_path = Path(output_path)
        self.entities = self._load_entities()
    
    def publish_all_entities(self):
        """Convert all entity markdown files to HTML."""
        for entity_file in self.vault_path.rglob("*.md"):
            if self._should_publish(entity_file):
                self._publish_entity(entity_file)
        
        self._generate_entity_index()
        self._generate_search_data()
    
    def _publish_entity(self, md_file):
        """Convert single entity markdown to HTML."""
        front_matter, content = self._parse_markdown(md_file)
        
        # Convert Dataview queries to static HTML
        content = self._render_dataview_queries(content, front_matter)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['tables', 'toc'])
        
        # Apply template
        html_page = self._apply_template(front_matter, html_content)
        
        # Write HTML file
        output_file = self._get_output_path(md_file)
        self._write_html_file(output_file, html_page)
```

### Phase 2: Article Entity Linking

```python
class ArticleEntityLinker:
    def __init__(self, entity_manager, base_url):
        self.entity_manager = entity_manager
        self.base_url = base_url
    
    def enhance_article(self, article_data):
        """Add entity links to article content."""
        content = article_data.get('content', '')
        
        # Find entity mentions
        entity_mentions = self._find_entity_mentions(content)
        
        # Replace with links
        enhanced_content = self._replace_with_links(content, entity_mentions)
        
        return {
            **article_data,
            'content': enhanced_content,
            'entity_links': entity_mentions
        }
    
    def _find_entity_mentions(self, text):
        """Find all entity mentions in text."""
        mentions = []
        
        for entity_name, entity_data in self.entity_manager.known_entities.items():
            # Check canonical name and aliases
            candidates = [entity_data['canonical_name']] + entity_data.get('aliases', [])
            
            for candidate in candidates:
                pattern = rf'\b{re.escape(candidate)}\b'
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    mentions.append({
                        'text': match.group(0),
                        'start': match.start(),
                        'end': match.end(),
                        'entity': entity_data['canonical_name'],
                        'type': entity_data['entity_type'],
                        'url': self._get_entity_url(entity_data['canonical_name'])
                    })
        
        return mentions
```

## HTML Template Design

### 🎨 **Entity Page Template**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{entity_name}} | Scrantenna Knowledge Base</title>
    <meta name="description" content="{{entity_bio}}">
    <meta property="og:title" content="{{entity_name}}">
    <meta property="og:description" content="{{entity_bio}}">
    <meta property="og:type" content="profile">
    <link rel="stylesheet" href="/css/entity-pages.css">
    <link rel="canonical" href="{{canonical_url}}">
</head>
<body>
    <nav class="breadcrumb">
        <a href="/">Scrantenna</a> → 
        <a href="/entities/">Entities</a> → 
        <a href="/entities/{{entity_type}}/">{{entity_type_label}}</a> → 
        <span class="current">{{entity_name}}</span>
    </nav>

    <header class="entity-header">
        <h1 class="entity-name">{{entity_name}}</h1>
        <div class="entity-meta">
            <span class="entity-type">{{entity_type_label}}</span>
            <span class="entity-confidence">{{confidence_score}}% confidence</span>
            <span class="entity-mentions">{{mention_count}} mentions</span>
        </div>
    </header>

    <main class="entity-content">
        <section class="entity-summary">
            {{entity_bio}}
        </section>

        <section class="entity-relationships">
            <h2>Connected Entities</h2>
            <div class="relationship-grid">
                {{#each relationships}}
                <div class="relationship-card">
                    <a href="{{target_url}}" class="relationship-link">
                        <span class="relationship-type">{{type}}</span>
                        <span class="relationship-target">{{target}}</span>
                    </a>
                </div>
                {{/each}}
            </div>
        </section>

        <section class="entity-articles">
            <h2>Recent Articles</h2>
            <div class="article-list">
                {{#each recent_articles}}
                <article class="article-card">
                    <h3><a href="{{url}}">{{title}}</a></h3>
                    <div class="article-meta">
                        <time>{{date}}</time>
                        <span class="source">{{source}}</span>
                    </div>
                    <p class="article-excerpt">{{excerpt}}</p>
                </article>
                {{/each}}
            </div>
        </section>
    </main>

    <aside class="entity-sidebar">
        <section class="entity-stats">
            <h3>Quick Facts</h3>
            <dl>
                <dt>First Mentioned</dt>
                <dd>{{first_mentioned}}</dd>
                <dt>Total Mentions</dt>
                <dd>{{mention_count}}</dd>
                <dt>Relationships</dt>
                <dd>{{relationship_count}}</dd>
                <dt>Last Updated</dt>
                <dd>{{last_updated}}</dd>
            </dl>
        </section>

        <section class="related-entities">
            <h3>Related Entities</h3>
            <ul class="entity-list">
                {{#each related_entities}}
                <li><a href="{{url}}">{{name}}</a></li>
                {{/each}}
            </ul>
        </section>
    </aside>

    <script src="/js/entity-pages.js"></script>
</body>
</html>
```

### 📰 **Enhanced Article Template**

```html
<article class="news-article">
    <header class="article-header">
        <h1>{{title}}</h1>
        <div class="article-meta">
            <time>{{published_date}}</time>
            <span class="source">{{source}}</span>
        </div>
    </header>

    <div class="article-content">
        {{enhanced_content}} <!-- With entity links -->
    </div>

    <aside class="article-entities">
        <h3>People & Places Mentioned</h3>
        <div class="entity-chips">
            {{#each entity_links}}
            <a href="{{url}}" class="entity-chip entity-{{type}}">
                {{text}}
            </a>
            {{/each}}
        </div>
    </aside>
</article>
```

## URL Structure & SEO

### 🔗 **Clean URL Design**

```
Entity Pages:
/entities/paige-cognetti/          # Mayor Cognetti
/entities/scranton/                # Scranton city page
/entities/ritz-theater/            # Ritz Theater venue
/entities/final-act/               # Final Act movie

Entity Collections:
/entities/people/                  # All people
/entities/people/government/       # Government officials
/entities/locations/               # All locations
/entities/works/movies/            # All movies

Article Pages:
/articles/2025/06/27/mayor-announces-project/
/articles/2025/06/25/final-act-filming/
```

### 📊 **SEO Optimization**

```html
<!-- Rich Schema.org markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Paige Gebhardt Cognetti",
  "jobTitle": "Mayor",
  "worksFor": {
    "@type": "Organization",
    "name": "City of Scranton"
  },
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Scranton",
    "addressRegion": "PA"
  },
  "url": "https://scrantenna.oboyle.co/entities/paige-cognetti/"
}
</script>
```

## Search & Discovery Features

### 🔍 **Entity Search**

```javascript
// Client-side search with Fuse.js
class EntitySearch {
    constructor() {
        this.index = null;
        this.loadSearchIndex();
    }
    
    async loadSearchIndex() {
        const response = await fetch('/entities/search-index.json');
        const entities = await response.json();
        
        this.index = new Fuse(entities, {
            keys: ['name', 'aliases', 'bio', 'tags'],
            threshold: 0.3
        });
    }
    
    search(query) {
        return this.index.search(query);
    }
}
```

### 📈 **Entity Analytics**

```javascript
// Track entity page views and interactions
class EntityAnalytics {
    trackEntityView(entityName, entityType) {
        gtag('event', 'entity_view', {
            'entity_name': entityName,
            'entity_type': entityType
        });
    }
    
    trackEntityLinkClick(fromArticle, toEntity) {
        gtag('event', 'entity_link_click', {
            'from_article': fromArticle,
            'to_entity': toEntity
        });
    }
}
```

## Content Enhancement Features

### 🔄 **Dynamic Content Updates**

```python
def update_entity_page_data():
    """Update entity pages with latest article mentions."""
    for entity in get_all_entities():
        # Find recent articles mentioning this entity
        recent_articles = find_articles_mentioning(entity['name'])
        
        # Update entity page with latest mentions
        update_entity_html(entity['slug'], {
            'recent_articles': recent_articles[:5],
            'mention_count': len(recent_articles),
            'last_updated': datetime.now()
        })
```

### 🎯 **Smart Entity Suggestions**

```python
def suggest_related_entities(current_entity):
    """Suggest related entities based on co-occurrence in articles."""
    related = []
    
    # Find entities that appear in same articles
    co_occurring = find_co_occurring_entities(current_entity)
    
    # Rank by relationship strength
    for entity, strength in co_occurring:
        if strength > 0.3:  # Significant co-occurrence
            related.append({
                'entity': entity,
                'strength': strength,
                'reason': f"Mentioned together in {count} articles"
            })
    
    return sorted(related, key=lambda x: x['strength'], reverse=True)[:5]
```

## Implementation Phases

### 🚀 **Phase 1: Basic Entity Publishing**
1. Build `entity_web_publisher.py`
2. Create HTML templates
3. Implement markdown → HTML conversion
4. Generate static entity pages
5. Deploy to `/entities/` subdirectory

### 🔗 **Phase 2: Article Entity Linking**  
1. Build `article_entity_linker.py`
2. Implement entity mention detection
3. Generate enhanced article pages
4. Add entity chips/tags to articles
5. Create entity → article cross-references

### 🔍 **Phase 3: Search & Discovery**
1. Generate search index JSON
2. Implement client-side entity search
3. Add "Related Entities" suggestions
4. Create entity browsing interfaces
5. Add analytics tracking

### 📊 **Phase 4: Advanced Features**
1. Real-time entity page updates
2. Entity relationship visualization
3. Trending entities dashboard
4. Entity timeline views
5. Social sharing optimization

## Success Metrics

### 📈 **User Engagement**
- **Entity page views**: Track most popular entities
- **Click-through rates**: Article → entity navigation
- **Time on entity pages**: Measure engagement depth
- **Entity search usage**: Popular search terms

### 🎯 **Knowledge Discovery**
- **Entity relationship exploration**: Graph navigation patterns
- **Cross-article discovery**: Related article views from entity pages
- **Search query analysis**: What entities people want to know about
- **Content gap identification**: Entities with high interest but low content

## The Vision Realized

This creates a **living knowledge ecosystem** where:

1. **Every article** becomes a gateway to deeper knowledge exploration
2. **Entity pages** serve as authoritative sources for local information  
3. **Users can explore** Scranton's knowledge graph through intuitive web navigation
4. **Search engines index** rich, interconnected content about Scranton
5. **The knowledge base grows** more valuable with every article published

**Result**: Scrantenna becomes the **definitive digital resource** for understanding Scranton's people, places, organizations, and their relationships - transforming local news consumption into knowledge discovery.

---

*🌐 Transform entity vault into public knowledge web with searchable pages and intelligent article linking.*