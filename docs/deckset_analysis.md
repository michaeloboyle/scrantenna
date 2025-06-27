# Deckset Integration Analysis for Scrantenna

## Deckset Overview

**Deckset** is a popular macOS presentation app that converts Markdown files into beautiful slides with minimal configuration. It uses special markdown syntax and directives to control slide layouts, text sizing, and visual effects.

## Key Deckset Features for Scrantenna Integration

### Text Formatting Directives

```markdown
# [fit] Large Headline Text
## Normal Subtitle
### [fit] Another fitted line

^ Presenter notes (hidden from audience)

---

# New slide starts after triple dash
```

### Image Styling Options

```markdown
![](image.jpg)              # Full background image
![left](image.jpg)          # Image on left, text on right  
![right](image.jpg)         # Image on right, text on left
![inline](image.jpg)        # Inline image in text flow
![original](image.jpg)      # Image at original size
![fit](image.jpg)           # Image scaled to fit slide
![50%](image.jpg)           # Image at 50% size
![filtered](image.jpg)      # Apply filter effects
```

### Layout Variations

```markdown
# [fit] **Mayor Announces**
# [fit] Infrastructure Project

![right filtered](scranton-infrastructure.jpg)

* $2 million investment
* Providence Road improvements  
* Expected completion: Fall 2025

^ This slide shows the infrastructure announcement with supporting details
```

## Scrantenna Presentation Mode Concept

### Enhanced News Shorts for Presentations

Transform news shorts into presentation slides with:

1. **[fit] Headlines** - Auto-scaling text that fills available space
2. **Background Images** - News photos as slide backgrounds
3. **Clean Typography** - Presentation-ready text layout
4. **Slide Transitions** - Smooth navigation between news stories
5. **Presenter Mode** - Speaker notes and timing controls

### Practical Applications

1. **City Council Presentations** - News updates for municipal meetings
2. **Community Briefings** - Visual summaries of local developments
3. **Social Media Content** - Instagram/LinkedIn slide carousels
4. **Newsroom Displays** - Digital signage in news organizations
5. **Educational Content** - Civic engagement presentations

## Implementation Strategy

### Phase 1: Core Deckset Syntax Support

```javascript
// Parse Deckset-style markdown directives
function parseDecksetSyntax(text) {
    const fitPattern = /\[fit\]\s*(.+?)$/gm;
    const imagePattern = /!\[(.*?)\]\((.*?)\)/g;
    const notePattern = /^\^(.+?)$/gm;
    
    return {
        title: extractFitText(text),
        images: extractImages(text),
        notes: extractNotes(text),
        content: cleanContent(text)
    };
}

// Auto-scale text to fit container
function applyFitSizing(element, text) {
    const container = element.parentElement;
    let fontSize = 120; // Start large
    
    element.style.fontSize = fontSize + 'px';
    element.textContent = text;
    
    while (element.scrollWidth > container.clientWidth && fontSize > 20) {
        fontSize -= 2;
        element.style.fontSize = fontSize + 'px';
    }
}
```

### Phase 2: Enhanced Visual Styling

```css
/* Presentation mode styles */
.presentation-mode {
    font-family: 'SF Pro Display', -apple-system, sans-serif;
    background: #000;
    color: #fff;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.slide {
    width: 90vw;
    height: 90vh;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem;
}

.fit-text {
    font-weight: 900;
    line-height: 0.9;
    text-align: center;
    word-wrap: break-word;
    hyphens: auto;
}

.slide-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
    opacity: 0.7;
}

.slide-background.filtered {
    filter: brightness(0.4) contrast(1.2) saturate(0.8);
}

.presenter-notes {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,0.9);
    color: #fff;
    padding: 1rem;
    font-size: 0.9rem;
    transform: translateY(100%);
    transition: transform 0.3s ease;
}

.presenter-notes.visible {
    transform: translateY(0);
}
```

### Phase 3: News-Specific Enhancements

```javascript
// Convert news article to presentation slide
function createPresentationSlide(article, style = 'default') {
    const templates = {
        headline: `
# [fit] **${article.title_distilled || article.title}**

![right filtered](${article.urlToImage})

## ${article.source}
### ${formatDate(article.publishedAt)}

^ ${article.description}
        `,
        
        breakdown: `
![](${article.urlToImage})

# [fit] ${extractMainPoint(article)}

* ${extractBulletPoints(article).join('\n* ')}

^ Full article: ${article.url}
        `,
        
        visual: `
![filtered](${article.urlToImage})

# [fit] **${article.title_distilled}**

^ Published: ${article.publishedAt}
^ Source: ${article.source}
^ ${article.description}
        `
    };
    
    return templates[style] || templates.headline;
}
```

## Enhanced Shorts Viewer with Presentation Mode

### New Features

1. **Presentation Toggle** - Switch between TikTok-style and presentation mode
2. **Slide Export** - Generate PNG/PDF slides for external use
3. **Timing Controls** - Auto-advance with configurable intervals
4. **Speaker View** - Dual-screen support with notes
5. **Template Selection** - Multiple presentation layouts

### Implementation Files

1. **`presentation_mode.html`** - Dedicated presentation interface
2. **`deckset_parser.js`** - Markdown syntax processing
3. **`slide_generator.py`** - Server-side slide creation
4. **`presentation_styles.css`** - Deckset-inspired styling

## Integration with Existing Pipeline

### Modified Shorts Generation

```python
def create_presentation_slide(article: Dict, template: str = "headline") -> Dict:
    """Create presentation slide from news article."""
    
    # Extract key visual elements
    main_image = article.get('urlToImage', '')
    headline = article.get('title_distilled', article.get('title', ''))
    source = article.get('source', {}).get('name', 'Unknown')
    
    # Generate Deckset-style markdown
    if template == "headline":
        markdown = f"""# [fit] **{headline}**

![right filtered]({main_image})

## {source}
### {format_date(article.get('publishedAt', ''))}

^ {article.get('description', '')}
"""
    
    elif template == "visual":
        markdown = f"""![filtered]({main_image})

# [fit] **{headline}**

^ Published: {article.get('publishedAt', '')}
^ Source: {source}
^ {article.get('description', '')}
"""
    
    return {
        "markdown": markdown,
        "template": template,
        "background_image": main_image,
        "fit_text": headline,
        "presenter_notes": article.get('description', ''),
        "metadata": {
            "source": source,
            "published": article.get('publishedAt', ''),
            "url": article.get('url', '')
        }
    }
```

### Enhanced Web Interface

```html
<!-- Presentation mode toggle -->
<div class="mode-controls">
    <button class="mode-btn" onclick="setMode('shorts')">
        📱 Shorts
    </button>
    <button class="mode-btn" onclick="setMode('presentation')">
        🎥 Presentation
    </button>
</div>

<!-- Presentation-specific controls -->
<div class="presentation-controls" id="presentationControls">
    <button onclick="togglePresenterNotes()">📝 Notes</button>
    <button onclick="exportSlides()">💾 Export</button>
    <button onclick="toggleAutoAdvance()">⏱️ Auto</button>
    <select onchange="changeTemplate(this.value)">
        <option value="headline">Headline</option>
        <option value="visual">Visual</option>
        <option value="breakdown">Breakdown</option>
    </select>
</div>
```

## Use Cases and Benefits

### Municipal Government
- **City Council Meetings** - Visual news summaries
- **Public Information Sessions** - Community updates
- **Press Conferences** - Professional presentation slides

### News Organizations
- **Editorial Meetings** - Story planning presentations
- **Social Media Content** - Multi-slide Instagram posts
- **Digital Signage** - Newsroom displays

### Community Organizations
- **Civic Engagement** - Local news discussions
- **Educational Presentations** - Current events classes
- **Public Speaking** - Community leader briefings

### Corporate Communications
- **Team Updates** - Local business news
- **Stakeholder Briefings** - Market condition presentations
- **Training Materials** - Media literacy education

## Technical Implementation Plan

### Week 1: Core Deckset Parser
- [ ] Implement markdown directive parsing
- [ ] Create [fit] text scaling algorithm
- [ ] Add basic image positioning support

### Week 2: Presentation Interface
- [ ] Build presentation mode UI
- [ ] Implement slide navigation
- [ ] Add presenter notes functionality

### Week 3: Enhanced Styling
- [ ] Create multiple presentation templates
- [ ] Implement image filtering and effects
- [ ] Add slide transition animations

### Week 4: Integration & Export
- [ ] Integrate with existing shorts pipeline
- [ ] Add slide export functionality (PNG/PDF)
- [ ] Implement auto-advance timing controls

This enhancement transforms Scrantenna from a TikTok-style viewer into a professional presentation tool while maintaining its core news aggregation and processing capabilities.